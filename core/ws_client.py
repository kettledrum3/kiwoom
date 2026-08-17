import asyncio
import websockets
import json
import os
import time
import logging
import pytz
import random
import sys
import threading
from datetime import datetime, timedelta, time as dtime
import math

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cavr import get_access_token, CAState, VRState, format_symbol_display, CAConfig, CostAveragingEngine
from core.database import load_state_db, save_state_db, log_trade_db, delete_order_by_odno_db, get_all_states_db, get_config
from core.notifier import send_telegram_message

# Exponential backoff constants
BASE_RECONNECT_DELAY = 5  # seconds
MAX_RECONNECT_DELAY = 300 # seconds (5 minutes)

# Kiwoom 주문 유형 매핑
ORDER_TYPE_MAP = {
    # 미국주식 (ust20000/ust20001)
    "00": "지정가",
    "03": "시장가",
    "26": "VWAP지정가",
    "27": "TWAP지정가",
    "30": "LOC / 중간가(IOC)",
    "33": "MOC",
    "36": "VWAP시장가",
    "37": "TWAP시장가",
    "35": "STOP",
    "34": "STOP LIMIT",

    # 국내주식 (kt10000/kt10001)
    "0": "보통",
    "3": "시장가",
    "5": "조건부지정가",
    "81": "장마감후시간외",
    "61": "장시작전시간외",
    "62": "시간외단일가",
    "6": "최유리지정가",
    "7": "최우선지정가",
    "10": "보통(IOC)",
    "13": "시장가(IOC)",
    "16": "최유리(IOC)",
    "20": "보통(FOK)",
    "23": "시장가(FOK)",
    "26": "최유리(FOK)",
    "28": "스톱지정가",
    "29": "중간가",
    "31": "중간가(FOK)",
}

logger = logging.getLogger(__name__)

