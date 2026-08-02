# Kiwoom 프로젝트 이식용 개선 사항 가이드 (2026-08-02)

이 문서는 2026년 8월 2일 한국투자증권(KIS) CAVR 프로젝트에서 해결한 대시보드 백테스트 및 실전 매매 안정화 조치 사항을 Kiwoom 프로젝트에도 그대로 이식할 수 있도록 정리한 가이드입니다.

---

## 1. 대시보드 백테스트 UI `widget_suffix` UnboundLocalError 해결

### [대상 파일] `dashboard.py`

#### [원인]
- 실행 모드를 "백테스트"로 전환할 때, 백테스트 전용 설정 UI(데이터 기간, 수수료, 매도 세금) 렌더링에 사용되는 `widget_suffix` 변수가 아직 정의되지 않은 시점에 호출되어 `UnboundLocalError`가 발생하였습니다.

#### [수정 내용]
- `widget_suffix = f"{s_symbol}_{s_alias}"` 선언부의 위치를 백테스트 설정 UI 렌더링 시작 직전으로 끌어올리고, 하위 CA/VR 분기 설정 내부에 있던 중복 선언을 삭제합니다.

```diff
@@ -635,18 +635,20 @@
             s_alias = selected_alias_opt
             st.info(f"선택됨: **{s_alias}**")
         
+        # 위젯 고유 키 생성을 위한 접미사 정의 (백테스트 설정 UI에서 사용하기 위해 상단으로 이동)
+        widget_suffix = f"{s_symbol}_{s_alias}"
+
         # DB에서 기존 설정 로드
         d_state = load_state_db(s_symbol, s_choice, market=m_code, strategy_name=s_alias) if s_mode == "실전 투자" and s_symbol else None
 
         # --- [통합] 백테스트 전용 설정 ---
         f_days, f_rate, t_rate = 300, 0.0007, 0.0
         if s_mode == "백테스트":
             col_bt1, col_bt2 = st.columns(2)
             f_days = col_bt1.number_input("데이터 기간 (일)", value=300, min_value=30, key=f"{m_lower}_{widget_suffix}_bt_days")
             f_rate = col_bt2.number_input("수수료 (%)", value=0.07, step=0.01, format="%.4f", key=f"{m_lower}_{widget_suffix}_bt_fee") / 100.0
             if m_code == "KR":
                 t_rate = st.number_input("매도 세금 (%)", value=0.25, step=0.01, format="%.4f", key=f"{m_lower}_{widget_suffix}_bt_tax") / 100.0
         
         if s_choice == "CA":
             # [CA 전용] 전략 할당 예수금만 표시
             def_pool = d_state.get('pool', 0.0) if d_state else 0.0
-            widget_suffix = f"{s_symbol}_{s_alias}"
             s_pool = st.number_input(f"전략 할당 예수금 ({m_curr})", value=float(def_pool), key=f"{m_lower}_{widget_suffix}_pool", help="이 전략에서 사용할 현금 한도입니다.")
@@ -674,5 +674,4 @@
             # [VR 전용] 운용 자본금만 표시 (예수금은 내부 상태 유지)
             def_budget = d_state.get('initial_budget', 10000.0) if d_state else 10000.0
             def_pool = d_state.get('pool', 0.0) if d_state else 0.0
-            widget_suffix = f"{s_symbol}_{s_alias}"
             i_cash = st.number_input(f"운용 자본금 ({m_curr})", value=float(def_budget), key=f"{m_lower}_{widget_suffix}_budget", help="밸류리밸런싱 운용 자본금(VR용).")
```

---

## 2. 실전 매매 운영 중 'symbol' KeyError 해결

### [대상 파일] `dashboard.py`

#### [원인]
- 계좌 동기화가 불완전한 상태(예: 최초 기동 시 일부 API 조회가 실패했거나, 5초 주기 프래그먼트 내부에서 `broker_cash`만 업데이트하여 `live_account` 세션에 다른 종목 키들이 들어가지 않은 경우)에서 `st.session_state['live_account']`를 참조하면서 `KeyError: 'symbol'` 오류가 발생하여 대시보드가 크래시되었습니다.

