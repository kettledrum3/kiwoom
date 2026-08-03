import os
import json
import requests
import logging
import math
import time
from dotenv import load_dotenv
from typing import Tuple, List, Literal, Optional
from datetime import datetime, timedelta

from core.brokers.base import Broker
from core.cavr import kis_headers, invalidate_access_token_controlled
from core.database import log_order_db
from core.notifier import send_telegram_message

logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))

class KiwoomKrBroker(Broker):
    _notified = False  # 프로세스 내 최초 알림 여부 플래그

    def __init__(self):
        # 1. 공통 환경 변수(.env) 로드
        common_env_path = os.path.join(PROJECT_ROOT, "env", ".env")
        if os.path.exists(common_env_path):
            load_dotenv(common_env_path, override=True)

        # 2. 한국 시장 전용 환경 변수(.env.kr) 로드 및 병합 (override)
        env_path = os.path.join(PROJECT_ROOT, "env", ".env.kr")
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            logger.debug(f"[KiwoomKrBroker] 환경 변수 로드 완료: {env_path}")

        # 3. 거래 모드(REAL vs MOCK) 판별 및 변수 설정
        from core.database import get_trade_mode
        trade_mode = get_trade_mode()

        if trade_mode == "MOCK":
            self.base_url = os.getenv("MOCK_BASE_URL", "https://mockapi.kiwoom.com").strip()
            self.account_no = os.getenv("MOCKKR_ACCOUNT_NO", "").strip()
            self.is_simulation = True
            mode_display = "모의 계좌 (MOCK)"
        else:
            self.base_url = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").strip()
            self.account_no = os.getenv("KIWOOM_ACCOUNT_NO", "").strip()
            self.is_simulation = False
            mode_display = "실전 계좌 (REAL)"

        logger.debug(f"[KiwoomKrBroker] 연결 계좌 번호: {self.account_no} (모드: {trade_mode})")
        
        if not KiwoomKrBroker._notified:
            send_telegram_message(f"🇰🇷 <b>[Kiwoom KR 브로커 시작 - {mode_display}]</b>\n연결 계좌: <code>{self.account_no}</code>")
            KiwoomKrBroker._notified = True

        self.cano = self.account_no
        self.trade_mode = trade_mode
        self.etf_tickers = self._load_etf_list()

    def _call_api(self, method, url, tr_id, params=None, data=None, extra_headers=None):
        res = None
        max_retries = 3
        for attempt in range(max_retries):
            # KIS 헤더 함수를 호출하여 키움 REST 헤더(api-id, authorization)를 생성함
            headers = kis_headers(tr_id, market="KR", trade_mode=self.trade_mode)
            if not headers:
                logger.warning(f"⚠️ [KR API] 헤더 생성 실패 (토큰 쿨다운 중). 5초 대기 후 재시도 ({attempt+1}/{max_retries})")
                time.sleep(5.0)
                continue

            if extra_headers:
                headers.update(extra_headers)

            logger.debug(f"[KR API Call] TR_ID: {tr_id}, URL: {url}, Attempt: {attempt+1}")
            try:
                res = requests.request(method, url, headers=headers, params=params, data=data, verify=False)
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ [KR API] Network Error: {e}. Retrying ({attempt+1}/{max_retries})...")
                    time.sleep(1.0)
                    continue
                else:
                    logger.error(f"❌ [KR API] Final failure after {max_retries} attempts: {e}")
                    return None
            
            # 토큰 만료 대응 (401 Unauthorized)
            if res.status_code == 401:
                logger.warning(f"⚠️ [KR API] 토큰 만료(401). 1초 대기 후 재발급 및 재시도.")
                invalidate_access_token_controlled(market="KR", account_no=self.account_no, trade_mode=self.trade_mode)
                time.sleep(1.0)
                continue
            
            # 서버 에러 대응 (500)
            if res.status_code == 500:
                logger.warning(f"⚠️ [KR API] Kiwoom 서버 에러(500). 1초 대기 후 재시도 ({attempt+1}/{max_retries})")
                time.sleep(1.0)
                continue
            
            if res.status_code == 200:
                res_data = res.json()
                # 키움 API 리턴코드 확인
                rt_cd = res_data.get('return_code')
                rt_msg = res_data.get('return_msg', '')
                logger.debug(f"[KR API Resp] TR_ID: {tr_id}, rt_cd: {rt_cd}, msg: {rt_msg}")
                
                # 토큰 오류 감지 및 대응
                if rt_msg and any(x in rt_msg for x in ["Token", "token", "토큰", "투자구분"]):
                    logger.warning(f"⚠️ [KR API] 토큰 오류 감지 ({rt_msg}). 토큰 무효화 후 재발급 재시도.")
                    invalidate_access_token_controlled(market="KR", account_no=self.account_no, trade_mode=self.trade_mode)
                    time.sleep(1.0)
                    continue

                # TPS 제한 감지 및 대응
                if rt_msg and "초당 거래건수를 초과" in rt_msg:
                    logger.warning(f"⚠️ [KR API] TPS 제한 감지. 2초 후 재시도 ({attempt+1}/{max_retries})")
                    time.sleep(2.0)
                    continue
                return res
            
            return res
        return res

    def _load_etf_list(self) -> List[str]:
        tickers = []
        try:
            etf_path = os.path.join(PROJECT_ROOT, "env", "ETF_list_kr.txt")
            if os.path.exists(etf_path):
                with open(etf_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.split('#')[0].strip()
                        if line:
                            tickers.append(line.split()[0])
        except Exception as e:
            logger.warning(f"[KiwoomKrBroker] ETF 리스트 로드 실패 (기본 호가 단위 적용): {e}")
        return tickers

    def get_price(self, symbol: str) -> float:
        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"stk_cd": symbol}
        res = self._call_api("POST", url, "ka10001", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                val = data.get('cur_prc')
                if val is not None:
                    return float(val)
        logger.error(f"[KR] 현재가 조회 실패 ({symbol}): {res.text if res else 'No Response'}")
        return 0.0

    def get_previous_close(self, symbol: str) -> float:
        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"stk_cd": symbol}
        res = self._call_api("POST", url, "ka10001", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                val = data.get('base_pric')
                if val is not None:
                    return float(val)
        logger.error(f"[KR] 전일종가 조회 실패 ({symbol}): {res.text if res else 'No Response'}")
        return 0.0

    def get_current_high(self, symbol: str) -> float:
        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"stk_cd": symbol}
        res = self._call_api("POST", url, "ka10001", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                val = data.get('high_pric')
                if val is not None:
                    return float(val)
        return 0.0

    def get_current_low(self, symbol: str) -> float:
        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"stk_cd": symbol}
        res = self._call_api("POST", url, "ka10001", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                val = data.get('low_pric')
                if val is not None:
                    return float(val)
        return 0.0

    def get_last_5_day_avg_close(self, symbol: str) -> float:
        url = f"{self.base_url}/api/dostk/chart"
        today_str = datetime.now().strftime("%Y%m%d")
        body = {
            "stk_cd": symbol,
            "base_dt": today_str,
            "upd_stkpc_tp": "1"
        }
        try:
            res = self._call_api("POST", url, "ka10081", data=json.dumps(body))
            if res:
                data = res.json()
                if data.get('return_code') == 0:
                    chart_list = data.get('stk_dt_pole_chart_qry', [])
                    
                    # 오늘 날짜 항목 제외
                    valid_items = [item for item in chart_list if item.get('dt') != today_str]
                    closes = [float(item['cur_prc']) for item in valid_items[:5] if item.get('cur_prc')]
                    
                    if len(closes) >= 5:
                        avg_close = sum(closes) / 5.0
                        logger.info(f"📊 [{symbol}] 직전 5일 종가 평균: ₩{int(avg_close):,}")
                        return avg_close
            logger.warning(f"[KR] 5일 평균가 조회 실패 ({symbol})")
        except Exception as e:
            logger.error(f"[KR] 5일 평균가 파싱 오류: {e}")
        return 0.0

    def get_account_equity(self, symbol: str) -> Tuple[float, float, float]:
        url = f"{self.base_url}/api/dostk/acnt"
        body = {
            "qry_tp": "0",
            "dmst_stex_tp": "KRX"
        }
        try:
            res = self._call_api("POST", url, "kt00004", data=json.dumps(body))
            if not res:
                return 0.0, 0.0, 0.0
            data = res.json()
            if data.get('return_code') != 0:
                logger.error(f"[KR] 잔고 조회 실패: {data.get('return_msg')}")
                return 0.0, 0.0, 0.0
                
            for item in data.get('stk_acnt_evlt_prst', []):
                item_cd = item.get('stk_cd', '').strip()
                # 접두사 A 등 제거 후 비교
                if item_cd.endswith(symbol.strip()):
                    return float(item.get('rmnd_qty', 0)), float(item.get('avg_prc', 0)), float(item.get('evlt_amt', 0))
        except Exception as e:
            logger.error(f"[KR] 잔고 조회 중 오류 발생: {e}")
        return 0.0, 0.0, 0.0

    def get_cumulative_buy_amount(self, symbol: str) -> float:
        res = self.get_account_equity(symbol)
        if res is None:
            return 0.0
        shares, avg_price, _ = res
        return shares * avg_price

    def get_cash_pool(self) -> float:
        url = f"{self.base_url}/api/dostk/acnt"
        body = {
            "qry_tp": "0",
            "dmst_stex_tp": "KRX"
        }
        res = self._call_api("POST", url, "kt00004", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                # D+2추정예수금 반환
                val = data.get('d2_entra')
                if val is not None:
                    return float(val)
        logger.error("[KR] 예수금 조회 실패")
        return 0.0

    def adjust_price_by_tick(self, symbol: str, price: float, order_type: Literal["BUY", "SELL"]) -> float:
        # ETF는 호가단위가 무조건 5원임 (한국 시장 기준)
        if symbol in self.etf_tickers or symbol.startswith("5") or symbol.startswith("1") or symbol.startswith("2") or symbol.startswith("3") or symbol.startswith("4"):
            tick = 5.0
            if order_type == "BUY":
                return math.ceil(price / tick) * tick
            else:
                return math.floor(price / tick) * tick
        
        # 일반 코스피/코스닥 주식 호가 단위 (마이그레이션용 기본값 유지)
        if price < 2000:
            tick = 1.0
        elif price < 5000:
            tick = 5.0
        elif price < 20000:
            tick = 10.0
        elif price < 50000:
            tick = 50.0
        elif price < 200000:
            tick = 100.0
        elif price < 500000:
            tick = 500.0
        else:
            tick = 1000.0

        if order_type == "BUY":
            return math.ceil(price / tick) * tick
        else:
            return math.floor(price / tick) * tick

    def place_order(self, symbol: str, price: float, qty: float, order_type: Literal["BUY", "SELL"], price_type: str = "00", strategy: str = "MANUAL", strategy_name: str = "") -> bool:
        """
        [국내주식] 주문 전송
        price_type (trde_tp): 지정가: "0", 시장가: "3" (키움증권 REST API 명세 기준)
        """
        action = "BUY" if order_type == "BUY" else "SELL"
        tr_id = "kt10000" if action == "BUY" else "kt10001"
        url = f"{self.base_url}/api/dostk/ordr"

        # KIS의 "00" 지정가, "01" 시장가를 키움 규격인 "0", "3"으로 보정
        if price_type in ["00", "0"]:
            trde_tp = "0"
            ord_uv = str(int(price))
        elif price_type in ["01", "3"]:
            trde_tp = "3"
            ord_uv = "0" # 시장가는 가격 0으로 제출
        else:
            trde_tp = "0" # 기본 지정가
            ord_uv = str(int(price))

        body = {
            "dmst_stex_tp": "KRX",
            "stk_cd": symbol,
            "ord_qty": str(int(qty)),
            "ord_uv": ord_uv,
            "trde_tp": trde_tp,
            "cond_uv": ""
        }

        try:
            res = self._call_api("POST", url, tr_id, data=json.dumps(body))
            if not res:
                return False
            data = res.json()
            if data.get('return_code') == 0:
                odno = data.get('ord_no')
                logger.info(f"🟢 [KR 주문 성공] {strategy} {action} {symbol} {qty}주 @ {price} (주문번호: {odno})")
                log_order_db(symbol, strategy, action, price, qty, trde_tp, "ORDERED", odno, "성공", market="KR", strategy_name=strategy_name)
                return True
            else:
                msg = data.get('return_msg', '알 수 없는 오류')
                logger.error(f"🔴 [KR 주문 실패] {strategy} {action} {symbol} {qty}주 @ {price} -> {msg}")
                log_order_db(symbol, strategy, action, price, qty, trde_tp, "FAILED", "", msg, market="KR", strategy_name=strategy_name)
                send_telegram_message(f"🔴 <b>[KR 주문 실패]</b>\n종목: {symbol}\n유형: {action}\n사유: {msg}")
                return False
        except Exception as e:
            logger.error(f"❌ [KR 주문 예외 발생] {e}")
            return False

    def fetch_open_orders(self, symbol: str) -> List[dict]:
        """미체결 주문 조회 (TR: kt00007)"""
        url = f"{self.base_url}/api/dostk/acnt"
        body = {
            "qry_tp": "0" # 0: 전체조회
        }
        orders = []
        try:
            res = self._call_api("POST", url, "kt00007", data=json.dumps(body))
            if res:
                data = res.json()
                if data.get('return_code') == 0:
                    for item in data.get('output1', []):
                        item_cd = item.get('stk_cd', '').strip()
                        # 접두사 A 등 제거 후 비교, 미체결 수량이 있는 것만 필터링
                        uncl_qty = float(item.get('uncl_qty', 0))
                        if item_cd.endswith(symbol.strip()) and uncl_qty > 0:
                            orders.append({
                                "odno": item.get('ord_no'),
                                "symbol": symbol,
                                "price": float(item.get('ord_uv', 0)),
                                "qty": float(item.get('ord_qty', 0)),
                                "uncl_qty": uncl_qty,
                                "side": "BUY" if item.get('slby_tp') == '2' else "SELL"
                            })
        except Exception as e:
            logger.error(f"[KR] 미체결 조회 중 오류 발생: {e}")
        return orders

    def fetch_execution_history(self, symbol: str, start_date: str, end_date: str) -> List[dict]:
        """당일 주문체결내역 상세조회 (TR: kt00007)"""
        url = f"{self.base_url}/api/dostk/acnt"
        body = {
            "qry_tp": "0"
        }
        history = []
        try:
            res = self._call_api("POST", url, "kt00007", data=json.dumps(body))
            if res:
                data = res.json()
                if data.get('return_code') == 0:
                    for item in data.get('output1', []):
                        item_cd = item.get('stk_cd', '').strip()
                        cntr_qty = float(item.get('cntr_qty', 0))
                        if item_cd.endswith(symbol.strip()) and cntr_qty > 0:
                            history.append({
                                "odno": item.get('ord_no'),
                                "symbol": symbol,
                                "price": float(item.get('cntr_uv', 0)),
                                "qty": cntr_qty,
                                "side": "BUY" if item.get('slby_tp') == '2' else "SELL",
                                "time": item.get('ord_time', '')
                            })
        except Exception as e:
            logger.error(f"[KR] 체결이력 조회 중 오류 발생: {e}")
        return history

    def fetch_daily_chart(self, symbol: str, days: int = 300) -> Optional[List[dict]]:
        """국내주식 일자별 시세 조회 (TR: ka10081)"""
        url = f"{self.base_url}/api/dostk/chart"
        all_rows = []
        next_key = ""
        base_dt = datetime.now().strftime("%Y%m%d")
        
        # [FIX] days 기간에 따라 연속 조회(Pagination) 루프 횟수를 동적으로 계산
        max_loops = max(5, (days // 15) + 2)
        
        for _ in range(max_loops):
            if len(all_rows) >= days:
                break
                
            # [ADD] 과도한 API 호출로 인한 서버 차단 방지용 짧은 딜레이 추가
            time.sleep(1.0)
                
            body = {
                "stk_cd": symbol,
                "base_dt": base_dt,
                "upd_stkpc_tp": "1"
            }
            extra_headers = {}
            if next_key:
                extra_headers["next-key"] = next_key
                extra_headers["cont-yn"] = "Y"
                
            res = self._call_api("POST", url, "ka10081", data=json.dumps(body), extra_headers=extra_headers)
            if not res:
                break
            data = res.json()
            if data.get('return_code') != 0:
                break
                
            items = data.get('stk_dt_pole_chart_qry', [])
            if not items:
                break
                
            for item in items:
                all_rows.append({
                    "Date": item.get('dt'),
                    "Open": float(item.get('open_pric', 0)),
                    "High": float(item.get('high_pric', 0)),
                    "Low": float(item.get('low_pric', 0)),
                    "Close": float(item.get('cur_prc', 0)),
                    "% change": "0.0%",
                    "Volume": int(float(item.get('trde_qty', 0)))
                })
                
            cont_yn = res.headers.get("cont-yn", "N")
            next_key = res.headers.get("next-key", "")
            if cont_yn != "Y" or not next_key:
                break
            base_dt = items[-1].get('dt')
            if not base_dt:
                break
                
        return all_rows[:days]
