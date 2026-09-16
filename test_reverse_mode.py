import unittest
import math
from datetime import datetime
from core.cavr import CostAveragingEngine, CAConfig, CAState
from core.brokers.base import Broker

class MockBroker(Broker):
    def __init__(self, price=100.0, shares=200.0, avg_price=100.0, pool=10000.0, ma5=100.0, trade_mode="REAL"):
        self._price = price
        self._shares = shares
        self._avg_price = avg_price
        self._pool = pool
        self._ma5 = ma5
        self.trade_mode = trade_mode
        self.orders = []

    def get_price(self, symbol: str) -> float:
        return self._price

    def get_previous_close(self, symbol: str) -> float:
        return self._price

    def get_last_5_day_avg_close(self, symbol: str) -> float:
        return self._ma5

    def get_current_high(self, symbol: str) -> float:
        return self._price

    def get_current_low(self, symbol: str) -> float:
        return self._price

    def get_account_equity(self, symbol: str):
        return self._shares, self._avg_price, self._shares * self._price

    def get_cash_pool(self) -> float:
        return self._pool

    def get_cumulative_buy_amount(self, symbol: str) -> float:
        return self._shares * self._avg_price

    def place_order(self, symbol, price, qty, order_type, price_type="00", strategy="CA", strategy_name="", stop_price=None):
        self.orders.append({
            "symbol": symbol,
            "price": price,
            "qty": qty,
            "order_type": order_type,
            "price_type": price_type,
            "strategy": strategy,
            "strategy_name": strategy_name
        })
        return True

    def fetch_open_orders(self, symbol: str):
        return []

    def fetch_execution_history(self, symbol: str, start_date: str, end_date: str):
        return []


