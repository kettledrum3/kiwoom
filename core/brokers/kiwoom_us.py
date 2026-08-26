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
        self.trade_mode = trade_mode
        self._exchange_rate_cache = None
        
        # 키움용 거래소 맵 (NASDAQ: ND, NYSE: NY, AMEX: NA)
        self.exchange_map = {"TQQQ": "ND", "SOXL": "NY", "SQQQ": "ND"}
        self._chart_cache = {}
        self._prev_close_cache = {}

    def _get_exchange(self, symbol: str) -> str:
        return self.exchange_map.get(symbol.upper(), "ND")

    def _call_api(self, method, url, tr_id, params=None, data=None, extra_headers=None):
        res = None
        max_retries = 3
        for attempt in range(max_retries):
            headers = kis_headers(tr_id, market="US", trade_mode=self.trade_mode)
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
                    logger.warning(f"⚠️ [US API] 토큰 만료 감지 (401). 재발급 및 재시도 ({attempt+1}/{max_retries})")
                    invalidate_access_token_controlled(market="US", account_no=self.account_no, trade_mode=self.trade_mode)
                    time.sleep(1.0)
                    continue
                
                # 서버 에러 (500) 및 호출 제한 (429 Too Many Requests, 403 Forbidden Rate Limit)
                if res.status_code in [429, 403, 500]:
                    logger.warning(f"⚠️ [US API] Kiwoom 서버 일시 오류/호출제한 ({res.status_code}). 1.5초 대기 후 재시도 ({attempt+1}/{max_retries})")
                    time.sleep(1.5)
                    continue

                # 토큰 비즈니스 에러 대응 (200 OK 내 에러 메시지 감지)
                if res.status_code == 200:
                    try:
                        res_data = res.json()
                        rt_cd = res_data.get('return_code')
                        rt_msg = res_data.get('return_msg', '')
                        if rt_msg and any(x in rt_msg for x in ["Token", "token", "토큰", "투자구분"]):
                            logger.warning(f"⚠️ [US API] 토큰 오류 감지 ({rt_msg}). 토큰 무효화 후 재발급 재시도.")
                            invalidate_access_token_controlled(market="US", account_no=self.account_no, trade_mode=self.trade_mode)
                            time.sleep(1.0)
                            continue
                    except Exception:
                        pass
                return res
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ [US API] Network Error: {e}. Retrying ({attempt+1}/{max_retries})...")
                else:
                    logger.error(f"❌ [US API] Final failure after {max_retries} attempts: {e}")
                    raise e
                time.sleep(1.0)
        return res

    def _get_chart_data(self, symbol: str, force: bool = False) -> Optional[List[dict]]:
        """usa06012 (미국주식 일 차트) API를 호출하여 일봉 데이터 리스트를 가져옵니다."""
        # 1. 캐시 확인 (60초 이내 재호출 시 API 부하 방지용)
        now_ts = time.time()
        if not force and symbol in self._chart_cache:
            cache_ts, cache_data = self._chart_cache[symbol]
            if now_ts - cache_ts < 60.0:
                logger.debug(f"💾 [US Chart Cache Hit] {symbol} 일봉 차트 캐시 재사용")
                return cache_data

        url = f"{self.base_url}/api/us/chart"
        # 시작일자를 오늘 날짜로 설정하여 최신 데이터를 확보함
        start_date = datetime.now().strftime("%Y%m%d")
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
            if data.get('return_code') == 0 and data.get('result_list'):
                latest = data['result_list'][0]
                # logger.info(f"🔍 [US API Debug] usa06012 조회 성공 ({symbol}) - 최근영업일({latest.get('dt')}): 현재가 {latest.get('cur_prc')}$")
            else:
                logger.warning(f"🔍 [US API Debug] usa06012 응답 실패 ({symbol}): {data.get('return_msg')}")
            if data.get('return_code') == 0:
                result = data.get('result_list', [])
                # 캐시에 기록
                self._chart_cache[symbol] = (now_ts, result)
                return result
        return None

    def get_price(self, symbol: str, force: bool = False) -> float:
        chart = self._get_chart_data(symbol, force=force)
        if chart:
            val = chart[0].get('cur_prc')
            if val is not None:
                return float(val)
        logger.error(f"[US] 현재가 조회 실패 ({symbol})")
        return 0.0

    def get_previous_close(self, symbol: str) -> float:
        # 1. 메모리 캐시 확인 (오늘 날짜 기준으로 조회 기록이 있으면 API 호출 스킵)
        today_str = datetime.now().strftime("%Y%m%d")
        if hasattr(self, '_prev_close_cache') and symbol in self._prev_close_cache:
            cache_date, val = self._prev_close_cache[symbol]
            if cache_date == today_str:  # 당일(오늘) 내에는 캐시 재사용
                return val

        # 2. usa20100 (미국주식 현재가 상세) API를 이용해 단건으로 전일 종가 조회
        url = f"{self.base_url}/api/us/mrkcond"
        body = {
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol
        }
        try:
            res = self._call_api("POST", url, "usa20100", data=json.dumps(body))
            if res:
                data = res.json()
                val = data.get('base_close_pric')
                if val is not None:
                    logger.info(f"🔍 [US API Debug] usa20100 조회 성공 ({symbol}) - 전일종가: {val}$")
                    float_val = float(val)
                    # 캐시 갱신 (메모리 및 DB config)
                    self._prev_close_cache[symbol] = (today_str, float_val)
                    try:
                        from core.database import set_config
                        set_config(f"PREV_CLOSE_{symbol}", str(float_val))
                    except Exception:
                        pass
                    return float_val
        except Exception as e:
            logger.error(f"[US] usa20100 API 호출 중 예외 발생: {e}")
                    
        # API 조회 실패 시 DB에 캐싱된 전일 종가 정보 로드 복구 시도
        try:
            from core.database import get_config
            cached_val = get_config(f"PREV_CLOSE_{symbol}", "")
            if cached_val:
                db_val = float(cached_val)
                if db_val > 0:
                    logger.warning(f"⚠️ [US] {symbol} 전일종가 API 조회 실패. DB 캐싱 값({db_val:.2f}원)을 임시 복구하여 반환합니다.")
                    return db_val
        except Exception:
            pass

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

    def get_exchange_rate(self, force: bool = False) -> dict:
        """환율 조회 (키움 ust31301 API 우선 적용 및 Exchangerate.host API Fallback 이중화)"""
        import pytz
        from core.database import get_config, set_config, get_latest_exchange_rate_db
        
        # 1. 미국 동부 시각(America/New_York) 기준 오늘 날짜 획득
        ny_tz = pytz.timezone('America/New_York')
        today_str = datetime.now(ny_tz).strftime("%Y-%m-%d")
        
        # 0. 메모리 캐시 확인 (강제 조회가 아니고, 오늘 날짜 캐시가 존재하면 갱신 안 함)
        if not force and hasattr(self, '_exchange_rate_cache') and self._exchange_rate_cache:
            cache_date, cache_data = self._exchange_rate_cache
            if cache_date == today_str and cache_data.get("rate", 0) > 0:
                return cache_data

        # 0-1. DB 캐시 확인 (강제 조회가 아니고, 오늘 날짜로 DB에 저장된 환율이 존재하면 그것을 우선 사용)
        if not force:
            db_rate_str = get_config("USDKRW", "")
            db_rate_date = get_config("USDKRW_UPDATE_DATE", "")
            if db_rate_date == today_str and db_rate_str:
                try:
                    db_rate = float(db_rate_str)
                    if db_rate > 0:
                        logger.info(f"💵 [ExchangeRate] DB에 저장된 오늘 자 환율을 사용합니다: 1달러당 {db_rate:.2f}원")
                        res_dict = {
                            "rate": db_rate,
                            "diff": 0.0,
                            "pct": 0.0,
                            "source": "DB_CACHE"
                        }
                        self._exchange_rate_cache = (today_str, res_dict)
                        return res_dict
                except ValueError:
                    pass

        # 1순위: 키움증권 ust31301 API를 최우선으로 사용하여 환율 조회
        logger.info(f"[ExchangeRate] 키움증권 ust31301 API를 사용하여 환율을 조회합니다. (모드: {self.trade_mode})")
        try:
            url = f"{self.base_url}/api/us/exchange"
            body = {
                "exch_tp": "2" # 2: 달러(USD) -> 원화(KRW) 환율
            }
            res = self._call_api("POST", url, "ust31301", data=json.dumps(body))
            if res is not None:
                if res.status_code == 200:
                    data = res.json()
                    if data.get('return_code') == 0:
                        rate = float(data.get('aplc_exrt', 0))
                        if rate > 0:
                            logger.info(f"💵 [ExchangeRate] 키움증권 API 환율 조회 성공: 1달러당 {rate:.2f}원")
                            res_dict = {
                                "rate": rate,
                                "diff": 0.0,
                                "pct": 0.0,
                                "source": "KIWOOM"
                            }
                            self._exchange_rate_cache = (today_str, res_dict)
                            return res_dict
                        else:
                            logger.warning(f"⚠️ [ExchangeRate] 키움증권 API 응답에서 환율 값이 0 이하입니다: {data}")
                    else:
                        logger.warning(f"⚠️ [ExchangeRate] 키움증권 API 오류: [{data.get('return_code')}]({data.get('return_msg', '알 수 없는 오류')})")
                else:
                    logger.warning(f"⚠️ [ExchangeRate] 키움증권 API HTTP 에러 ({res.status_code}): {res.text}")
        except Exception as e:
            logger.warning(f"⚠️ [ExchangeRate] 키움증권 API 환율 조회 중 오류 발생: {e}")

        # 2순위 (Fallback): 키움증권 API 실패 시에만 외부 Exchangerate.host API 호출 시도
        ex_key = os.getenv("EXCHANGERATE_KEY", "").strip()
        if ex_key:
            try:
                call_date = get_config("EXCHANGERATE_CALL_DATE", "")
                try:
                    call_count = int(get_config("EXCHANGERATE_CALL_COUNT", "0"))
                except ValueError:
                    call_count = 0
                    
                if call_date != today_str:
                    call_count = 0
                    
                if call_count < 3:
                    api_url = f"https://api.exchangerate.host/live?access_key={ex_key}&symbols=KRW"
                    logger.info(f"[ExchangeRate] 키움 API 대체로 Exchangerate.host API를 시도합니다. (호출: {call_count + 1}/3)")
                    response = requests.get(api_url, timeout=5.0)
                    if response.status_code == 200:
                        res_data = response.json()
                        if res_data.get("success"):
                            quotes = res_data.get("quotes", {})
                            rate = float(quotes.get("USDKRW", 0.0))
                            if rate > 0:
                                set_config("EXCHANGERATE_CALL_DATE", today_str)
                                set_config("EXCHANGERATE_CALL_COUNT", str(call_count + 1))
                                logger.info(f"💵 [ExchangeRate] Exchangerate.host 최신 환율 조회 성공: 1달러당 {rate:.2f}원")
                                res_dict = {
                                    "rate": rate,
                                    "diff": 0.0,
                                    "pct": 0.0,
                                    "source": "EXCHANGERATE_HOST"
                                }
                                self._exchange_rate_cache = (today_str, res_dict)
                                return res_dict
            except Exception as e:
                logger.warning(f"⚠️ [ExchangeRate] Exchangerate.host Fallback 호출 실패: {e}")

        # 3순위: 최근 DB 저장 환율 반환
        latest_record = get_latest_exchange_rate_db()
        if latest_record and latest_record.get("rate", 0) > 0:
            db_rate = latest_record["rate"]
            logger.info(f"💵 [ExchangeRate] API 호출 실패로 DB 최근 환율을 사용합니다: 1달러당 {db_rate:.2f}원 (기준일: {latest_record.get('trade_date')})")
            res_dict = {
                "rate": db_rate,
                "diff": latest_record.get("diff", 0.0),
                "pct": latest_record.get("pct", 0.0),
                "source": "DB_FALLBACK"
            }
            self._exchange_rate_cache = (today_str, res_dict)
            return res_dict

        res_dict = {"rate": 0.0, "diff": 0.0, "pct": 0.0, "source": "NONE"}
        self._exchange_rate_cache = (today_str, res_dict)
        return res_dict

    def get_exchange_rate_history(self, start_date: str = "", end_date: str = "") -> List[dict]:
        """DB에 저장된 미국 정규장 개장 기준 일별 환율 이력 반환"""
        from core.database import get_exchange_rate_history_db
        db_history = get_exchange_rate_history_db(days=90)
        if db_history:
            return db_history
        # DB에 이력이 없으면 현재 환율로 1건 생성
        rate_info = self.get_exchange_rate()
        return [{
            "trade_date": datetime.now().strftime("%Y-%m-%d"),
            "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rate": rate_info["rate"],
            "base_rate": rate_info["rate"],
            "diff": 0.0,
            "pct": 0.0,
            "source": rate_info.get("source", "KIWOOM")
        }]

    def get_account_equity(self, symbol: str) -> Optional[Tuple[float, float, float]]:
        """ust21070 (미국주식 원장잔고확인) API 연동"""
        url = f"{self.base_url}/api/us/acnt"
        body = {
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol
        }
        try:
            res = self._call_api("POST", url, "ust21070", data=json.dumps(body))
            if not res:
                logger.error("[US] 잔고 조회 API 응답 없음")
                return None
            data = res.json()
            if data.get('return_code') == 0:
                res_list = data.get('result_list', [])
                # logger.info(f"🔍 [US API Debug] ust21070 조회 성공 - 보유 종목 수: {len(res_list)}개")
                for item in res_list:
                    if item.get('stk_cd', '').strip().upper() == symbol.strip().upper():
                        poss_qty_val = int(float(item.get('poss_qty', 0)))
                        # logger.info(f"   -> {symbol} 발견: 수량 {poss_qty_val}주, 평단가 {item.get('frgn_stk_book_uv')}$, 평가금액 {item.get('evlt_amt')}$")
                        return float(item.get('poss_qty', 0)), float(item.get('frgn_stk_book_uv', 0)), float(item.get('evlt_amt', 0))
                # 결과 리스트에 종목이 없으면 보유 수량 0
                return 0.0, 0.0, 0.0
            else:
                logger.warning(f"🔍 [US API Debug] ust21070 응답 실패: {data.get('return_msg')}")
                return None
        except Exception as e:
            logger.error(f"[US] 잔고 조회 중 오류 발생: {e}")
            return None

    def get_cumulative_buy_amount(self, symbol: str) -> float:
        res = self.get_account_equity(symbol)
        if res is None:
            return 0.0
        shares, avg_price, _ = res
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

    def place_order(self, symbol: str, price: float, qty: float, order_type: Literal["BUY", "SELL"], price_type: str = "00", strategy: str = "MANUAL", strategy_name: str = "", stop_price: Optional[float] = None) -> bool:
        """
        [미국주식] 주문 전송
        매매구분(trde_tp): 00:지정가, 03:시장가, 26:VWAP지정가, 27:TWAP지정가, 30:LOC, 33:MOC, 36:VWAP시장가, 37:TWAP시장가, 35:STOP, 34:STOP LIMIT
        """
        logger.info(f"🔍 [US API Debug] place_order 호출: symbol={symbol}, price={price}, qty={qty}, order_type={order_type}, price_type={price_type}, strategy={strategy}, strategy_name={strategy_name}, stop_price={stop_price}")

        # 모의투자(MOCK) 모드이고 시장가 주문이 요청된 경우, 현재가 기준으로 지정가 호가 보정 우회 처리
        if self.trade_mode == "MOCK" and price_type in ["03", "36", "37"]:
            current_price = self.get_price(symbol)
            if current_price > 0:
                tick_diff = 0.01 if order_type == "BUY" else -0.01
                price = current_price + tick_diff
                price = self.adjust_price_by_tick(symbol, price, order_type)
                price_type = "00"
                logger.info(f"🔄 [MOCK US 시장가 우회] 시장가 주문을 지정가 {price:.2f}로 변환하여 제출합니다. ({symbol})")
            else:
                logger.error(f"❌ [MOCK US 시장가 우회 실패] 현재가를 조회할 수 없어 주문을 진행하지 않습니다. ({symbol})")
                return False

        action = "BUY" if order_type == "BUY" else "SELL"
        tr_id = "ust20000" if action == "BUY" else "ust20001"
        url = f"{self.base_url}/api/us/ordr"

        # 미국주식 단가는 $1 미만 소수점 4자리, $1 이상 소수점 2자리까지만 입력 가능함
        def format_price(p: float) -> str:
            if p < 1.0:
                return f"{p:.4f}"
            else:
                return f"{p:.2f}"

        # 해외매매구분 처리
        trde_tp = price_type

        # [MOCK US LOC 모사] 모의투자 모드이고 LOC("30") 주문일 경우 지정가("00") 주문으로 우회 변환하여 마감 20분 전에 제출되도록 함
        if self.trade_mode == "MOCK" and trde_tp == "30":
            trde_tp = "00"
            logger.info(f"🔄 [MOCK US LOC 모사] 모의투자 계좌의 LOC 주문을 지정가 {price:.2f}로 변환하여 전송합니다. ({symbol})")

        # 시장가 및 STOP 유형은 가격을 0.0으로 제출
        if trde_tp in ["03", "36", "37", "35"]:
            ord_uv = "0.0"
        else:
            ord_uv = format_price(price)

        body = {
            "stex_tp": self._get_exchange(symbol),
            "stk_cd": symbol,
            "ord_qty": str(int(qty)),
            "ord_uv": ord_uv,
            "trde_tp": trde_tp
        }

        if action == "SELL":
            formatted_stop_price = ""
            if stop_price is not None:
                formatted_stop_price = format_price(stop_price)
            elif trde_tp in ["34", "35"]:
                formatted_stop_price = format_price(price)
            body["stop_pric"] = formatted_stop_price

        logger.info(f"🔍 [US API Debug] 주문 요청 전송 준비: URL={url}, TR_ID={tr_id}, Body={json.dumps(body)}")

        try:
            res = self._call_api("POST", url, tr_id, data=json.dumps(body))
            if res is None:
                logger.error(f"❌ [US API Debug] API 호출 결과가 None입니다. (네트워크/인증 오류 가능성)")
                return False
            
            logger.info(f"🔍 [US API Debug] API 응답 코드: {res.status_code}, 본문: {res.text}")
            
            if res.status_code != 200:
                logger.error(f"🔴 [US 주문 HTTP 에러] {strategy} {action} {symbol} {qty}주 @ {price} -> HTTP {res.status_code}: {res.text}")
                log_order_db(symbol, strategy, action, price, qty, trde_tp, "FAILED", "", f"HTTP {res.status_code}", market="US", strategy_name=strategy_name)
                send_telegram_message(f"🔴 <b>[US 주문 HTTP 에러]</b>\n종목: {symbol}\n유형: {action}\n사유: HTTP {res.status_code}")
                return False

            data = res.json()
            if data.get('return_code') == 0:
                odno = data.get('ord_no')
                logger.info(f"🟢 [US 주문 성공] {strategy} {action} {symbol} {qty}주 @ {price} (주문번호: {odno})")
                log_order_db(symbol, strategy, action, price, qty, trde_tp, "ORDERED", odno, "성공", market="US", strategy_name=strategy_name)
                return True
            else:
                msg = data.get('return_msg', '알 수 없는 오류')
                logger.error(f"🔴 [US 주문 실패] {strategy} {action} {symbol} {qty}주 @ {price} -> {msg}")
                log_order_db(symbol, strategy, action, price, qty, trde_tp, "FAILED", "", msg, market="US", strategy_name=strategy_name)
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
        # 시작일자를 오늘 날짜로 설정하여 오늘부터 과거로 데이터를 수집함
        start_date = datetime.now().strftime("%Y%m%d")
        
        # [FIX] days 기간에 따라 연속 조회(Pagination) 루프 횟수를 동적으로 계산
        max_loops = max(5, (days // 15) + 2)
        
        for _ in range(max_loops):
            if len(all_rows) >= days:
                break
                
            # [ADD] 과도한 API 호출로 인한 서버 차단 방지용 짧은 딜레이 추가
            time.sleep(1.0)
                
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
