import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import VRConfig, VRState, ValueRebalancingEngine

class TestVRDailyLimitOrders(unittest.TestCase):
    def setUp(self):
        self.mock_broker = MagicMock()
        self.mock_broker.adjust_price_by_tick.side_effect = lambda symbol, price, side: round(price, 2)
        self.mock_broker.place_order.return_value = True
        self.mock_broker.fetch_open_orders.return_value = []

    @patch('core.cavr.send_telegram_message')
    @patch('core.cavr.load_state_db')
    def test_us_tqqq_vr_limit_orders(self, mock_load, mock_tg):
        # 1. TQQQ VR 상태 (RUNNING 모드, V=9532.64, 보유 71주, Pool 912.10)
        tqqq_state = {
            'symbol': 'TQQQ', 'strategy_type': 'VR', 'strategy_name': 'VR-TQQQ-1호',
            'market': 'US', 'is_active': True, 'mode': 'RUNNING',
            'V': 9532.64, 'cycle_V': 9532.64, 'pool': 912.10, 'cycle_start_pool': 912.10,
            'total_shares': 71.0, 'avg_price': 67.54, 'last_E': 4795.56,
            'initial_budget': 10000.0, 'G': 10.0, 'band_low_pct': 85.0, 'band_high_pct': 115.0,
            'investment_type': 'accumulation', 'pool_limit_pct': 50.0, 'bootstrap_days': 10,
            'bootstrap_day_count': 10, 'bootstrap_order_amount': 0.0
        }
        mock_load.return_value = tqqq_state
        self.mock_broker.get_price.return_value = 75.0
        self.mock_broker.get_account_equity.return_value = (71.0, 67.54, 71.0 * 75.0)

        cfg = VRConfig(symbol='TQQQ', use_db=True, market='US', strategy_name='VR-TQQQ-1호')
        engine = ValueRebalancingEngine(cfg, broker=self.mock_broker)

        # 2. 주문 실행
        today = datetime(2026, 8, 20, 9, 40)
        engine.place_daily_limit_orders(date=today, check_existing_orders=False, preview=False)

        # 3. 매도 및 매수 주문 검증
        # 매도 5건 + 매수 4건 = 총 9건의 주문이 발주되어야 함
        self.assertEqual(self.mock_broker.place_order.call_count, 9)

        # 모든 주문이 ptype="00" (지정가)로 발주되었는지 확인
        for call in self.mock_broker.place_order.call_args_list:
            args, kwargs = call
            symbol = args[0]
            price = args[1]
            qty = args[2]
            side = args[3]
            price_type = kwargs.get('price_type')
            
            self.assertEqual(symbol, 'TQQQ')
            self.assertEqual(qty, 1)
            self.assertEqual(price_type, '00')

        # V=9532.64, High Band (115%)=10962.54, Pool=912.10, Shares=71
        # Target Sell = 10962.536 - 912.10 = 10050.436
        # Sell 1: 10050.436 / 71 = 141.56
        # Sell 2: 10050.436 / 70 = 143.58
        # Sell 3: 10050.436 / 69 = 145.66
        # Sell 4: 10050.436 / 68 = 147.80
        # Sell 5: 10050.436 / 67 = 150.01
        sell_prices = [call[0][1] for call in self.mock_broker.place_order.call_args_list if call[0][3] == 'SELL']
        expected_sells = [141.56, 143.58, 145.66, 147.80, 150.01]
        self.assertEqual(sell_prices, expected_sells)

        # V=9532.64, Low Band (85%)=8102.744, Pool=912.10, Shares=71
        # Target Buy = 8102.744 - 912.10 = 7190.644
        # Buy 1: 7190.644 / (71 + 1) = 99.87
        # Buy 2: 7190.644 / (71 + 2) = 98.50
        # Buy 3: 7190.644 / (71 + 3) = 97.17
        # Buy 4: 7190.644 / (71 + 4) = 95.88
        buy_prices = [call[0][1] for call in self.mock_broker.place_order.call_args_list if call[0][3] == 'BUY']
        expected_buys = [99.87, 98.50, 97.17, 95.88]
        self.assertEqual(buy_prices, expected_buys)

        # 텔레그램 메시지 발송 검증
        self.assertTrue(mock_tg.called)
        tg_text = mock_tg.call_args[0][0]
        self.assertIn("TQQQ", tg_text)
        self.assertIn("매도 예약 접수 (5건)", tg_text)
        self.assertIn("매수 예약 접수 (4건)", tg_text)
        self.assertIn("141.56", tg_text)
        self.assertIn("99.87", tg_text)

    @patch('core.cavr.send_telegram_message')
    @patch('core.cavr.load_state_db')
    def test_kr_vr_limit_orders(self, mock_load, mock_tg):
        # 2. KR VR 상태 (RUNNING 모드)
        kr_state = {
            'symbol': '122630', 'strategy_type': 'VR', 'strategy_name': 'KODEX_레버리지_VR',
            'market': 'KR', 'is_active': True, 'mode': 'RUNNING',
            'V': 10000000.0, 'cycle_V': 10000000.0, 'pool': 2000000.0, 'cycle_start_pool': 2000000.0,
            'total_shares': 50.0, 'avg_price': 100000.0, 'last_E': 5000000.0,
            'initial_budget': 10000000.0, 'G': 10.0, 'band_low_pct': 80.0, 'band_high_pct': 120.0,
            'investment_type': 'accumulation', 'pool_limit_pct': 50.0, 'bootstrap_days': 10,
            'bootstrap_day_count': 10, 'bootstrap_order_amount': 0.0
        }
        mock_load.return_value = kr_state
        self.mock_broker.adjust_price_by_tick.side_effect = lambda symbol, price, side: round(price)
        self.mock_broker.get_price.return_value = 100000.0
        self.mock_broker.get_account_equity.return_value = (50.0, 100000.0, 5000000.0)

        cfg = VRConfig(symbol='122630', use_db=True, market='KR', strategy_name='KODEX_레버리지_VR')
        engine = ValueRebalancingEngine(cfg, broker=self.mock_broker)

        today = datetime(2026, 8, 20, 9, 10)
        engine.place_daily_limit_orders(date=today, check_existing_orders=False, preview=False)

        # 한국 시장에서도 ptype="00" 지정가로 발주되었는지 확인
        self.assertTrue(self.mock_broker.place_order.call_count > 0)
        for call in self.mock_broker.place_order.call_args_list:
            self.assertEqual(call[1].get('price_type'), '00')

if __name__ == '__main__':
    unittest.main()
