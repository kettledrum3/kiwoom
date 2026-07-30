import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestKiwoom")

from core.database import init_db
init_db()

from core.cavr import get_access_token
from core.brokers.kiwoom_kr import KiwoomKrBroker
from core.brokers.kiwoom_us import KiwoomUsBroker

def test_token_issuance():
    logger.info("=== 1. API Token Issuance Test ===")
    try:
        kr_token = get_access_token("KR")
        logger.info(f"KR Access Token: {kr_token[:10]}... (Len: {len(kr_token) if kr_token else 0})")
    except Exception as e:
        logger.error(f"KR Token Fail: {e}")
        
    try:
        us_token = get_access_token("US")
        logger.info(f"US Access Token: {us_token[:10]}... (Len: {len(us_token) if us_token else 0})")
    except Exception as e:
        logger.error(f"US Token Fail: {e}")

def test_kr_broker():
    logger.info("=== 2. Kiwoom KR Broker Test ===")
    try:
        broker = KiwoomKrBroker()
        # KODEX 레버리지 (122630) 또는 삼성전자 (005930)
        symbol = "005930"
        price = broker.get_price(symbol)
        prev_close = broker.get_previous_close(symbol)
        high = broker.get_current_high(symbol)
        low = broker.get_current_low(symbol)
        logger.info(f"KR Stock info ({symbol}): Price={price}, Prev_Close={prev_close}, High={high}, Low={low}")
        
        avg_5day = broker.get_last_5_day_avg_close(symbol)
        logger.info(f"KR 5-day Avg Close: {avg_5day}")
        
        cash = broker.get_cash_pool()
        logger.info(f"KR Cash Pool: {cash}")
        
        equity = broker.get_account_equity(symbol)
        logger.info(f"KR Equity ({symbol}): {equity}")
    except Exception as e:
        logger.error(f"KR Broker Error: {e}")

def test_us_broker():
    logger.info("=== 3. Kiwoom US Broker Test ===")
    try:
        broker = KiwoomUsBroker()
        # NVDA 또는 SOXL
        symbol = "SOXL"
        price = broker.get_price(symbol)
        prev_close = broker.get_previous_close(symbol)
        high = broker.get_current_high(symbol)
        low = broker.get_current_low(symbol)
        logger.info(f"US Stock info ({symbol}): Price={price}, Prev_Close={prev_close}, High={high}, Low={low}")
        
        avg_5day = broker.get_last_5_day_avg_close(symbol)
        logger.info(f"US 5-day Avg Close: {avg_5day}")
        
        cash = broker.get_cash_pool()
        logger.info(f"US Cash Pool: {cash}")
        
        equity = broker.get_account_equity(symbol)
        logger.info(f"US Equity ({symbol}): {equity}")
        
        exch_rate = broker.get_exchange_rate()
        logger.info(f"Exchange Rate: {exch_rate}")
    except Exception as e:
        logger.error(f"US Broker Error: {e}")

if __name__ == "__main__":
    test_token_issuance()
    test_kr_broker()
    test_us_broker()
