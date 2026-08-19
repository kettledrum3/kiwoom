import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, time as dtime
import pytz
import threading
import os

from core.cavr import CAConfig, CAState, CostAveragingEngine, _active_intraday_timers, _ca_intraday_lock

class TestIntradayDrop(unittest.TestCase):
    def setUp(self):
        _active_intraday_timers.clear()
        self.mock_broker = MagicMock()
        self.mock_broker.adjust_price_by_tick.side_effect = lambda sym, p, s: p
        self.mock_broker.get_price.return_value = 6705.0
        self.mock_broker.get_previous_close.return_value = 7145.0
        self.mock_broker.get_account_equity.return_value = (100.0, 7545.0, 0.0)
        self.mock_broker.send_order.return_value = {"status": "SUCCESS", "order_id": "MOCK123"}
        self.mock_broker.get_cash_pool.return_value = 1000000.0

        self.test_save_path = "test_intraday_state.json"
        if os.path.exists(self.test_save_path):
            os.remove(self.test_save_path)

    def tearDown(self):
        for timer in list(_active_intraday_timers.values()):
            if timer.is_alive():
                timer.cancel()
        _active_intraday_timers.clear()
        if os.path.exists(self.test_save_path):
            os.remove(self.test_save_path)

    @patch('core.cavr.save_state')
    @patch('core.cavr.datetime')
    def test_open_rush_guard_before_0905_kr(self, mock_datetime, mock_save_state):
        """09:05 이전(09:00:30)에는 급락 감시를 건너뛰어야 함"""
        kr_tz = pytz.timezone('Asia/Seoul')
        mock_now = datetime(2026, 8, 19, 9, 0, 30, tzinfo=kr_tz)
        mock_datetime.now.return_value = mock_now

        config = CAConfig(symbol="233740", market="KR", use_db=False, save_path=self.test_save_path, initial_budget=1000000.0, unit_buy_amount=100000.0)
        engine = CostAveragingEngine(config, broker=self.mock_broker)
        engine.state = CAState(
            symbol="233740", market="KR", strategy_type="CA", 
            last_check_date="2026-08-19", avg_price=7545.0, last_execution_price=0.0, unit_buy_amount=100000.0
        )

        # 전일종가 7145 대비 6705는 약 -6.15% 하락
        engine.run_intraday_check(current_price=6705.0, prev_close=7145.0)

        # 09:05 이전이므로 pending되지 않아야 함
        self.assertFalse(engine.state.intraday_drop_pending)
        timer_key = f"{config.market}_{config.symbol}_{config.strategy_name}"
        self.assertNotIn(timer_key, _active_intraday_timers)

    @patch('core.cavr.save_state')
    @patch('core.cavr.datetime')
    def test_intraday_drop_trigger_after_0905_kr(self, mock_datetime, mock_save_state):
        """09:05 이후(09:06:00)에는 급락 감시가 정상 작동하여 펜딩 설정 및 타이머 등록되어야 함"""
        kr_tz = pytz.timezone('Asia/Seoul')
        mock_now = datetime(2026, 8, 19, 9, 6, 0, tzinfo=kr_tz)
        mock_datetime.now.return_value = mock_now

        config = CAConfig(symbol="233740", market="KR", use_db=False, save_path=self.test_save_path, initial_budget=1000000.0, unit_buy_amount=100000.0)
        engine = CostAveragingEngine(config, broker=self.mock_broker)
        engine.state = CAState(
            symbol="233740", market="KR", strategy_type="CA", 
            last_check_date="2026-08-19", avg_price=7545.0, last_execution_price=0.0, unit_buy_amount=100000.0
        )

        # 전일종가 7145 대비 6705는 약 -6.15% 하락
        engine.run_intraday_check(current_price=6705.0, prev_close=7145.0)

        # 09:05 이후이므로 pending True 및 타이머 등록
        self.assertTrue(engine.state.intraday_drop_pending)
        self.assertEqual(engine.state.last_execution_price, 6705.0)
        timer_key = f"{config.market}_{config.symbol}_{config.strategy_name}"
        self.assertIn(timer_key, _active_intraday_timers)

    @patch('core.cavr.save_state')
    @patch('core.cavr.datetime')
    def test_concurrent_ticks_deduplication(self, mock_datetime, mock_save_state):
        """동시에 10개의 스레드가 틱을 처리하더라도 타이머는 1개만 등록되어야 함"""
        kr_tz = pytz.timezone('Asia/Seoul')
        mock_now = datetime(2026, 8, 19, 9, 6, 0, tzinfo=kr_tz)
        mock_datetime.now.return_value = mock_now

        config = CAConfig(symbol="233740", market="KR", use_db=False, save_path=self.test_save_path, initial_budget=1000000.0, unit_buy_amount=100000.0)
        
        # 공통 상태를 공유하는 엔진
        engine = CostAveragingEngine(config, broker=self.mock_broker)
        engine.state = CAState(
            symbol="233740", market="KR", strategy_type="CA", 
            last_check_date="2026-08-19", avg_price=7545.0, last_execution_price=0.0, unit_buy_amount=100000.0
        )

        threads = []
        for _ in range(10):
            t = threading.Thread(target=engine.run_intraday_check, kwargs={"current_price": 6705.0, "prev_close": 7145.0})
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        timer_key = f"{config.market}_{config.symbol}_{config.strategy_name}"
        self.assertIn(timer_key, _active_intraday_timers)
        self.assertTrue(engine.state.intraday_drop_pending)

    @patch('core.cavr.save_state')
    @patch('core.cavr.datetime')
    def test_reverse_mode_skips_intraday_drop(self, mock_datetime, mock_save_state):
        """리버스 모드에서는 장중 급락 매수를 건너뛰어야 함"""
        kr_tz = pytz.timezone('Asia/Seoul')
        mock_now = datetime(2026, 8, 19, 9, 6, 0, tzinfo=kr_tz)
        mock_datetime.now.return_value = mock_now

        config = CAConfig(symbol="233740", market="KR", use_db=False, save_path=self.test_save_path, initial_budget=1000000.0, unit_buy_amount=100000.0)
        engine = CostAveragingEngine(config, broker=self.mock_broker)
        engine.state = CAState(
            symbol="233740", market="KR", strategy_type="CA", 
            mode="REVERSE", last_check_date="2026-08-19", avg_price=7545.0, last_execution_price=0.0, unit_buy_amount=100000.0
        )

        engine.run_intraday_check(current_price=6705.0, prev_close=7145.0)

        self.assertFalse(engine.state.intraday_drop_pending)
        timer_key = f"{config.market}_{config.symbol}_{config.strategy_name}"
        self.assertNotIn(timer_key, _active_intraday_timers)

if __name__ == '__main__':
    unittest.main()
