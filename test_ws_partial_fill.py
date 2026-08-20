import os
import sys
import unittest
from unittest.mock import MagicMock, patch

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.ws_client import KisWebSocketClient

class TestWebSocketExecution(unittest.TestCase):
    def setUp(self):
        self.client_kr = KisWebSocketClient(market="KR")
        self.client_kr._broker = MagicMock()
        self.client_kr._broker.get_account_equity.return_value = (1000000, 7112.0)

    @patch('core.ws_client.send_telegram_message')
    @patch('core.ws_client.log_trade_db')
    @patch('core.ws_client.delete_order_by_odno_db')
    @patch('core.ws_client.save_state_db')
    @patch('core.ws_client.load_state_db')
    def test_kr_partial_fill_with_unit_qty(self, mock_load, mock_save, mock_del, mock_log, mock_tg):
        mock_load.return_value = {
            'symbol': '233740', 'strategy_type': 'CA', 'strategy_name': 'KODEX_1',
            'market': 'KR', 'is_active': True, 'avg_price': 7112.0, 'total_shares': 175.0,
            'current_turn': 6.2, 'pool': 8000000.0, 'unit_buy_amount': 200000.0
        }

        # 6회 분할 체결 시뮬레이션
        events = [
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '20', '911': '20', '902': '112', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '30', '911': '50', '902': '82', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '20', '911': '70', '902': '62', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '30', '911': '100', '902': '32', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '10', '911': '110', '902': '22', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
            {'item': '233740', 'values': {'9203': '0023239', '913': '체결', '915': '22', '911': '132', '902': '0', '900': '132', '914': '7605', '907': '1', '908': '102603'}},
        ]

        for ev in events:
            self.client_kr.parse_execution_data(ev)

        # 6건 모두 체결 기록이 남았는지 확인
        self.assertEqual(mock_log.call_count, 6)
        
        # 기록된 수량들의 합계가 정확히 132주인지 확인
        logged_quantities = [call.kwargs['qty'] for call in mock_log.call_args_list]
        self.assertEqual(logged_quantities, [20, 30, 20, 30, 10, 22])
        self.assertEqual(sum(logged_quantities), 132)

        # delete_order_by_odno_db는 마지막 전량 체결(unfilled_qty == 0)에서만 호출되었는지 확인
        self.assertEqual(mock_del.call_count, 1)
        mock_del.assert_called_with('0023239')

    @patch('core.ws_client.send_telegram_message')
    @patch('core.ws_client.log_trade_db')
    @patch('core.ws_client.delete_order_by_odno_db')
    @patch('core.ws_client.save_state_db')
    @patch('core.ws_client.load_state_db')
    def test_us_partial_fill_without_unit_qty(self, mock_load, mock_save, mock_del, mock_log, mock_tg):
        client_us = KisWebSocketClient(market="US")
        client_us._broker = MagicMock()
        client_us._broker.get_account_equity.return_value = (10000, 70.0)

        mock_load.return_value = {
            'symbol': 'TQQQ', 'strategy_type': 'CA', 'strategy_name': 'TQQQ_1',
            'market': 'US', 'is_active': True, 'avg_price': 70.0, 'total_shares': 100.0,
            'current_turn': 2.0, 'pool': 20000.0, 'unit_buy_amount': 500.0
        }

        # 단위체결량(915) 없이 누적체결량(911)만 오는 경우 (미국 등) + 중복 수신 테스트
        events = [
            {'item': 'TQQQ', 'values': {'9203': 'US_001', '913': '체결', '911': '20', '902': '80', '900': '100', '910': '75.5', '907': '1'}},
            {'item': 'TQQQ', 'values': {'9203': 'US_001', '913': '체결', '911': '50', '902': '50', '900': '100', '910': '75.5', '907': '1'}},
            {'item': 'TQQQ', 'values': {'9203': 'US_001', '913': '체결', '911': '100', '902': '0', '900': '100', '910': '75.5', '907': '1'}},
            # 중복 패킷
            {'item': 'TQQQ', 'values': {'9203': 'US_001', '913': '체결', '911': '100', '902': '0', '900': '100', '910': '75.5', '907': '1'}},
        ]

        for ev in events:
            client_us.parse_execution_data(ev)

        # 3건만 처리되고 중복 1건은 무시되어야 함
        self.assertEqual(mock_log.call_count, 3)
        logged_quantities = [call.kwargs['qty'] for call in mock_log.call_args_list]
        self.assertEqual(logged_quantities, [20, 30, 50])
        self.assertEqual(sum(logged_quantities), 100)

        # 전량 체결 시에만 삭제
        self.assertEqual(mock_del.call_count, 1)

    @patch('core.ws_client.get_connection')
    @patch('core.ws_client.send_telegram_message')
    @patch('core.ws_client.log_trade_db')
    @patch('core.ws_client.delete_order_by_odno_db')
    @patch('core.ws_client.save_state_db')
    @patch('core.ws_client.load_state_db')
    def test_us_sell_order_receipt_and_fill(self, mock_load, mock_save, mock_del, mock_log, mock_tg, mock_get_conn):
        # mock order_history query returning (side="SELL", price=137.50, type="00")
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = ("SELL", 137.50, "00")
        mock_conn.cursor.return_value = mock_cur
        mock_get_conn.return_value = mock_conn

        client_us = KisWebSocketClient(market="US")
        client_us._broker = MagicMock()
        client_us._broker.get_account_equity.return_value = (71.0, 67.54, 71.0 * 75.0)

        # 1. 미국 매도 주문 접수 패킷 시뮬레이션 (FID 907="01" 또는 "매도" 등)
        event_receipt = {
            'item': 'TQQQ',
            'values': {
                '9203': '000004394',
                '913': '접수',
                '900': '1',
                '901': '137.50',
                '907': '01',
                '50072': '매도',
                '908': '233404'
            }
        }
        client_us.parse_execution_data(event_receipt)

        self.assertTrue(mock_tg.called)
        tg_text = mock_tg.call_args[0][0]
        self.assertIn("[US 접수: SELL]", tg_text)
        self.assertIn("구분: 매도", tg_text)
        self.assertIn("🔴", tg_text)
        self.assertNotIn("BUY", tg_text)
        self.assertNotIn("구분: 매수", tg_text)

if __name__ == '__main__':
    unittest.main()
