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

        # 캐시 딕셔너리 초기화
        self._stkinfo_cache = {}
        self._prev_close_cache = {}
        self._acnt_cache = {}

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
            
            # 429 Too Many Requests 대응
            if res.status_code == 429:
                logger.warning(f"⚠️ [KR API] 429 Too Many Requests 감지. 1.5초 대기 후 재시도 ({attempt+1}/{max_retries})")
                time.sleep(1.5)
                continue

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

                # TPS 및 요청건수 제한 감지 및 대응
                if rt_cd == 5 or (rt_msg and "요청 건수를 초과" in rt_msg):
                    if "일 API 요청 건수" in rt_msg or "일일" in rt_msg:
                        logger.error(f"🔴 [KR API] 일일 API 요청 한도 초과 감지: {rt_msg}")
                        return res
                    logger.warning(f"⚠️ [KR API] TPS 초과 제한 감지 ({rt_msg}). 1.5초 후 재시도 ({attempt+1}/{max_retries})")
                    time.sleep(1.5)
                    continue

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

    def _get_stkinfo(self, symbol: str) -> Optional[dict]:
        """주식기본정보(ka10001) 캐싱 헬퍼 (5초 유효)"""
        now_ts = time.time()
        if hasattr(self, '_stkinfo_cache') and symbol in self._stkinfo_cache:
            cache_ts, cache_data = self._stkinfo_cache[symbol]
            if now_ts - cache_ts < 5.0:
                logger.debug(f"💾 [KR Price Cache Hit] {symbol} 시세 캐시 재사용")
                return cache_data

        url = f"{self.base_url}/api/dostk/stkinfo"
        body = {"stk_cd": symbol}
        res = self._call_api("POST", url, "ka10001", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                self._stkinfo_cache[symbol] = (now_ts, data)
                return data
        return None

    def get_price(self, symbol: str, force: bool = False) -> float:
        data = self._get_stkinfo(symbol)
        if data:
            val = data.get('cur_prc')
            if val is not None:
                clean_val = str(val).replace('+', '').replace('-', '')
                return float(clean_val)
        logger.error(f"[KR] 현재가 조회 실패 ({symbol})")
        return 0.0

    def get_previous_close(self, symbol: str) -> float:
        # 오늘 날짜 기준으로 전일종가 캐시 확인
        today_str = datetime.now().strftime("%Y%m%d")
        if hasattr(self, '_prev_close_cache') and symbol in self._prev_close_cache:
            cache_date, val = self._prev_close_cache[symbol]
            if cache_date == today_str:
                return val

        # ka10086 (일별주가요청)을 사용하여 정확한 전일종가 획득
        url = f"{self.base_url}/api/dostk/mrkcond"
        body = {
            "stk_cd": symbol,
            "qry_dt": today_str,
            "indc_tp": "0"
        }
        res = self._call_api("POST", url, "ka10086", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                daly_stkpc = data.get('daly_stkpc', [])
                if daly_stkpc:
                    # 첫 번째 영업일이 오늘과 같으면, 두 번째 영업일이 전일 종가임
                    if daly_stkpc[0].get('date') == today_str:
                        if len(daly_stkpc) > 1:
                            val = daly_stkpc[1].get('close_pric')
                        else:
                            val = daly_stkpc[0].get('close_pric')
                    else:
                        val = daly_stkpc[0].get('close_pric')

                    if val is not None:
                        clean_val = str(val).replace('+', '').replace('-', '')
                        float_val = float(clean_val)
                        self._prev_close_cache[symbol] = (today_str, float_val)
                        return float_val
        logger.error(f"[KR] 전일종가 조회 실패 ({symbol}): {res.text if res else 'No Response'}")
        return 0.0

    def get_current_high(self, symbol: str) -> float:
        data = self._get_stkinfo(symbol)
        if data:
            val = data.get('high_pric')
            if val is not None:
                clean_val = str(val).replace('+', '').replace('-', '')
                return float(clean_val)
        return 0.0

    def get_current_low(self, symbol: str) -> float:
        data = self._get_stkinfo(symbol)
        if data:
            val = data.get('low_pric')
            if val is not None:
                clean_val = str(val).replace('+', '').replace('-', '')
                return float(clean_val)
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

    def _get_acnt_info(self) -> Optional[dict]:
        """계좌 잔고 및 예수금 정보(kt00004) 캐싱 헬퍼 (5초 유효)"""
        now_ts = time.time()
        cache_key = "acnt_info"
        if hasattr(self, '_acnt_cache') and cache_key in self._acnt_cache:
            cache_ts, cache_data = self._acnt_cache[cache_key]
            if now_ts - cache_ts < 5.0:
                logger.debug("💾 [KR Account Cache Hit] 계좌 정보 캐시 재사용")
                return cache_data

        url = f"{self.base_url}/api/dostk/acnt"
        body = {
            "qry_tp": "0",
            "dmst_stex_tp": "KRX"
        }
        res = self._call_api("POST", url, "kt00004", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                if not hasattr(self, '_acnt_cache'):
                    self._acnt_cache = {}
                self._acnt_cache[cache_key] = (now_ts, data)
                return data
        return None

    def get_account_equity(self, symbol: str) -> Optional[Tuple[float, float, float]]:
        try:
            data = self._get_acnt_info()
            if not data:
                return None
                
            for item in data.get('stk_acnt_evlt_prst', []):
                item_cd = item.get('stk_cd', '').strip()
                # 접두사 A 등 제거 후 비교
                if item_cd.endswith(symbol.strip()):
                    return float(item.get('rmnd_qty', 0)), float(item.get('avg_prc', 0)), float(item.get('evlt_amt', 0))
            # 결과 리스트에 종목이 없으면 보유 수량 0
            return 0.0, 0.0, 0.0
        except Exception as e:
            logger.error(f"[KR] 잔고 조회 중 오류 발생: {e}")
            return None

    def get_cumulative_buy_amount(self, symbol: str) -> float:
        res = self.get_account_equity(symbol)
        if res is None:
            return 0.0
        shares, avg_price, _ = res
        return shares * avg_price

    def get_cash_pool(self) -> float:
        data = self._get_acnt_info()
        if data:
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

    def place_order(self, symbol: str, price: float, qty: float, order_type: Literal["BUY", "SELL"], price_type: str = "0", strategy: str = "MANUAL", strategy_name: str = "", stop_price: Optional[float] = None) -> bool:
        """
        [국내주식] 주문 전송
        매매구분(trde_tp): 0:보통, 3:시장가, 5:조건부지정가, 81:장마감후시간외, 61:장시작전시간외, 62:시간외단일가, 6:최유리지정가, 7:최우선지정가, 10:보통(IOC), 13:시장가(IOC), 16:최유리(IOC), 20:보통(FOK), 23:시장가(FOK), 26:최유리(FOK), 28:스톱지정가, 29:중간가, 30:중간가(IOC), 31:중간가(FOK)
        """
        # 모의투자(MOCK) 모드이고 시장가 주문이 요청된 경우, 현재가 기준으로 지정가 호가 보정 우회 처리
        if self.trade_mode == "MOCK" and price_type in ["3", "13", "23"]:
            current_price = self.get_price(symbol)
            if current_price > 0:
                tick_diff = 10 if order_type == "BUY" else -10
                price = current_price + tick_diff
                price = self.adjust_price_by_tick(symbol, price, order_type)
                price_type = "0"
                logger.info(f"🔄 [MOCK KR 시장가 우회] 시장가 주문을 지정가 {price:.0f}로 변환하여 제출합니다. ({symbol})")
            else:
                logger.error(f"❌ [MOCK KR 시장가 우회 실패] 현재가를 조회할 수 없어 주문을 진행하지 않습니다. ({symbol})")
                return False

        action = "BUY" if order_type == "BUY" else "SELL"
        tr_id = "kt10000" if action == "BUY" else "kt10001"
        url = f"{self.base_url}/api/dostk/ordr"

        trde_tp = price_type
        # 시장가/IOC시장가/FOK시장가 유형은 단가를 "0"으로 입력
        if trde_tp in ["3", "13", "23"]:
            ord_uv = "0"
        else:
            ord_uv = str(int(price))

        cond_uv = ""
        if stop_price is not None:
            cond_uv = str(int(stop_price))
        elif trde_tp == "28":
            cond_uv = str(int(price))

        body = {
            "dmst_stex_tp": "KRX",
            "stk_cd": symbol,
            "ord_qty": str(int(qty)),
            "ord_uv": ord_uv,
            "trde_tp": trde_tp,
            "cond_uv": cond_uv
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
