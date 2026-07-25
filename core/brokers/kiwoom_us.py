import os
import json
import time
import requests
import logging
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

class KiwoomUsBroker(Broker):
    _notified = False  # 프로세스 내 최초 알림 여부 플래그

    def __init__(self):
        # 1. 공통 환경 변수(.env) 로드
        common_env_path = os.path.join(PROJECT_ROOT, "env", ".env")
        if os.path.exists(common_env_path):
            load_dotenv(common_env_path, override=True)

        # 2. 미국 시장 전용 환경 변수(.env.us) 로드 및 병합 (override)
        env_path = os.path.join(PROJECT_ROOT, "env", ".env.us")
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            logger.info(f"[KiwoomUsBroker] 환경 변수 로드 완료: {env_path}")

        # 3. 거래 모드(REAL vs MOCK) 판별 및 변수 설정
        from core.database import get_trade_mode
        trade_mode = get_trade_mode()

        if trade_mode == "MOCK":
            self.base_url = os.getenv("MOCK_BASE_URL", "https://mockapi.kiwoom.com").strip()
            self.account_no = os.getenv("MOCKUS_ACCOUNT_NO", "").strip()
            self.is_simulation = True
            mode_display = "모의 계좌 (MOCK)"
        else:
            self.base_url = os.getenv("KIWOOM_BASE_URL", "https://api.kiwoom.com").strip()
            self.account_no = os.getenv("KIWOOM_ACCOUNT_NO", "").strip()
            self.is_simulation = False
            mode_display = "실전 계좌 (REAL)"

        logger.info(f"[KiwoomUsBroker] 연결 계좌 번호: {self.account_no} (모드: {trade_mode})")
        
        if not KiwoomUsBroker._notified:
            send_telegram_message(f"🇺🇸 <b>[Kiwoom US 브로커 시작 - {mode_display}]</b>\n연결 계좌: <code>{self.account_no}</code>")
            KiwoomUsBroker._notified = True

        self.cano = self.account_no
        
        # 키움용 거래소 맵 (NASDAQ: ND, NYSE: NY, AMEX: NA)
        self.exchange_map = {"TQQQ": "ND", "SOXL": "NY", "SQQQ": "ND"}

    def _get_exchange(self, symbol: str) -> str:
        return self.exchange_map.get(symbol.upper(), "ND")

    def _call_api(self, method, url, tr_id, params=None, data=None, extra_headers=None):
        max_retries = 3
        for attempt in range(max_retries):
            headers = kis_headers(tr_id, market="US")
            if not headers:
                logger.warning(f"⚠️ [US API] 헤더 생성 실패 (토큰 쿨다운 중). 5초 대기 후 재시도 ({attempt+1}/{max_retries})")
                time.sleep(5.0)
                continue

            if extra_headers:
                headers.update(extra_headers)

            try:
                res = requests.request(method, url, headers=headers, params=params, data=data, verify=False)
                
                # 토큰 만료 대응 (401 Unauthorized)
                if res.status_code == 401:
                    logger.warning(f"⚠️ [US API] 토큰 만료 감지. 재발급 및 재시도 ({attempt+1}/{max_retries})")
                    invalidate_access_token_controlled(market="US", account_no=self.account_no)
                    time.sleep(1.0)
                    continue
                
                # 서버 에러 대응 (500)
                if res.status_code == 500:
                    logger.warning(f"⚠️ [US API] Kiwoom 서버 에러(500). 1초 대기 후 재시도 ({attempt+1}/{max_retries})")
                    time.sleep(1.0)
                    continue
                return res
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ [US API] Network Error: {e}. Retrying ({attempt+1}/{max_retries})...")
                else:
                    logger.error(f"❌ [US API] Final failure after {max_retries} attempts: {e}")
                    raise e
                time.sleep(1.0)
        return res

    def _get_chart_data(self, symbol: str) -> Optional[List[dict]]:
        """usa06012 (미국주식 일 차트) API를 호출하여 일봉 데이터 리스트를 가져옵니다."""
        url = f"{self.base_url}/api/us/chart"
        # 시작일자를 오늘로부터 15일 전으로 세팅하여 충분한 데이터를 확보함
        start_date = (datetime.now() - timedelta(days=15)).strftime("%Y%m%d")
        body = {
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol,
            "strt_dt": start_date,
            "upd_stkpc_tp": "1",
            "exrt_appl_tp": "0"
        }
        res = self._call_api("POST", url, "usa06012", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                return data.get('result_list', [])
        return None

    def get_price(self, symbol: str) -> float:
        chart = self._get_chart_data(symbol)
        if chart:
            val = chart[0].get('cur_prc')
            if val is not None:
                return float(val)
        logger.error(f"[US] 현재가 조회 실패 ({symbol})")
        return 0.0

    def get_previous_close(self, symbol: str) -> float:
        chart = self._get_chart_data(symbol)
        if chart:
            # 첫 번째 항목이 오늘이고, 두 번째 항목이 전일일 수 있음
            today_str = datetime.now().strftime("%Y%m%d")
            valid_items = [item for item in chart if item.get('dt') != today_str]
            if valid_items:
                val = valid_items[0].get('cur_prc')
                if val is not None:
                    return float(val)
        logger.error(f"[US] 전일종가 조회 실패 ({symbol})")
        return 0.0

    def get_current_high(self, symbol: str) -> float:
        chart = self._get_chart_data(symbol)
        if chart:
            val = chart[0].get('high_pric')
            if val is not None:
                return float(val)
        return 0.0

    def get_current_low(self, symbol: str) -> float:
        chart = self._get_chart_data(symbol)
        if chart:
            val = chart[0].get('low_pric')
            if val is not None:
                return float(val)
        return 0.0

    def get_last_5_day_avg_close(self, symbol: str) -> float:
        chart = self._get_chart_data(symbol)
        if chart:
            today_str = datetime.now().strftime("%Y%m%d")
            valid_items = [item for item in chart if item.get('dt') != today_str]
            closes = [float(item['cur_prc']) for item in valid_items[:5] if item.get('cur_prc')]
            if len(closes) >= 5:
                return sum(closes) / 5.0
        logger.warning(f"[US] 5일 평균가 조회 실패 ({symbol})")
        return 0.0

    def get_exchange_rate(self) -> dict:
        """ust31301 (환율 조회) API 연동"""
        url = f"{self.base_url}/api/us/exchange"
        body = {
            "exch_tp": "2" # 2: 달러(USD) -> 원화(KRW) 환율
        }
        res = self._call_api("POST", url, "ust31301", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                rate = float(data.get('aplc_exrt', 0))
                # diff와 pct는 API 구조상 없을 수 있어 기본값 처리
                return {
                    "rate": rate,
                    "diff": 0.0,
                    "pct": 0.0
                }
        return {"rate": 0.0, "diff": 0.0, "pct": 0.0}

    def get_exchange_rate_history(self, start_date: str, end_date: str) -> List[dict]:
        # 환율 이력을 구하는 TR이 단일 시트에 없으므로 현재 환율을 활용하거나 기존 방식을 대체
        rate_info = self.get_exchange_rate()
        return [{"date": datetime.now().strftime("%Y%m%d"), "rate": rate_info["rate"]}]

    def get_account_equity(self, symbol: str) -> Tuple[float, float, float]:
        """ust21070 (미국주식 원장잔고확인) API 연동"""
        url = f"{self.base_url}/api/us/acnt"
        body = {
            "stex_tp": "",
            "stk_cd": symbol
        }
        try:
            res = self._call_api("POST", url, "ust21070", data=json.dumps(body))
            if not res:
                return 0.0, 0.0, 0.0
            data = res.json()
            if data.get('return_code') == 0:
                for item in data.get('result_list', []):
                    if item.get('stk_cd', '').strip().upper() == symbol.strip().upper():
                        return float(item.get('poss_qty', 0)), float(item.get('frgn_stk_book_uv', 0)), float(item.get('evlt_amt', 0))
        except Exception as e:
            logger.error(f"[US] 잔고 조회 중 오류 발생: {e}")
        return 0.0, 0.0, 0.0

    def get_cumulative_buy_amount(self, symbol: str) -> float:
        shares, avg_price, _ = self.get_account_equity(symbol)
        return shares * avg_price

    def get_cash_pool(self) -> float:
        """ust21160 (미국주식 예수금 상세) API 연동"""
        url = f"{self.base_url}/api/us/acnt"
        body = {}
        res = self._call_api("POST", url, "ust21160", data=json.dumps(body))
        if res:
            data = res.json()
            if data.get('return_code') == 0:
                # D2 외화예수금(USD) 반환
                val = data.get('d2_usd_fx_entr')
                if val is not None:
                    return float(val)
        logger.error("[US] 예수금 조회 실패")
        return 0.0

    def place_order(self, symbol: str, price: float, qty: float, order_type: Literal["BUY", "SELL"], price_type: str = "00", strategy: str = "MANUAL") -> bool:
        """
        [미국주식] 주문 전송
        price_type (frgn_trde_tp): 지정가: "00", 시장가: "03", LOC: "30" (키움증권 REST API 명세 기준)
        """
        action = "BUY" if order_type == "BUY" else "SELL"
        tr_id = "ust20000" if action == "BUY" else "ust20001"
        url = f"{self.base_url}/api/us/ordr"

        # KIS의 "00" 지정가, "01" 시장가, "34" LOC를 키움 규격인 "00", "03", "30"으로 보정
        if price_type in ["00", "0"]:
            frgn_trde_tp = "00"
            ord_uv = f"{price:.4f}"
        elif price_type in ["01", "3"]:
            frgn_trde_tp = "03"
            ord_uv = "0.0" # 시장가는 가격 0으로 제출
        elif price_type in ["34", "30"]:
            frgn_trde_tp = "30"
            ord_uv = f"{price:.4f}"
        else:
            frgn_trde_tp = "00"
            ord_uv = f"{price:.4f}"

        body = {
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol,
            "ord_qty": str(int(qty)),
            "ord_uv": ord_uv,
            "frgn_trde_tp": frgn_trde_tp
        }

        try:
            res = self._call_api("POST", url, tr_id, data=json.dumps(body))
            if not res:
                return False
            data = res.json()
            if data.get('return_code') == 0:
                odno = data.get('ord_no')
                logger.info(f"🟢 [US 주문 성공] {strategy} {action} {symbol} {qty}주 @ {price} (주문번호: {odno})")
                log_order_db(symbol, strategy, "US", action, price, qty, frgn_trde_tp, "ORDERED", odno, "성공", strategy)
                return True
            else:
                msg = data.get('return_msg', '알 수 없는 오류')
                logger.error(f"🔴 [US 주문 실패] {strategy} {action} {symbol} {qty}주 @ {price} -> {msg}")
                log_order_db(symbol, strategy, "US", action, price, qty, frgn_trde_tp, "FAILED", "", msg, strategy)
                send_telegram_message(f"🔴 <b>[US 주문 실패]</b>\n종목: {symbol}\n유형: {action}\n사유: {msg}")
                return False
        except Exception as e:
            logger.error(f"❌ [US 주문 예외 발생] {e}")
            return False

    def fetch_open_orders(self, symbol: str) -> List[dict]:
        """미체결 주문 조회 (TR: ust21510)"""
        url = f"{self.base_url}/api/us/acnt"
        body = {
            "slby_tp": "0", # 전체
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol
        }
        orders = []
        try:
            res = self._call_api("POST", url, "ust21510", data=json.dumps(body))
            if res:
                data = res.json()
                if data.get('return_code') == 0:
                    for item in data.get('result_list', []):
                        uncl_qty = float(item.get('ord_remnq', 0))
                        if uncl_qty > 0:
                            orders.append({
                                "odno": item.get('ord_no'),
                                "symbol": symbol,
                                "price": float(item.get('ord_uv', 0)),
                                "qty": float(item.get('ord_qty', 0)),
                                "uncl_qty": uncl_qty,
                                "side": "BUY" if item.get('slby_tp') == '2' else "SELL"
                            })
        except Exception as e:
            logger.error(f"[US] 미체결 조회 중 오류 발생: {e}")
        return orders

    def fetch_execution_history(self, symbol: str, start_date: str, end_date: str) -> List[dict]:
        """주문체결이력 조회 (TR: ust21510)"""
        url = f"{self.base_url}/api/us/acnt"
        body = {
            "slby_tp": "0",
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol
        }
        history = []
        try:
            res = self._call_api("POST", url, "ust21510", data=json.dumps(body))
            if res:
                data = res.json()
                if data.get('return_code') == 0:
                    for item in data.get('result_list', []):
                        cntr_qty = float(item.get('cntr_qty', 0))
                        if cntr_qty > 0:
                            history.append({
                                "odno": item.get('ord_no'),
                                "symbol": symbol,
                                "price": float(item.get('cntr_uv', 0)),
                                "qty": cntr_qty,
                                "side": "BUY" if item.get('slby_tp') == '2' else "SELL",
                                "time": item.get('ord_time', '')
                            })
        except Exception as e:
            logger.error(f"[US] 체결이력 조회 중 오류 발생: {e}")
        return history

    def fetch_daily_chart(self, symbol: str, days: int = 300) -> Optional[List[dict]]:
        """미국주식 일자별 시세 조회 (TR: usa06012)"""
        url = f"{self.base_url}/api/us/chart"
        all_rows = []
        next_key = ""
        start_date = (datetime.now() - timedelta(days=450)).strftime("%Y%m%d")
        
        for _ in range(5):
            if len(all_rows) >= days:
                break
                
            body = {
                "stex_tp": self._get_exchange(symbol),
                "stk_cd": symbol,
                "strt_dt": start_date,
                "upd_stkpc_tp": "1",
                "exrt_appl_tp": "0"
            }
            extra_headers = {}
            if next_key:
                extra_headers["next-key"] = next_key
                extra_headers["cont-yn"] = "Y"
                
            res = self._call_api("POST", url, "usa06012", data=json.dumps(body), extra_headers=extra_headers)
            if not res:
                break
            data = res.json()
            if data.get('return_code') != 0:
                break
                
            items = data.get('result_list', [])
            if not items:
                break
                
            for item in items:
                all_rows.append({
                    "Date": item.get('dt'),
                    "Open": float(item.get('open_pric', 0)),
                    "High": float(item.get('high_pric', 0)),
                    "Low": float(item.get('low_pric', 0)),
                    "Close": float(item.get('cur_prc', 0)),
                    "% change": f"{float(item.get('flu_rt', 0)):.2f}%",
                    "Volume": int(float(item.get('trde_qty', 0)))
                })
                
            cont_yn = res.headers.get("cont-yn", "N")
            next_key = res.headers.get("next-key", "")
            if cont_yn != "Y" or not next_key:
                break
                
        return all_rows[:days]
