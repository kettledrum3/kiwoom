import unittest
from unittest.mock import MagicMock, patch
import math

from core.cavr import VRConfig, VRState, ValueRebalancingEngine

class TestVRBootstrapV(unittest.TestCase):
    def setUp(self):
        self.mock_broker = MagicMock()
        self.mock_broker.adjust_price_by_tick.side_effect = lambda sym, p, s: p
        self.mock_broker.get_price.return_value = 50.0
        self.mock_broker.get_previous_close.return_value = 50.0
        self.mock_broker.get_account_equity.return_value = (0.0, 0.0, 0.0)
        self.mock_broker.get_cash_pool.return_value = 10000.0
        self.mock_broker.place_order.return_value = True

    def test_vr_initial_state_v_equals_initial_budget(self):
        """VR 생성 시 초기 목표 밸류 V는 초기 투자금(initial_budget)으로 설정되어야 함"""
        config = VRConfig(symbol="TQQQ", market="US", initial_budget=10000.0, G=10.0, use_db=False)
        engine = ValueRebalancingEngine(config, broker=self.mock_broker)

        # 초기 V는 10,000$ 이어야 함 (1/10 토막인 1,000$ 아님)
        self.assertEqual(engine.state.V, 10000.0)
        self.assertEqual(engine.state.initial_budget, 10000.0)

    def test_vr_bootstrap_completion_v2_formula(self):
        """
        Bootstrap 10일차 완료 후 실력공식으로 V2가 올바르게 계산되는지 검증
        초기 투자금 V1 = $10,000, Pool = $1,055.34, G = 10, E = $4,690.29
        V2 = 10000 + 1055.34/10 + (4690.29 - 10000)/(2*sqrt(10)) = 9265.98$
        """
        config = VRConfig(symbol="TQQQ", market="US", initial_budget=10000.0, G=10.0, use_db=False)
        engine = ValueRebalancingEngine(config, broker=self.mock_broker)
        
        # 10일차 빌드업 완료 직전 상태 모사
        engine.state = VRState(
            symbol="TQQQ", strategy_type="VR", market="US",
            V=10000.0, initial_budget=10000.0, pool=1055.34, G=10.0,
            mode="BOOTSTRAP", bootstrap_days=10, bootstrap_day_count=9, bootstrap_order_amount=0.0
        )
        
        # 10일차 마지막 매수 실행 완료 (qty=0 매수 시뮬레이션으로 E=4690.29 유지)
        self.mock_broker.get_account_equity.return_value = (93.8058, 50.0, 4690.29)
        self.mock_broker.get_price.return_value = 50.0
        
        engine.place_daily_limit_orders(
            date=MagicMock(), contribution=0.0, is_cycle_start_day=False,
            check_existing_orders=False, preview=False, order_filter="BOOTSTRAP_BUY_ONLY"
        )
        
        # 10일차 완료 후 RUNNING 모드로 전환
        self.assertEqual(engine.state.mode, "RUNNING")
        self.assertEqual(engine.state.bootstrap_day_count, 10)
        
        # 계산된 V 검증
        expected_v = 10000.0 + (1055.34 / 10.0) + ((4690.29 - 10000.0) / (2.0 * math.sqrt(10.0)))
        self.assertAlmostEqual(engine.state.V, expected_v, places=2)
        self.assertAlmostEqual(engine.state.V, 9265.98, delta=0.1)

    def test_self_healing_restores_distorted_v(self):
        """과거 왜곡된 V($898.72)가 initial_budget($10,000) 기준으로 자동 치유되는지 검증"""
        config = VRConfig(symbol="TQQQ", market="US", initial_budget=10000.0, G=10.0, use_db=True)
        
        # DB에 왜곡된 상태가 저장되어 있다고 가정
        mock_db_state = {
            "symbol": "TQQQ", "strategy_type": "VR", "market": "US", "strategy_name": "",
            "V": 898.72, "cycle_V": 898.72, "initial_budget": 10000.0,
            "pool": 1055.34, "last_E": 4690.29, "G": 10.0, "mode": "RUNNING",
            "periodic_accumulation": 0.0
        }
        
        with patch('core.cavr.load_state_db', return_value=mock_db_state), \
             patch('core.cavr.save_state_db') as mock_save:
            engine = ValueRebalancingEngine(config, broker=self.mock_broker)
            
            # 자가 치유 후 V가 9265.98$ 부근으로 복구되었는지 확인
            expected_v = 10000.0 + (1055.34 / 10.0) + ((4690.29 - 10000.0) / (2.0 * math.sqrt(10.0)))
            self.assertAlmostEqual(engine.state.V, expected_v, places=2)
            self.assertAlmostEqual(engine.state.cycle_V, expected_v, places=2)
            mock_save.assert_called()

if __name__ == '__main__':
    unittest.main()