class TestReverseMode(unittest.TestCase):

    def test_reverse_mode_entry(self):
        """1. 진입 조건 테스트: T >= a - 1 도달 시 REVERSE 모드로 전환 및 reverse_cycle_count = 0"""
        broker = MockBroker(price=70.0, shares=390.0, avg_price=100.0, pool=1000.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=39.0, # T = 39 >= 40 - 1
            total_shares=390.0,
            avg_price=100.0,
            pool=1000.0,
            mode="NORMAL",
            reverse_cycle_count=0
        )

        planned = engine.run_cycle(datetime.now(), preview=True)
        self.assertEqual(engine.state.mode, "REVERSE")
        self.assertEqual(engine.state.reverse_cycle_count, 0)

    def test_reverse_mode_first_day(self):
        """2. 첫날(1회차) 분기 테스트: MOC 강제 매도 1/(a/2), 매수 없음, T값 갱신 및 reverse_cycle_count 증가"""
        broker = MockBroker(price=70.0, shares=200.0, avg_price=100.0, pool=5000.0, ma5=75.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=39.0,
            total_shares=200.0,
            avg_price=100.0,
            pool=5000.0,
            mode="REVERSE",
            reverse_cycle_count=0
        )

        # 1) Preview 모드 검증
        planned = engine.run_cycle(datetime.now(), preview=True)
        self.assertIsNotNone(planned)
        self.assertEqual(len(planned), 1)
        sell_order = planned[0]
        self.assertEqual(sell_order["side"], "SELL")
        self.assertEqual(sell_order["qty"], 10) # 200 / 20 = 10
        self.assertEqual(sell_order["type"], "33") # 미국 MOC
        self.assertIn("MOC", sell_order["desc"])

        # 2) 실제 실행 모드 검증
        engine.run_cycle(datetime.now(), preview=False)
        # T_new = 39.0 * (1 - 1/20) = 39.0 * 0.95 = 37.05
        self.assertAlmostEqual(engine.state.current_turn, 37.05, places=3)
        self.assertEqual(engine.state.reverse_cycle_count, 1)
        self.assertEqual(engine.state.mode, "REVERSE")

    def test_reverse_mode_second_day_and_beyond(self):
        """3. 2회차 이후 테스트: MA5 위 LOC 매도 + MA5 아래 가용 Pool 25% LOC 쿼터 매수, T값 수식 검증"""
        broker = MockBroker(price=70.0, shares=190.0, avg_price=100.0, pool=5000.0, ma5=75.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=37.05,
            total_shares=190.0,
            avg_price=100.0,
            pool=5000.0,
            mode="REVERSE",
            reverse_cycle_count=1 # 2회차
        )

        # 1) Preview 검증
        planned = engine.run_cycle(datetime.now(), preview=True)
        self.assertIsNotNone(planned)
        self.assertEqual(len(planned), 2)

        # 매도: 190 / 20 = 9주, 가격 = MA5(75.00), type = 30(LOC)
        sell_order = next(o for o in planned if o["side"] == "SELL")
        self.assertEqual(sell_order["qty"], 9)
        self.assertEqual(sell_order["price"], 75.0)
        self.assertEqual(sell_order["type"], "30")

        # 매수: Pool 5000 * 0.25 = 1250$, 가격 = 75.0 * 0.9999 = 74.99$, qty = floor(1250 / 74.99) = 16주
        buy_order = next(o for o in planned if o["side"] == "BUY")
        self.assertEqual(buy_order["price"], 74.99)
        self.assertEqual(buy_order["type"], "30")
        self.assertEqual(buy_order["qty"], int(1250.0 / 74.99))

        # 2) 실제 실행 시 T값 수식 검증
        # T_old = 37.05
        # T_sell = 37.05 * (1 - 1/20) = 35.1975
        # T_buy = 35.1975 + (40 - 35.1975) * 0.25 = 36.398125
        engine.run_cycle(datetime.now(), preview=False)
        self.assertAlmostEqual(engine.state.current_turn, 36.398125, places=4)
        self.assertEqual(engine.state.reverse_cycle_count, 2)
        self.assertEqual(engine.state.mode, "REVERSE")

    def test_reverse_mode_persistence(self):
        """4. 지속성 보장 테스트: T값이 35 등으로 떨어져도 종료 조건 미충족 시 REVERSE 모드 유지"""
        broker = MockBroker(price=70.0, shares=180.0, avg_price=100.0, pool=5000.0, ma5=75.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=35.0, # T가 a - 1 (39)보다 훨씬 낮음
            total_shares=180.0,
            avg_price=100.0,
            pool=5000.0,
            mode="REVERSE",
            reverse_cycle_count=2
        )

        engine.run_cycle(datetime.now(), preview=False)
        self.assertEqual(engine.state.mode, "REVERSE")
        self.assertEqual(engine.state.reverse_cycle_count, 3)

    def test_reverse_mode_exit_condition(self):
        """5. 종료(회귀) 조건 테스트: 현재가 >= 평단가 * (1 - target_profit_pct) 일 때 일반 모드로 복귀 및 T값/유동 매수금 계승"""
        # 평단 100$, target_profit_pct = 0.10 -> 탈출 기준가 = 90$
        # 현재가 91$ (손익률 -9% >= -10%)
        broker = MockBroker(price=91.0, shares=180.0, avg_price=100.0, pool=20000.0, ma5=88.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=36.0,
            total_shares=180.0,
            avg_price=100.0,
            pool=20000.0,
            mode="REVERSE",
            reverse_cycle_count=3
        )

        planned = engine.run_cycle(datetime.now(), preview=True)
        # 복귀 후 NORMAL 모드 전환 및 reverse_cycle_count = 0 확인
        self.assertEqual(engine.state.mode, "NORMAL")
        self.assertEqual(engine.state.reverse_cycle_count, 0)

        # V4.0 유동 매수금 재계산 확인: available_slots = 40 - 36.0 = 4.0
        # invested = 180 * 100 = 18000$, s_pool = max(0, 20000 - 18000) = 2000$
        # unit_buy_amount = 2000 / 4 = 500$
        self.assertAlmostEqual(config.unit_buy_amount, 500.0, places=2)

    def test_reverse_mode_guards(self):
        """6. 가드 로직 테스트: SELL_LIMIT_ONLY 시 리버스 모드에서는 지정가 매도 주문 생성 안함"""
        broker = MockBroker(price=70.0, shares=200.0, avg_price=100.0, pool=5000.0, ma5=75.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=39.0,
            total_shares=200.0,
            avg_price=100.0,
            pool=5000.0,
            mode="REVERSE",
            reverse_cycle_count=1
        )

        # SELL_LIMIT_ONLY 호출
        res = engine.run_cycle(datetime.now(), preview=True, order_filter="SELL_LIMIT_ONLY")
        self.assertIsNone(res) # 75% 지정가 매도 스킵되어 아무 주문도 생성되지 않아야 함

    def test_reverse_mode_kr_first_day(self):
        """7. 한국장 리버스 모드 첫날 테스트: 시장가 매도 (type: 3), 매수 없음"""
        # 100주 보유, 40분할 -> sell_qty = 5주
        broker = MockBroker(price=50000.0, shares=100.0, avg_price=70000.0, pool=10000000.0, ma5=55000.0)
        config = CAConfig(
            symbol="005930",
            version="V4.0",
            market="KR",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="005930",
            version="V4.0",
            market="KR",
            current_turn=39.0,
            total_shares=100.0,
            avg_price=70000.0,
            pool=10000000.0,
            mode="REVERSE",
            reverse_cycle_count=0
        )

        planned = engine.run_cycle(datetime.now(), preview=True)
        self.assertIsNotNone(planned)
        self.assertEqual(len(planned), 1)
        sell_order = planned[0]
        self.assertEqual(sell_order["side"], "SELL")
        self.assertEqual(sell_order["qty"], 5)
        self.assertEqual(sell_order["type"], "3") # 한국 시장가

    def test_reverse_mode_kr_second_day(self):
        """8. 한국장 리버스 모드 2회차 테스트: LOC 모사 매도 (type: 0 또는 3) + LOC 모사 매수"""
        broker = MockBroker(price=50000.0, shares=95.0, avg_price=70000.0, pool=10000000.0, ma5=50000.0)
        config = CAConfig(
            symbol="005930",
            version="V4.0",
            market="KR",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="005930",
            version="V4.0",
            market="KR",
            current_turn=37.05,
            total_shares=95.0,
            avg_price=70000.0,
            pool=10000000.0,
            mode="REVERSE",
            reverse_cycle_count=1
        )

        planned = engine.run_cycle(datetime.now(), preview=True)
        self.assertIsNotNone(planned)
        self.assertEqual(len(planned), 2)
        sell_order = next(o for o in planned if o["side"] == "SELL")
        self.assertEqual(sell_order["qty"], 4) # 95 / 20 = 4주
        buy_order = next(o for o in planned if o["side"] == "BUY")
        self.assertEqual(buy_order["qty"], int(2500000.0 / 49990.0))

    def test_v4_turn_not_exploding_with_dynamic_unit_buy(self):
        """9. V4.0 동적 1회 매수금 축소 시에도 T(회차)가 기준분할매수금 기준으로 안정 유지되는지 검증 (T 폭등 버그 방지)"""
        # 사이클 총 예산 $10,000, 40분할 -> base_unit_buy = $250
        # 현재 누적 매수: 95주 * $100 = $9,500 (T = 38.0)
        # 잔여 가용 풀: $200 (2슬롯 남음 -> 유동 매수액 = $100)
        broker = MockBroker(price=95.0, shares=95.0, avg_price=100.0, pool=9700.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            initial_budget=10000.0,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=38.0,
            total_shares=95.0,
            avg_price=100.0,
            pool=9700.0,
            cycle_budget=10000.0,
            unit_buy_amount=250.0,
            mode="NORMAL"
        )

        # 사이클 실행 시 유동 매수액이 $100으로 줄어들더라도 T가 95로 튀지 않고 38.0을 유지해야 함
        engine.run_cycle(datetime.now(), preview=True)
        self.assertAlmostEqual(engine._get_base_unit_buy_amount(), 250.0, places=2)
        self.assertAlmostEqual(engine.state.current_turn, 38.0, places=2)
        # T가 38.0이므로 a - 1(39) 미만이어서 리버스 모드로 진입하지 않아야 함
        self.assertEqual(engine.state.mode, "NORMAL")

    def test_reverse_mode_exit_safety_and_flag(self):
        """10. 리버스 모드 탈출 시 재귀 호출 없이 NORMAL 복귀 및 _reverse_exited_today 플래그 설정 검증"""
        # 평단 100, 현재가 95 (손실률 -5.0% >= -10% 회복 조건 만족)
        broker = MockBroker(price=95.0, shares=200.0, avg_price=100.0, pool=5000.0)
        config = CAConfig(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            a_default=40,
            target_profit_pct=0.10,
            use_db=False
        )
        engine = CostAveragingEngine(config, broker=broker)
        engine.state = CAState(
            symbol="TQQQ",
            version="V4.0",
            market="US",
            current_turn=39.0,
            total_shares=200.0,
            avg_price=100.0,
            pool=5000.0,
            mode="REVERSE",
            reverse_cycle_count=1
        )

        engine.run_cycle(datetime.now(), preview=False)
        self.assertEqual(engine.state.mode, "NORMAL")
        self.assertTrue(engine._reverse_exited_today)

    def test_float_tick_rounding_defense(self):
        """11. 호가 단위 보정 시 70.07이 70.06으로 절사되지 않고 70.07로 유지되는지 부동소수점 오차 검증"""
        broker = MockBroker()
        # MockBroker 호가 보정
        sell_p = broker.adjust_price_by_tick("TQQQ", 70.07, "SELL")
        buy_p = broker.adjust_price_by_tick("TQQQ", 70.07, "BUY")
        self.assertEqual(sell_p, 70.07)
        self.assertEqual(buy_p, 70.07)

        from core.brokers.kiwoom_us import KiwoomUsBroker
        from unittest.mock import MagicMock
        us_broker = KiwoomUsBroker.__new__(KiwoomUsBroker)
        us_sell = us_broker.adjust_price_by_tick("TQQQ", 70.07, "SELL")
        us_buy = us_broker.adjust_price_by_tick("TQQQ", 70.07, "BUY")
        self.assertEqual(us_sell, 70.07)
        self.assertEqual(us_buy, 70.07)

    def test_wash_trade_prevention_max_buy_allowed(self):
        """12. 자전거래 방지 상한선 max_buy_allowed: 큰수 매수 가격이 매도 호가보다 최소 1센트 낮음 보장"""
        base_price = 71.7781
        star = -0.0237
        loc_buy_offset = -0.01

        broker = MockBroker()
        loc_sell_ref = broker.adjust_price_by_tick("TQQQ", base_price * (1.0 + star), "SELL")
        max_buy_allowed = broker.adjust_price_by_tick("TQQQ", loc_sell_ref + loc_buy_offset, "BUY")
        
        price_star_raw = (base_price * (1.0 + star)) + loc_buy_offset
        star_buy_price = broker.adjust_price_by_tick("TQQQ", price_star_raw, "BUY")
        limit_star_buy = min(star_buy_price, max_buy_allowed)

        # base_price * (1+star) = 70.0769
        # 매도 LOC: 70.07
        # 매수 큰수LOC: 70.06 (70.07과 같아지지 않고 1센트 갭 보장!)
        self.assertEqual(loc_sell_ref, 70.07)
        self.assertEqual(limit_star_buy, 70.06)
        self.assertLess(limit_star_buy, loc_sell_ref)


if __name__ == "__main__":
    unittest.main()