class KisWebSocketClient:
    """
    키움증권 REST 웹소켓 클라이언트 (KIS와 동일한 인터페이스 유지)
    """
    def __init__(self, market: str = "US"):
        self.market = market.upper()
        
        # 1. 공통 환경 변수(.env) 로드
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        common_env_path = os.path.join(project_root, "env", ".env")
        from dotenv import load_dotenv
        if os.path.exists(common_env_path):
            load_dotenv(common_env_path, override=True)

        # 2. 시장별 환경변수 로드 및 병합 (override)
        env_suffix = "kr" if self.market == "KR" else "us"
        env_path = os.path.join(project_root, "env", f".env.{env_suffix}")
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)

        # 3. 거래 모드(REAL vs MOCK) 판별 및 변수 설정
        from core.database import get_trade_mode
        self.trade_mode = get_trade_mode()

        if self.trade_mode == "MOCK":
            prefix = "MOCKKR_" if self.market == "KR" else "MOCKUS_"
            self.hts_id = os.getenv(f"{prefix}CLIENT_ID", "").strip()
            self.ws_url = os.getenv("MOCK_SOCKET_URL", "wss://mockapi.kiwoom.com:10000").strip()
            self.account_no = os.getenv(f"{prefix}ACCOUNT_NO", "").strip()
        else:
            self.hts_id = os.getenv("KIWOOM_CLIENT_ID", "").strip()
            self.ws_url = os.getenv("KIWOOM_SOCKET_URL", "wss://api.kiwoom.com:10000").strip()
            self.account_no = os.getenv("KIWOOM_ACCOUNT_NO", "").strip()

        # 웹소켓 URI 경로 자동 추가
        ws_path = "/api/dostk/websocket" if self.market == "KR" else "/api/us/websocket"
        if not self.ws_url.endswith(ws_path):
            self.ws_url = self.ws_url.rstrip('/') + ws_path

        self._broker = None
            
        self.approval_key = None
        self.running = False
        self.retry_attempts = 0
        self._websocket = None
        self.ping_task = None
        self._force_token_renew = False
        self._prev_close_cache = {}
        self._last_db_update = {}
        self._last_cache_date = None
        self.tz = pytz.timezone('Asia/Seoul' if self.market == "KR" else 'America/New_York')
        self._cache_lock = threading.Lock()
        self.is_subscribed_prices = False

    async def connect(self):
        """웹소켓 연결 및 데이터 수신 메인 루프"""
        self.running = True
        connection_start_time = 0

        while self.running:
            try:
                # 1. 거래 모드(REAL vs MOCK) 동적 갱신
                from core.database import get_trade_mode
                self.trade_mode = get_trade_mode()
                
                # 시장별 환경 변수 재설정 (모드 변경 대비)
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                env_suffix = "kr" if self.market == "KR" else "us"
                env_path = os.path.join(project_root, "env", f".env.{env_suffix}")
                if os.path.exists(env_path):
                    from dotenv import load_dotenv
                    load_dotenv(env_path, override=True)
                    
                if self.trade_mode == "MOCK":
                    prefix = "MOCKKR_" if self.market == "KR" else "MOCKUS_"
                    self.hts_id = os.getenv(f"{prefix}CLIENT_ID", "").strip()
                    self.ws_url = os.getenv("MOCK_SOCKET_URL", "wss://mockapi.kiwoom.com:10000").strip()
                    self.account_no = os.getenv(f"{prefix}ACCOUNT_NO", "").strip()
                else:
                    self.hts_id = os.getenv("KIWOOM_CLIENT_ID", "").strip()
                    self.ws_url = os.getenv("KIWOOM_SOCKET_URL", "wss://api.kiwoom.com:10000").strip()
                    self.account_no = os.getenv("KIWOOM_ACCOUNT_NO", "").strip()

                ws_path = "/api/dostk/websocket" if self.market == "KR" else "/api/us/websocket"
                if not self.ws_url.endswith(ws_path):
                    self.ws_url = self.ws_url.rstrip('/') + ws_path

                # 시장별 타임존 및 운영 시간 설정 동적 업데이트
                if self.market == "KR":
                    market_tz = pytz.timezone('Asia/Seoul')
                    if self.trade_mode == "MOCK":
                        open_time = dtime(9, 0)
                        close_time = dtime(15, 30)
                    else:
                        open_time = dtime(9, 0)
                        close_time = dtime(15, 50)
                else: # US Market
                    market_tz = pytz.timezone('America/New_York')
                    if self.trade_mode == "MOCK":
                        open_time = dtime(9, 30)
                        close_time = dtime(16, 0)
                    else:
                        open_time = dtime(7, 0)
                        close_time = dtime(18, 0)

                if self.retry_attempts == 0:
                    await asyncio.sleep(2)

                now_in_market_tz = datetime.now(market_tz)
                is_weekend = now_in_market_tz.weekday() >= 5
                
                is_holiday = False
                if self.market == "KR":
                    is_holiday = get_config("kr_market_opnd_yn") == "N"
                elif self.market == "US":
                    is_holiday = get_config("us_market_opnd_yn") == "N"

                if is_weekend:
                    next_check = (now_in_market_tz + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
                    sleep_seconds = (next_check - now_in_market_tz).total_seconds()
                    logger.info(f"📅 [WS] 오늘은 {self.market} 시장 주말입니다. 현지 시간 내일 오전 8시까지 대기합니다.")
                    await asyncio.sleep(sleep_seconds)
                    continue
                
                if is_holiday:
                    next_check = (now_in_market_tz + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
                    sleep_seconds = (next_check - now_in_market_tz).total_seconds()
                    logger.info(f"📅 [WS] 오늘은 {self.market} 시장 휴장일(DB 설정)입니다. 현지 시간 내일 오전 8시까지 대기합니다.")
                    await asyncio.sleep(sleep_seconds)
                    continue

                is_active_time = open_time <= now_in_market_tz.time() <= close_time
                if not is_active_time:
                    now_time = now_in_market_tz.time()
                    current_date = now_in_market_tz.date()
                    
                    next_open_dt = None
                    if now_time < open_time:
                        next_open_dt = market_tz.localize(datetime.combine(current_date, open_time))
                    else:
                        next_open_dt = market_tz.localize(datetime.combine(current_date + timedelta(days=1), open_time))
                        while next_open_dt.weekday() >= 5:
                            next_open_dt += timedelta(days=1)
                    
                    sleep_seconds = (next_open_dt - now_in_market_tz).total_seconds()
                    
                    if sleep_seconds > 4 * 3600:
                        actual_sleep = 4 * 3600
                        log_msg = f"[WS] {self.market} 시장 운영 시간 외입니다. 4시간 후 재확인합니다."
                    elif sleep_seconds > 3600:
                        actual_sleep = 3600
                        log_msg = f"[WS] {self.market} 시장 운영 시간 외입니다. 1시간 후 재확인합니다."
                    elif sleep_seconds > 600:
                        actual_sleep = 600
                        log_msg = f"[WS] {self.market} 시장 운영 시간 외입니다. 10분 후 재확인합니다."
                    else:
                        actual_sleep = max(60, sleep_seconds)
                        log_msg = f"[WS] {self.market} 시장 운영 시간 외입니다. {int(actual_sleep/60)}분 후 재확인합니다."
                    
                    logger.info(log_msg)
                    await asyncio.sleep(actual_sleep)
                    continue

                # 만약 기존 브로커가 있고, 그 브로커의 trade_mode가 현재 self.trade_mode와 다르다면 브로커 재생성
                if self._broker is not None and getattr(self._broker, 'trade_mode', None) != self.trade_mode:
                    logger.info(f"🔄 [WS] {self.market} 거래 모드 변경 감지 ({self._broker.trade_mode} -> {self.trade_mode}). 브로커를 재구성합니다.")
                    self._broker = None

                if self._broker is None:
                    from core.brokers.kiwoom_kr import KiwoomKrBroker
                    from core.brokers.kiwoom_us import KiwoomUsBroker
                    self._broker = KiwoomKrBroker() if self.market == "KR" else KiwoomUsBroker()
                    logger.info(f"🚀 [WS] {self.market} 실시간 감시를 위한 브로커를 시작합니다.")

                # 키움증권은 웹소켓 승인키로 접근 토큰을 그대로 사용함
                self.approval_key = get_access_token(self.market, force=self._force_token_renew, trade_mode=self.trade_mode)
                if self._force_token_renew:
                    self._force_token_renew = False # 리셋
                if not self.approval_key:
                    logger.error(f"[WS] {self.market} Access Token(웹소켓용) 획득 실패. 1분 후 재시도.")
                    await asyncio.sleep(60)
                    continue

                headers = {
                    "authorization": f"Bearer {self.approval_key}"
                }
                
                import inspect
                sig = inspect.signature(websockets.connect)
                connect_kwargs = {"ping_interval": None, "close_timeout": 10}
                if "additional_headers" in sig.parameters:
                    connect_kwargs["additional_headers"] = headers
                else:
                    connect_kwargs["extra_headers"] = headers

                logger.info(f"[WS] {self.market} 웹소켓 연결 시도 중... (URL: {self.ws_url})")
                async with websockets.connect(self.ws_url, **connect_kwargs) as websocket:
                    self._websocket = websocket
                    self.is_subscribed_prices = False # 실시간 시세 구독 여부 플래그 초기화
                    connection_start_time = time.time()
                    logger.info(f"✅ [WS] {self.market} 웹소켓 서버에 연결되었습니다.")
                    
                    # 클라이언트 주도 PING 루프 시작 (키움 규격에 맞춤)
                    self.ping_task = asyncio.create_task(self._ping_loop(websocket))
                    
                    # 로그인 인증 요청 전송 (LOGIN)
                    login_data = {
                        "trnm": "LOGIN",
                        "token": self.approval_key
                    }
                    await websocket.send(json.dumps(login_data))
                    logger.info(f"[WS] {self.market} 로그인 인증 요청 전송")

                    # 메시지 수신 루프
                    while self.running:
                        try:
                            # 거래 모드 및 계좌 번호 동적 변경 체크
                            from core.database import get_trade_mode
                            current_mode = get_trade_mode()
                            
                            # 환경 변수 재로드 후 계좌 번호 확인
                            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                            env_suffix = "kr" if self.market == "KR" else "us"
                            env_path = os.path.join(project_root, "env", f".env.{env_suffix}")
                            if os.path.exists(env_path):
                                from dotenv import load_dotenv
                                load_dotenv(env_path, override=True)
                                
                            if current_mode == "MOCK":
                                prefix = "MOCKKR_" if self.market == "KR" else "MOCKUS_"
                                current_account = os.getenv(f"{prefix}ACCOUNT_NO", "").strip()
                            else:
                                current_account = os.getenv("KIWOOM_ACCOUNT_NO", "").strip()
                                
                            if current_mode != self.trade_mode or current_account != self.account_no:
                                logger.info(
                                    f"🔄 [WS] {self.market} 거래 모드 또는 계좌 번호 변경 감지 "
                                    f"(Mode: {self.trade_mode} -> {current_mode}, Account: {self.account_no} -> {current_account}). "
                                    f"웹소켓 연결을 종료하고 재접속합니다."
                                )
                                self.trade_mode = current_mode
                                self.account_no = current_account
                                break

                            now_time = datetime.now(market_tz).time()
                            if not (open_time <= now_time <= close_time):
                                logger.info(f"⏰ [WS] {self.market} 정규장 운영 시간 종료. 연결을 해제합니다.")
                                break

                            msg = await asyncio.wait_for(websocket.recv(), timeout=30)
                            logger.debug(f"[WS] {self.market} Received raw message: {msg[:100]}...")
                            await self.on_message(msg)
                        except asyncio.TimeoutError:
                            continue
                        except websockets.ConnectionClosed as e:
                            now_in_market_tz = datetime.now(market_tz)
                            if not (open_time <= now_in_market_tz.time() <= close_time):
                                logger.info(f"⏰ [WS] {self.market} 정규장 운영 시간 종료 후 연결 끊김.")
                                self.running = False
                                break
                            raise e
                        
                        await asyncio.sleep(0.1)

            except Exception as e:
                self._stop_ping_loop()
                duration = time.time() - connection_start_time
                if duration > 300:
                    self.retry_attempts = 1
                else:
                    self.retry_attempts += 1

                delay = min(MAX_RECONNECT_DELAY, BASE_RECONNECT_DELAY * (2 ** (self.retry_attempts - 1)))
                jitter = random.uniform(0.8, 1.2)
                wait_time = delay * jitter

                if self.retry_attempts >= 2:
                    wait_time = max(60, wait_time)
                    logger.warning(f"⚠️ [WS] {self.market} 빈번한 연결 끊김 감지. {wait_time:.0f}초간 대기 후 재시도합니다.")

                if self.retry_attempts <= 3 or self.retry_attempts % 5 == 0:
                    send_telegram_message(f"⚠️ <b>[WS 재연결 경고]</b> {self.market} 웹소켓 연결 실패 ({self.retry_attempts}회).\n사유: {type(e).__name__}\n{wait_time:.0f}초 후 재시도.")
                
                logger.error(f"[WS] {self.market} 연결 오류 발생 ({self.retry_attempts}회): {e}. {wait_time:.0f}초 후 재시도.")
                await asyncio.sleep(wait_time)

        self._stop_ping_loop()

    async def _ping_loop(self, websocket):
        """클라이언트 PINGPONG 루프 (키움 REST 웹소켓 규격)"""
        logger.info(f"[WS] {self.market} 클라이언트 PING 루프를 시작합니다.")
        try:
            while self.running:
                await asyncio.sleep(120)  # 2분 간격
                is_open = False
                if hasattr(websocket, 'open'):
                    is_open = websocket.open
                elif hasattr(websocket, 'closed'):
                    is_open = not websocket.closed
                else:
                    is_open = True
                if is_open:
                    ping_msg = {
                        "trnm": "PING",
                        "header": {
                            "api-id": "PINGPONG",
                            "authorization": f"Bearer {self.approval_key}"
                        }
                    }
                    logger.debug(f"[WS] {self.market} Sending client-initiated PING...")
                    await websocket.send(json.dumps(ping_msg))
        except asyncio.CancelledError:
            logger.info(f"[WS] {self.market} PING 루프가 취소되었습니다.")
        except Exception as e:
            logger.error(f"[WS] {self.market} PING 루프 오류 발생: {e}")

    def _stop_ping_loop(self):
        if hasattr(self, 'ping_task') and self.ping_task and not self.ping_task.done():
            self.ping_task.cancel()
            logger.info(f"[WS] {self.market} 기존 PING 루프 취소 요청 완료.")

    async def subscribe(self, websocket):
        """체결 통보 구독 요청 (00 또는 F5)"""
        api_id = "00" if self.market == "KR" else "F5"
        
        # 미국 시장(F5)인 경우, 규격상 리스트 내 맵 구조 문자열을 사용해야 파싱 실패 및 100013 에러를 예방할 수 있음
        if self.market == "US":
            items = [{"jmcode": "TQQQ", "stex_tp": "ND"}]
            item_list = [json.dumps(items)]
        else:
            item_list = [""]
            
        payload = {
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [
                {
                    "item": item_list,
                    "type": [api_id]
                }
            ]
        }
        send_data = json.dumps(payload)
        logger.info(f"[WS] {self.market} 체결 통보 구독 요청 전송 전문: {send_data}")
        await websocket.send(send_data)

    async def subscribe_prices(self, websocket):
        """실시간 시세 구독 요청 (0B 또는 FE)"""
        api_id = "0B" if self.market == "KR" else "FE"
        all_states = get_all_states_db(market=self.market)
        active_symbols = set(s['symbol'] for s in all_states if s.get('is_active', True))
        
        if not active_symbols:
            default_ticker = os.getenv("ticker", "").strip().upper()
            if default_ticker:
                active_symbols.add(default_ticker)
            if self.market == "KR":
                active_symbols.update(["122630", "005930"])
            else:
                active_symbols.update(["SOXL", "TQQQ"])
            logger.info(f"[WS] 설정된 활성 전략이 없습니다. 기본 종목을 구독합니다: {active_symbols}")
        
        for symbol in active_symbols:
            if self.market == "US":
                stex_tp = "ND"
                if self._broker and hasattr(self._broker, '_get_exchange'):
                    stex_tp = self._broker._get_exchange(symbol)
                item_list = [json.dumps([{"jmcode": symbol, "stex_tp": stex_tp}])]
            else:
                item_list = [symbol]

            payload = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": item_list,
                        "type": [api_id]
                    }
                ]
            }
            send_data = json.dumps(payload)
            logger.info(f"[WS] {self.market} {symbol} 실시간 시세 구독 요청 전송 전문: {send_data}")
            await websocket.send(send_data)
            await asyncio.sleep(0.1)

    async def on_message(self, message):
        """수신된 JSON 메시지 처리"""
        try:
            data = json.loads(message)
            header = data.get('header', {})
            
            # PINGPONG 응답 처리
            if header.get('api-id') == 'PINGPONG':
                logger.debug(f"[WS] {self.market} PINGPONG Echo received.")
                return

            trnm = data.get('trnm')
            # 서버 주도 PING에 대한 PONG Echo 처리 (R10002 오류 해결)
            if trnm == "PING":
                logger.debug(f"[WS] {self.market} Server PING received. Echoing back.")
                if self._websocket:
                    await self._websocket.send(message)
                return

            # Control Message 수신 기록
            if trnm != "REAL":
                logger.info(f"[WS] {self.market} Control Message received: {message}")
                
                # 로그인 세션 불일치/부재 오류 처리 (예: return_code == 100013, 100018, 100004)
                ret_code = data.get('return_code')
                if ret_code in [100013, 100018, 100004, "100013", "100018", "100004"]:
                    logger.warning(f"⚠️ [WS] {self.market} 로그인 세션/인증 오류 감지 (코드: {ret_code}). 토큰을 강제 재발급하며 재연결을 대기합니다.")
                    self._force_token_renew = True
                    if self._websocket:
                        await self._websocket.close()
                    return

                # 로그인 인증 전문(LOGIN)에 대한 결과 처리
                if trnm == "LOGIN":
                    if ret_code in [0, "0", "000000", None]:
                        logger.info(f"🔑 [WS] {self.market} 로그인 인증 성공. 체결 통보 구독을 진행합니다.")
                        asyncio.create_task(self.subscribe(self._websocket))
                    else:
                        logger.error(f"❌ [WS] {self.market} 로그인 인증 실패 (코드: {ret_code}, 메시지: {data.get('return_msg')}).")
                        self._force_token_renew = True
                        if self._websocket:
                            await self._websocket.close()
                    return

                # 로그인 인증(체결 통보 등록 완료) 성공 시 실시간 시세 구독 트리거
                msg_api_id = header.get('api-id')
                target_api_id = "00" if self.market == "KR" else "F5"
                if trnm == "REG" and (msg_api_id == target_api_id or msg_api_id is None):
                    if ret_code in [105101, "105101"]:
                        logger.warning(
                            f"❌ [WS] {self.market} 구독 실패 (105101: 전문 변환 실패). "
                            f"보낸 구독 전문의 규격이나 타입 설정을 다시 확인해야 합니다. 수신 전문: {message}"
                        )
                    
                    if ret_code in [0, "0", "000000", None] and not self.is_subscribed_prices:
                        logger.info(f"🔑 [WS] {self.market} 로그인 인증(체결 통보 등록) 확인 성공. 실시간 시세 구독을 진행합니다.")
                        self.is_subscribed_prices = True
                        asyncio.create_task(self.subscribe_prices(self._websocket))
                return

            # 실시간 데이터 파싱 (trnm == "REAL")
            real_data_list = data.get('data', [])
            for item in real_data_list:
                item_type = item.get('type')
                
                # 1. 체결 데이터 처리 (00 또는 F5)
                if item_type in ["00", "F5"]:
                    asyncio.create_task(asyncio.to_thread(self.parse_execution_data, item))
                
                # 2. 시세 데이터 처리 (0B 또는 FE)
                elif item_type in ["0B", "FE"]:
                    asyncio.create_task(asyncio.to_thread(self.handle_realtime_price, item))

        except Exception as e:
            logger.error(f"[WS] 메시지 디코딩/처리 오류: {e} | 원본: {message[:150]}")

    def handle_realtime_price(self, item):
        """실시간 시세를 이용한 장중 급락 감시 로직"""
        try:
            symbol = item.get('item')
            values = item.get('values', {})
            
            # FID 10: 현재가 (부호 포함)
            raw_price = values.get('10')
            if not raw_price: return
            
            current_price = abs(float(raw_price))
            if current_price <= 0: return

            # 날짜 변경 시 캐시 초기화
            today = datetime.now(self.tz).date()
            if self._last_cache_date != today:
                self._prev_close_cache.clear()
                self._last_cache_date = today

            # 전일종가 캐싱
            cache_key = f"{self.market}_{symbol}"
            with self._cache_lock:
                if cache_key not in self._prev_close_cache:
                    try:
                        pc = self._broker.get_previous_close(symbol)
                        self._prev_close_cache[cache_key] = pc if pc and pc > 0 else 0.01
                        logger.info(f"[WS] Cached prev_close for {cache_key}: {self._prev_close_cache[cache_key]}")
                    except Exception as e:
                        logger.error(f"[WS] 전일종가 조회 실패 ({cache_key}): {e}")
                        self._prev_close_cache[cache_key] = 0.01

            # 상태 업데이트 및 장중 급락 점검
            target_states = get_all_states_db(symbol=symbol, market=self.market)
            
            for state_data in target_states:
                if not state_data.get('is_active', True): continue
                
                stype = state_data.get('strategy_type')
                alias = state_data.get('strategy_name', '')
                update_key = (stype, symbol, alias)
                now = time.time()
                
                # DB 저장 쓰로틀링 (10초)
                should_save = (now - self._last_db_update.get(update_key, 0)) > 10
                state_data.pop('updated_at', None)

                if stype == "CA":
                    config = CAConfig(symbol=symbol, use_db=True, market=self.market, strategy_name=alias)
                    engine = CostAveragingEngine(config, broker=self._broker)
                    engine.run_intraday_check(current_price=current_price, prev_close=self._prev_close_cache.get(cache_key))
                    target_state = engine.state
                elif stype == "VR":
                    target_state = VRState(**state_data)

                if should_save:
                    target_state.current_price = current_price
                    save_state_db(target_state, market=self.market, strategy_name=alias, only_if_exists=True)
                    self._last_db_update[update_key] = now

        except Exception as e:
            logger.error(f"[WS] 실시간 시세 처리 오류: {e}")

    def parse_execution_data(self, item):
        """체결 통보 데이터 파싱 (JSON 포맷)"""
        try:
            symbol = item.get('item', '').strip().upper()
            values = item.get('values', {})
            
            # FID 파싱
            odno = str(values.get('9203'))
            status_text = values.get('913') # 접수, 체결, 취소 등
            
            # 체결 단계일 때는 체결량(911)을 사용하고, 접수 등 비체결 단계일 때는 주문수량(900)을 사용
            cntg_div = "02" if "체결" in status_text else "01"
            if cntg_div == "02":
                exec_qty_str = values.get('911')
            else:
                exec_qty_str = values.get('900') or values.get('911')
                
            # 체결 단계일 때는 체결단가(910)를 사용하고, 접수 등 비체결 단계일 때는 주문단가(901)를 우선 사용
            if cntg_div == "02":
                exec_price_str = values.get('910') or values.get('901')
            else:
                exec_price_str = values.get('901') or values.get('910')

            # 만약 여전히 가격이 0이거나 없다면 order_history DB에서 주문단가 조회
            if (not exec_price_str or float(exec_price_str or 0) <= 0) and odno:
                try:
                    from core.database import get_connection
                    conn_tmp = get_connection()
                    cur_tmp = conn_tmp.cursor()
                    cur_tmp.execute("SELECT price FROM order_history WHERE odno=?", (odno,))
                    row_p = cur_tmp.fetchone()
                    if row_p and row_p[0] and float(row_p[0]) > 0:
                        exec_price_str = str(row_p[0])
                    conn_tmp.close()
                except Exception:
                    pass

            side_raw = values.get('907') # 1:매도, 2:매수
            exec_time = values.get('908') # HHmmss
            order_div_cd = str(values.get('906') or "") # 매매구분명 또는 코드
            
            if not exec_qty_str:
                return
                
            exec_qty = int(float(exec_qty_str))
            exec_price = float(exec_price_str or 0.0)
            order_type = "SELL" if side_raw == "1" else "BUY"

            logger.debug(f"[WS] {self.market} Parsed Fields: odno={odno}, order_type={order_type}, symbol={symbol}, exec_qty={exec_qty}, exec_price={exec_price}, status={status_text}")

            is_buy = (order_type == "BUY")
            side_icon = "🔵" if is_buy else "🔴"
            status_icon = "✅" if cntg_div == "02" else "📝"
            log_prefix = "체결" if cntg_div == "02" else "주문"
            msg_title = f"{status_icon}{side_icon} [{self.market} {status_text}: {order_type}]"

            # 체결 수량이 없는 접수 단계 등은 알림만 하고 리턴 (US)
            if self.market == "US" and cntg_div == "02" and (exec_qty <= 0 or exec_price <= 0):
                return

            # DB에서 주문 유형 정보 보완
            if not order_div_cd:
                from core.database import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT type FROM order_history WHERE odno=?", (odno,))
                db_res = cursor.fetchone()
                if db_res:
                    order_div_cd = db_res[0]
                conn.close()

            cur_sym = "₩" if self.market == "KR" else "$"
            today_str = datetime.now().strftime("%Y-%m-%d")
            if exec_time and len(exec_time) == 6:
                formatted_exec_time = f"{today_str} {exec_time[:2]}:{exec_time[2:4]}:{exec_time[4:6]}"
            else:
                formatted_exec_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            price_fmt = f"{int(exec_price):,}" if self.market == "KR" else f"{exec_price:,.2f}"
            symbol_display = format_symbol_display(symbol, self.market)
            side_name = "매수" if is_buy else "매도"
            
            order_type_display = ORDER_TYPE_MAP.get(order_div_cd, order_div_cd)

            # 로그 기록 및 텔레그램 전송
            log_msg = f"[WS {log_prefix}] [{self.market}] {symbol_display} {side_name} {log_prefix} ({order_type_display})! {exec_qty}주 @ {cur_sym}{price_fmt} ({exec_time})"
            logger.info(log_msg)
            
            tg_msg = (
                f"⚡ <b>{msg_title}</b>\n"
                f"일시: {formatted_exec_time}\n"
                f"종목: <b>{symbol_display}</b>\n"
                f"구분: {side_name}\n"
                f"수량: {exec_qty}주\n"
                f"가격: {cur_sym}{price_fmt}"
            )
            if order_type_display:
                tg_msg += f"\n유형: {order_type_display}"
            send_telegram_message(tg_msg)
            
            # 실제 체결 완료 시 잔고/상태 및 DB 업데이트
            if cntg_div == "02":
                self.process_trade_update(symbol, order_type, exec_price, exec_qty, formatted_exec_time, odno=odno)

        except Exception as e:
            logger.error(f"[WS] 데이터 파싱 오류: {e} | 아이템: {item}")

    def process_trade_update(self, symbol, order_type, price, qty, time_str, odno=None):
        """체결 정보를 바탕으로 DB 업데이트 (KIS 로직 완전 계승)"""
        if odno:
            delete_order_by_odno_db(odno)

        from core.database import get_connection, load_state_db
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT strategy, strategy_name FROM order_history WHERE odno=?", (odno,))
        order_info = cursor.fetchone()

        # 잔고 조회
        equity_res = self._broker.get_account_equity(symbol)
        real_avg_price = 0.0
        if equity_res and equity_res[1] is not None:
            real_avg_price = equity_res[1]
        
        avg_price_for_profit = real_avg_price
        realized_profit = 0.0
        realized_profit_rate = 0.0

        if order_info:
            target_strategy_type = order_info[0]
            target_strategy_alias = order_info[1]
            strategy_found_for_log = target_strategy_type
        elif symbol:
            cursor.execute("SELECT strategy, strategy_name FROM strategy_state WHERE (symbol=? OR symbol LIKE ?) AND market=? AND is_active=1 LIMIT 1", (symbol, f"{symbol} %", self.market))
            fallback_info = cursor.fetchone()
            if fallback_info:
                target_strategy_type, target_strategy_alias = fallback_info
                strategy_found_for_log = target_strategy_type
            else:
                target_strategy_type, target_strategy_alias, strategy_found_for_log = None, None, "MANUAL"
        
        conn.close()

        if target_strategy_type and target_strategy_alias:
            state_data = load_state_db(symbol, target_strategy_type, market=self.market, strategy_name=target_strategy_alias)
            
            if state_data:
                if avg_price_for_profit <= 0:
                    avg_price_for_profit = float(state_data.get('avg_price', 0.0))
                
                if avg_price_for_profit <= 0:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT avg_price FROM trade_history 
                        WHERE symbol=? AND market=? AND strategy_name=? AND avg_price > 0 
                        ORDER BY date DESC, id DESC LIMIT 1
                    ''', (symbol, self.market, target_strategy_alias))
                    row_th = cursor.fetchone()
                    if row_th:
                        avg_price_for_profit = row_th[0]
                    conn.close()

                try:
                    if target_strategy_type == "VR":
                        vr_state = VRState(**state_data)
                        current_pool = float(vr_state.pool)
                        trade_amt = price * qty
                        
                        if order_type == "BUY":
                            vr_state.pool = current_pool - trade_amt
                        elif order_type == "SELL":
                            vr_state.pool = current_pool + trade_amt
                        
                        save_state_db(vr_state, market=self.market, strategy_name=vr_state.strategy_name)
                        cur_sym = "₩" if self.market == "KR" else "$"
                        symbol_display = format_symbol_display(symbol, self.market)
                        msg = f"💰 [{self.market} VR 잔고 보고] {symbol_display} ({vr_state.strategy_name})\nPool: {cur_sym}{current_pool:,.2f} -> <b>{cur_sym}{vr_state.pool:,.2f}</b>"
                        logger.info(msg.replace('\n', ' '))
                        send_telegram_message(msg)
                        
                    elif target_strategy_type == "CA":
                        ca_state = CAState(**state_data)
                        current_shares = float(ca_state.total_shares)
                        current_avg = float(ca_state.avg_price)
                        trade_amt = price * qty
                        
                        if order_type == "BUY":
                            new_shares = current_shares + qty
                            if new_shares > 0:
                                new_avg = ((current_shares * current_avg) + (qty * price)) / new_shares
                            else:
                                new_avg = price
                            
                            ca_state.total_shares = new_shares
                            ca_state.avg_price = new_avg
                            ca_state.last_execution_price = price
                            
                            unit_buy = float(ca_state.unit_buy_amount)
                            if unit_buy > 0:
                                invested = new_shares * new_avg
                                ca_state.current_turn = math.ceil((invested / unit_buy) * 10) / 10.0
                            
                        elif order_type == "SELL":
                            new_shares = max(0, current_shares - qty)
                            ca_state.total_shares = new_shares
                            
                            if new_shares == 0:
                                ca_state.pending_cycle_transition = True
                                logger.info(f"🚩 [WS] {symbol} 전량 매도 확인. 다음 날 장 시작 시 차수 전환이 진행됩니다.")
                        
                        save_state_db(ca_state, market=self.market, strategy_name=ca_state.strategy_name)
                        symbol_display = format_symbol_display(symbol, self.market)
                        logger.info(f"[WS] CA 잔고 및 상태 업데이트 완료: {symbol_display} ({ca_state.strategy_name}) (T: {ca_state.current_turn})")
                except Exception as e:
                    logger.error(f"[WS] {target_strategy_type} 상태 업데이트 실패: {e}")

        # 수수료 및 세금 산출
        fee_rate = float(os.getenv("fee_rate", "0.00015" if self.market == "KR" else "0.0007"))
        tax_rate = float(os.getenv("tax_sell", "0.0020" if self.market == "KR" else "0.0000206"))

        fee_val = 0.0
        tax_val = 0.0
        principal = price * qty
        if order_type == "SELL":
            fee_val = round(principal * fee_rate, 2)
            tax_val = round(principal * tax_rate, 2)
            total_amt = principal - fee_val - tax_val
            
            if avg_price_for_profit > 0:
                cost_basis = avg_price_for_profit * qty * (1 + fee_rate)
                realized_profit = total_amt - cost_basis
                if cost_basis > 0:
                    realized_profit_rate = (realized_profit / cost_basis) * 100
        else:
            fee_val = round(principal * fee_rate, 2)
            total_amt = principal + fee_val

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total_amount) FROM trade_history WHERE strategy_name=? AND symbol=? AND market=? AND side='BUY'", (target_strategy_alias, symbol, self.market))
            c_buy = (cursor.fetchone()[0] or 0.0) + (total_amt if order_type == "BUY" else 0.0)
            cursor.execute("SELECT SUM(total_amount) FROM trade_history WHERE strategy_name=? AND symbol=? AND market=? AND side='SELL'", (target_strategy_alias, symbol, self.market))
            c_sell = (cursor.fetchone()[0] or 0.0) + (total_amt if order_type == "SELL" else 0.0)
            conn.close()

            trade_date = time_str if (time_str and '-' in str(time_str)) else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_trade_db(
                date=trade_date,
                symbol=symbol,
                strategy=strategy_found_for_log,
                side=order_type,
                price=price,
                qty=qty,
                fee=fee_val,
                total_amount=total_amt,
                turn=0.0,
                note=f"Synced (ODNO: {odno})",
                odno=odno, 
                market=self.market,
                strategy_name=target_strategy_alias,
                avg_price=avg_price_for_profit,
                realized_profit=realized_profit,
                realized_profit_rate=realized_profit_rate,
                cum_buy_amt=c_buy,
                cum_sell_amt=c_sell
            )
        except Exception as e:
            logger.error(f"[WS] 거래 내역 저장 실패: {e}")
