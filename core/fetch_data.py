import os
import sys
import time
import pandas as pd
import logging
from datetime import datetime

# core 폴더로 이동함에 따라 경로 재설정
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CORE_DIR) # 프로젝트 루트

from core.brokers.kiwoom_kr import KiwoomKrBroker
from core.brokers.kiwoom_us import KiwoomUsBroker

def update_ticker_data(ticker, days=300, market="US"):
    """특정 티커의 데이터를 수집하여 CSV로 저장하는 헬퍼 함수"""
    logging.info(f"[{ticker}] {market} 과거 데이터 조회 시도...")
    
    try:
        if market == "KR":
            broker = KiwoomKrBroker()
            history = broker.fetch_daily_chart(ticker, days=days)
        else:
            broker = KiwoomUsBroker()
            history = broker.fetch_daily_chart(ticker, days=days)
            
        if history:
            df = pd.DataFrame(history)
            df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
            df = df.sort_values('Date', ascending=False).reset_index(drop=True)
            
            data_dir = os.path.join(BASE_DIR, "data")
            os.makedirs(data_dir, exist_ok=True)
            save_path = os.path.join(data_dir, f"{ticker}.csv")
            df.to_csv(save_path, index=False)
            return True, f"{ticker} 데이터 {len(df)}건 저장 완료 ({save_path})"
        else:
            return False, f"{ticker} 데이터 수집 실패 (조회된 결과가 없습니다)"
    except Exception as e:
        logging.error(f"[Fetch Error] {ticker} ({market}): {e}")
        return False, str(e)

def main():
    log_file_path = os.path.join(CORE_DIR, "logs.txt")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.info("시뮬레이션 데이터 수집 시스템 시작 (키움증권 REST API 기반)")
    
    etf_list_path = os.path.join(BASE_DIR, "env", "ETF_list_us.txt")
    if not os.path.exists(etf_list_path):
        etf_list_path = os.path.join(BASE_DIR, "env", "ETF_List.txt")
    
    try:
        with open(etf_list_path, 'r', encoding='utf-8') as f:
            targets = []
            for line in f:
                clean_line = line.split('#')[0].strip()
                if clean_line:
                    targets.append(clean_line.split()[0].upper())
    except FileNotFoundError:
        logging.error(f"{etf_list_path} 파일을 찾을 수 없습니다.")
        return
             
    logging.info(f"대상 종목({len(targets)}개): {targets}")
    logging.info("="*60)
    
    for ticker in targets:
        success, msg = update_ticker_data(ticker, days=300, market="US")
        if success:
            logging.info(f"  > {msg}")
        else:
            logging.error(f"  > {msg}")
        time.sleep(0.5)
        logging.info("-" * 60)

if __name__ == "__main__":
    main()