#### [수정 내용]
- `st.session_state['live_account']`에 접근할 때 단순 존재 유무(`in st.session_state`)만 검사하지 않고, `'symbol'` 키가 실제로 존재하는지 검증하며, 직접 키 조회가 아닌 안전한 `.get('symbol')` 형태의 참조로 방어합니다.
- `dashboard.py` 내부에서 실시간 계좌 잔고를 활용하여 화면을 그리거나 T값 계산을 제안하는 4가지 조건 분기 위치를 다음과 같이 보완합니다.

```diff
@@ -1750,7 +1750,7 @@
 
                 # [Live Data Overlay] 실시간 계좌 정보가 있다면 화면 표시용 변수를 최신화
                 # (DB 상태가 아직 업데이트되지 않았거나 초기화 상태일 경우를 대비)
-                if 'live_account' in st.session_state and st.session_state['live_account']['symbol'] == symbol:
+                if 'live_account' in st.session_state and st.session_state['live_account'].get('symbol') == symbol:
                     live_info = st.session_state['live_account']
                     if live_info['shares'] > 0:
                         # 평단과 수량을 실시간 데이터로 대체하여 표시
@@ -1948,7 +1948,7 @@
             # === 신규 진입 또는 재시작 (상태 데이터 없음) ===
             st.warning(f"'{symbol}'에 대한 진행 중인 CA 전략이 없습니다.")
             
-            if 'live_account' in st.session_state:
+            if 'live_account' in st.session_state and 'symbol' in st.session_state['live_account']:
                 # 계좌 정보 기반 T값 역산 및 초기화 제안
                 info = st.session_state['live_account']
                 current_shares = info['shares']
@@ -2030,7 +2030,7 @@
                 # VRState에는 shares가 없고 Pool과 V만 관리됨. Shares는 실시간 잔고로 파악해야 함.
                 
                 # Live 정보가 있으면 그것을 우선 사용
-                if 'live_account' in st.session_state and st.session_state['live_account']['symbol'] == symbol:
+                if 'live_account' in st.session_state and st.session_state['live_account'].get('symbol') == symbol:
                     live_shares = st.session_state['live_account']['shares']
                     live_pool = st.session_state['live_account']['pool']
                     current_price = st.session_state['live_account']['current_price']
@@ -2217,7 +2217,7 @@
         else:
             # === 신규 진입 (VR) ===
             st.warning(f"'{symbol}'에 대한 진행 중인 VR 전략이 없습니다.")
-            if 'live_account' in st.session_state and 'symbol' in st.session_state['live_account']:
+            if 'live_account' in st.session_state and 'symbol' in st.session_state['live_account']:
                 info = st.session_state['live_account']
                 init_v = (info['shares'] * info['current_price']) + info['pool']
```

---

## 3. 백테스트 실행 시 `BacktestBroker` `NotImplementedError` 해결

### [대상 파일] `core/backtest.py`

#### [원인]
- 백테스트가 종료 단계(`_save_and_finish` 등)에 도달할 때, 브로커 인스턴스의 전일 종가 조회 메서드(`get_previous_close`)를 필요로 하지만 `BacktestBroker`에 해당 메서드가 구현되어 있지 않아 부모 추상 클래스인 `Broker`의 `NotImplementedError`가 발생하여 시뮬레이션이 중단되었습니다.

#### [수정 내용]
- `BacktestBroker` 클래스 내에 `get_previous_close` 메서드를 추가합니다.
- 현재 인덱스(`self.current_idx`)를 기준으로 직전 데이터 종가(`Close`)를 반환하며, 첫 번째 거래일(0일)인 경우 당일의 `Open` 가격(존재 시) 또는 `Close` 가격을 대용하여 반환하도록 설계합니다.

```python
    def get_previous_close(self, symbol: str) -> float:
        """직전 거래일 종가 반환 (백테스트 시뮬레이션용)"""
        if self.current_idx > 0:
            return float(self.df.iloc[self.current_idx - 1]['Close'])
        else:
            row = self.df.iloc[self.current_idx]
            if 'Open' in row:
                return float(row['Open'])
            return float(row['Close'])
```

#### [코드 추가 위치 예시]
- `core/backtest.py` 의 `BacktestBroker` 내 `get_price` 와 `get_current_high` 메서드 사이에 위 코드를 배치하면 무난합니다.
