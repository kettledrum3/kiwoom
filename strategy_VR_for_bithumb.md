# 암호화폐(빗썸) 밸류 리밸런싱(Value Rebalancing, VR) 전략 명세서

본 문서는 미국/한국 주식 시장에서 검증된 **라오어의 밸류 리밸런싱(Value Rebalancing, VR) 및 실력공식(Skill Formula)**을 **빗썸(Bithumb) 암호화폐 거래소 환경**에 최적화하여 이식하기 위한 상세 전략 기술 명세서입니다.

---

## 1. 전략 개요 및 코인 시장 가변 사이클 타임 철학

### 1.1. 밸류 리밸런싱(VR)이란?
* 주가(코인가격)의 변동에 따라 목표 자산 가치(Target Value, $V$)를 중심으로 포트폴리오(코인 평가액 vs 원화 현금 Pool)를 정기적으로 리밸런싱하는 전략입니다.
* 목표 밸류($V$) 대비 코인 평가액이 상승하면 분할 매도하여 현금을 확보하고, 코인 가격이 하락하면 저가에서 분할 매수하여 코인 수량을 늘립니다.

### 1.2. 암호화폐 가변 사이클 타임 (Cycle Time) 및 갱신 시각 설계
24시간 365일 실시간 거래되는 빗썸 거래소 환경에 맞추어 **가변 사이클 주기**와 **사용자 지정 일일 갱신 시각**을 도입합니다.

* **사이클 주기 (Cycle Period) 선택 옵션**:
  * **1일 (24시간)**: 초고속 템포의 일일 리밸런싱
  * **2일 (48시간)**: 단기 변동성 대응 리밸런싱
  * **4일 (96시간)**: 중단기 스윙형 리밸런싱
  * **일주일 (7일, 기본 권장)**: 주간 단위 표준 리밸런싱
  * *(선택적 확장: 2주일 / 14일)*
* **전략 밸류($V$) 갱신 기준 시각 (Rebalance Execution Time)**:
  * 하루 중 전략 $V$값을 새로 산출하고 10단계 매수/매도 밴드 주문을 재배치하는 기준 시각을 사용자가 자유롭게 설정할 수 있습니다.
  * **기본값: 22:00 KST** (사용자 선호에 따라 09:00, 22:00, 00:00 등으로 변경 가능)

### 1.3. 주식 vs 빗썸 암호화폐 시장 핵심 차이점

| 구분 | 주식 시장 (미국/한국) | 빗썸(Bithumb) 암호화폐 시장 |
| :--- | :--- | :--- |
| **거래 시간** | 정규장(하루 6.5시간) / 주말 휴장 | **24시간 365일 연중무휴** |
| **리밸런싱 주기** | 2주(14일) 고정 | **가변 주기 (1일, 2일, 4일, 일주일) + 갱신 시각(기본 22:00)** |
| **최소 주문 단위** | 1주 단위 정수(int) | **소수점(Float) 단위 지원 (0.0001 단위 등)** |
| **최소 주문 금액** | 1주 가격 (종목별 상이) | **KRW 마켓 공식 최소 주문금액 5,000 KRW** |
| **거래 수수료** | 0.05% ~ 0.25% + 제세금 | **0.04% (쿠폰 적용 시)** |
| **가격 변동성** | 일일 ±30% 상하한가 또는 레버리지 변동 | **상하한가 없음 (극심한 변동성, 펌핑/덤핑)** |
| **주문 유지 방식** | 2주 예약 주문(GTC) API 지원 | **사이클 주기별 미체결 지정가 유지 + 20초 주기 동기화** |

---

## 2. 목표 밸류($V$) 산출: 실력공식 (Skill Formula)

기본 밸류 리밸런싱에 코인 하락장 방어력을 극대화한 **"실력공식"**을 적용하여 곡선형 목표 밸류($V$)를 구축합니다.

### 2.1. 실력공식 (Skill Formula) 수식

설정된 사이클(예: 1일/2일/4일/7일마다 지정된 갱신 시각, 기본 22:00 KST)이 도달하면 다음 사이클의 목표 밸류($V_2$)를 아래 공식으로 갱신합니다. (사이클 진행 중에는 $V$를 임의 변경하지 않음)

$$V_2 = V_1 + \frac{\text{Pool}}{G} + \frac{E - V_1}{2\sqrt{G}} + \text{적립금}$$

* $V_1$: 이전 사이클의 목표 밸류
* $V_2$: 신규 사이클의 목표 밸류
* $E$: 직전 사이클 종료 시점(설정 시각 22:00 KST)의 코인 총 평가액 ($E = \text{총 보유수량} \times \text{현재가}$)
* $\text{Pool}$: 현재 계좌의 가용 원화(KRW) 예수금
* $G$: 기울기 계수
  * **적립식 / 거치식**: $G = 10$ (기본 권장)
  * **인출식 (수익금 인출 목적)**: $G = 20$
* **적립금**: 해당 사이클에 사용자가 수동/자동으로 추가 투입한 KRW 금액

> **빗썸 코인 시장에서의 실력공식 효과**
> * 하락장($E < V_1$)에서는 세 번째 항인 $\frac{E - V_1}{2\sqrt{G}}$이 음수가 되어 $V$의 급상승을 억제하거나 하향 조정(내려앉음)합니다.
> * 이로 인해 극심한 코인 급락장에서도 원화 예수금(Pool)의 급격한 소진을 방지하고, 바닥권에서 매수 여력을 보존합니다.

---

## 3. 빗썸 코인형 분할 매수/매도 밴드 설계

주식과 달리 코인은 1코인 단위가 비트코인(1억원대), 솔라나(10만원대), 리플(수백원대) 등 다양하므로 **정수 1주 단위가 아닌 '가용 자산 분할 비율($N$등분, 기본 $N=10$) 기반 분할 공식'**을 적용합니다.

### 3.1. 밸류 밴드(Band) 정의
* **매수 밴드 하단 (Low Band)**: $V \times (1 - \text{band\_pct}/100)$ (기본 $\text{band\_pct} = 15\% \rightarrow V \times 0.85$)
* **매도 밴드 상단 (High Band)**: $V \times (1 + \text{band\_pct}/100)$ (기본 $\text{band\_pct} = 15\% \rightarrow V \times 1.15$)

### 3.2. 빗썸 맞춤형 분할 매수 주문 (지정가)
가용 Pool 중 사용자가 지정한 한도($25\% \sim 75\%$, 기본 50%) 내에서 Low Band 아래로 $N$단계(기본 $N=10$) 분할 매수 주문을 제출합니다.

1. **사용 가능 풀 ($P_{\text{usable}}$)**:
   $$P_{\text{usable}} = \text{Pool} \times \frac{\text{pool\_limit\_pct}}{100}$$
2. **1회 분할 매수 금액 ($M_{\text{buy}}$)**:
   $$M_{\text{buy}} = \frac{P_{\text{usable}}}{N}$$
   *(가드: 빗썸 공식 최소 주문금액 **5,000 KRW** 기준 적용, $M_{\text{buy}} < 5,000\text{ KRW}$인 경우 분할수 $N$을 줄여 건당 최소 5,000 KRW 이상이 되도록 자동 보정)*
3. **$k$번째 매수 가격 ($P_{\text{buy}, k}$)**:
   $$P_{\text{buy}, k} = \frac{\text{Low Band}}{\text{현재 보유 수량} + k \times \Delta Q_{\text{step}}}$$
   *(여기서 $\Delta Q_{\text{step}} = \frac{M_{\text{buy}}}{P_{\text{curr}}}$)*
   * 산출된 가격은 빗썸 호가 단위(`get_shifted_tick_price`)로 내림 보정합니다.
4. **$k$번째 매수 수량 ($Q_{\text{buy}, k}$)**:
   $$Q_{\text{buy}, k} = \text{floor}\left(\frac{M_{\text{buy}}}{P_{\text{buy}, k}} \times 10000\right) / 10000.0$$

### 3.3. 빗썸 맞춤형 분할 매도 주문 (지정가)
보유 코인 중 매도 대상 수량($Q_{\text{sell\_total}}$, 기본 전체 수량의 50~100%)에 대해 High Band 위로 $N$단계(기본 $N=10$) 분할 매도 주문을 제출합니다.

1. **1회 분할 매도 수량 ($\Delta Q_{\text{sell}}$)**:
   $$\Delta Q_{\text{sell}} = \text{floor}\left(\frac{Q_{\text{sell\_total}}}{N} \times 10000\right) / 10000.0$$
2. **$k$번째 매도 가격 ($P_{\text{sell}, k}$)**:
   $$P_{\text{sell}, k} = \frac{\text{High Band}}{\max(\text{현재 보유 수량} - (k-1) \times \Delta Q_{\text{sell}}, \Delta Q_{\text{sell}})}$$
   * 산출된 가격은 빗썸 호가 단위로 올림 보정합니다.
3. **최소 주문금액 가드**:
   * 매도 예정 금액($P_{\text{sell}, k} \times \Delta Q_{\text{sell}}$)이 5,000 KRW 미만인 경우 잔여 수량을 이전 단계에 합산하거나 분할수를 축소합니다.

---

## 4. 1회차 초기화 및 Bootstrap (초기 시드 분할 진입) 모드

최초 전략 기동 시 코인 잔고가 없거나 부족한 경우를 위해 **Bootstrap 분할 매수 모드**를 지원합니다.

### 4.1. 1회차 최초 목표 밸류 ($V_{\text{init}}$)
* **초기 $V_1$**: $0.0$
* **초기 $P$ (Pool)**: 사용자가 입력한 운용 원화(KRW)
* **초기 $E$ (평가액)**: $\text{기존 보유수량} \times \text{평균매입단가}$ (없으면 $0.0$)
* **최초 목표 밸류 ($V_2$)**:
  $$V_2 = \frac{P}{G} + \frac{E}{2\sqrt{G}}$$

### 4.2. Bootstrap 자동 진입 및 분할 매수 규칙
1. **진입 조건**:
   * $P_{\text{usable}} (\text{Pool} \times \text{pool\_limit\_pct}/100) > \text{Low Band}$ 인 경우, 초기 코인 비중 확보를 위해 **Bootstrap 모드** 시작.
   * 그렇지 않을 경우 즉시 일반 `RUNNING` 밸류리밸런싱 모드로 시작.
2. **Bootstrap 분할 실행**:
   * 매일 지정 갱신 시각(기본 22:00 KST)에 $P_{\text{usable}}$의 **10등분(10일)** 또는 **5등분(5일)**을 분할 매수.
   * 건당 매수 금액이 5,000 KRW 이상이어야 하며, 5등분으로도 5,000 KRW 미만일 경우 즉시 일반 모드로 전환.
3. **일반 모드 전환**:
   * 지정 일수(10일/5일) 매수가 완료되면 실력공식에 의해 $V$를 정규 산출하고 일반 `RUNNING` 모드로 진입.

---

## 5. 빗썸 대시보드(Streamlit UI) 및 시스템 아키텍처 연계

기존 빗썸 대시보드의 상태와 UI 개선 사항(`project_context_ca.md`)을 완벽히 계승하여 통합합니다.

### 5.1. 대시보드 7대 메인 탭 구성
1. **[ 📈 그리드 현황 ]**: 기존 그리드 매매 실시간 모니터링
2. **[ ⭐ 무한매수법 CA ]**: 가변 주기(4h/6h/8h/12h/24h) CA V4.0 전용 대시보드
3. **[ 💎 밸류 리밸런싱 VR ]**: **(신설)** 가변 주기(1일/2일/4일/7일, 갱신 시각: 22:00 KST) VR 전용 대시보드
4. **[ 📋 거래 내역 ]**: 전략별(그리드/CA/VR) 통합 주문/체결 내역 조회
5. **[ 📊 수익 분석 ]**: 서브 탭 분리 (`[ 📊 그리드 수익분석 ]` / `[ ⭐ CA 수익분석 ]` / `[ 💎 VR 수익분석 ]`)
6. **[ 🗃️ 종료된 전략 ]**: 완결 및 수동 종료된 전략 아카이빙 (`closed_strategies` 테이블 연동)
7. **[ ⚙️ 시스템 설정 ]**: API 키, 텔레그램 연동, DB 관리

### 5.2. 사이드바 (Sidebar) 제어 UI
* **전략 생성 폼 (VR)**:
  * 마켓 선택: KRW-BTC, KRW-ETH, KRW-SOL 등
  * 운용 자본금(Pool), 기울기 계수 $G$ (기본 10), 밴드 폭 (기본 ±15%), Pool 사용한도 (기본 50%), 적립금 설정
  * **사이클 주기 선택**: `1일` / `2일` / `4일` / `일주일 (7일)` (드롭다운)
  * **일일 갱신 시각 지정**: `22:00` (기본값, TimePicker 또는 셀렉트박스)
* **실행 중인 VR 카드 & 4대 제어 버튼**:
  * 상태 뱃지: 🟢 가동 중 / ⏸️ 일시정지 / 🔵 Bootstrap 중
  * 진행 현황: 예) `3일차 / 4일 (다음 갱신: 오늘 22:00 KST)`
  * **⏸️ 일시정지**: `vr_state`에 `is_running='false'` 기록 후 미체결 안전 유지
  * **▶️ 다시시작**: `vr_state`에 `is_running='true'` 기록 후 매매 재개
  * **🔄 동기화**: 빗썸 잔고 및 10단계 밴드 주문 실시간 교차 동기화
  * **🛑 종료**: 미체결 전량 취소, 최종 실현손익 `closed_strategies` 영구 저장 및 안전 정리 (`terminate`)

### 5.3. 빗썸 API 특화 및 체결 가드
1. **최소 주문 금액 일원화**: **5,000 KRW** (`core/constants.py: MIN_ORDER_AMOUNT_KRW = 5000`)
2. **수량 계산**: **소수점 이하 4자리 절사 (`math.floor(q * 10000) / 10000.0`)**
3. **빗썸 KRW 마켓 호가단위 룰 준수**
4. **50만원 분할 발주 & API Rate Limit 방어**:
   * 50만원 초과 주문 시 50만원 이하 단위로 분할하여 0.2초 간격 발주.
5. **사전 예상 주문 등록 및 지연 REST 검증**:
   * 웹소켓과 REST API 교차 검증으로 체결 알림 및 상태 동기화 보장.

---

## 6. Multi-DB 분리 및 아키텍처 구현 내역 (2026-09-04 ~ 2026-09-05 구현 완료)

### 6.1. VR 엔진 아키텍처 및 표준 라이프사이클 (`core/vr_strategy.py`)
* **`CoinVRStrategy` 표준 비동기 루프 (`async def run(self)` 구현)**:
  * 대시보드 백그라운드 태스크 러너(`run_strategy_async`)와의 완전한 규격 호환성 확보.
  * 가동 시작 시 `self.is_running = True` 설정 및 `initialize()` 실행 (빗썸 실시간 잔고/시세 동기화, 초기 $V$ 및 $\pm 15\%$ 밴드 계산, 시작 시각 등록).
  * 웹소켓 리스너 등록 및 텔레그램 시작 알림 발송.
  * 초기 진입 매수 및 10단계 밴드 주문 자동 배치 후, 백그라운드 스케줄러 루프(`_scheduler_loop`)를 지속 가동.
  * 태스크 취소/종료 시 DB 상태 자동 백업 및 리소스 안전 해제.
* **표준 라이프사이클 메서드 연계**:
  * `start()`: `await self.run()` 호출을 통한 통합 기동.
  * `pause()`: `self.is_running = False` 설정, 미체결 주문 보존 및 DB 상태 동기화.
  * `resume()`: 시세/잔고 재동기화 후 `_scheduler_loop` 재가동.
  * `cleanup()`: `await self.terminate()`를 호출하여 대시보드 종료 프로세스와 100% 호환.
  * `to_config_dict()`: 대시보드 및 백업 매니저에서 재기동 시 필요한 전략 파라미터 딕셔너리 반환.

### 6.2. Multi-DB 물리적 완전 격리 (`core/database.py`)
* **VR 메인 DB 분리**: `data/vr_trading.db` 전용 DB를 운용하여 Grid(`grid_trading.db`), CA(`ca_trading.db`)와의 파일 잠금(Lock) 경합 0% 달성.
* **개별 전략 DB 폴더 분리**: `data/strategies/vr/{전략명}.db` 전용 디렉토리 격리.
* **전용 테이블 및 핸들러**:
  * `vr_state`: 목표 밸류($V$), $V_1$, $V_2$, Low/High 밴드, 회차, Bootstrap 진행도, `is_running` 영구 보관 (`save_vr_state`, `load_vr_state`).
  * `vr_band_orders`: 10단계 상/하향 밴드 주문 이력 및 상태 관리 (`save_vr_band_order`, `load_vr_band_orders`, `update_vr_band_order_status`).
  * `is_vr_type()`: 전략명 또는 타입에 기반한 자동 전용 DB 라우팅 지원.

### 6.3. 대시보드 통합 UI 구성 (`web_ui/dashboard.py`)
* **메인 대시보드**: **`💎 밸류 리밸런싱 VR` 전용 탭** 배치, 실시간 목표 밸류($V$), 가용 Pool, 현재가 손익률, 10단계 상·하향 분할 밴드 주문 모니터링, 사이클 타임라인 카운트다운 실시간 표출.
* **사이드바 제어**:
  * 첫 번째 탭 명칭을 `전략 제어`로 개편하여 `▶️ 실행 중인 전략`, `⏸️ 일시정지된 전략`을 분리 표출하고 원클릭 제어 지원.
  * 일시정지 개별 제어 시 그리드 전용 체크박스를 숨기고, 저장된 전략 탭에서 일시정지 전략에 대한 정확한 상태 안내 및 백업 복원 가동 지원.
  * 자금 검증(`_check_sufficient_funds`)에서 VR 전용 예외 처리를 적용하여 불필요한 그리드 가격 범위 검증 없이 즉시 시작 보장.
* **통합 내역 및 로그 연동**:
  * 거래 내역 탭 내 `💎 밸류 리밸런싱(VR)` 전용 서브 탭 분리 (`load_all_vr_order_history`).
  * 종료된 전략 탭 내 `💎 밸류 리밸런싱 (VR) 종료 내역` 독립 표출.
  * 시스템 로그 필터에 `💎 밸류리밸런싱(VR) 로그` 옵션 신설.

---

## 7. 주요 안정화 및 버그 수정 내역 (2026-09-06 ~ 2026-09-07)

### 7.1. 거래소 예수금 확인 기반 사이클 적립금 Pool 충전 및 3단계 재확인 파이프라인
* **스케줄링 산출 보정**: 기준 시각이 당일 갱신 시각 이전인 경우 당일 갱신 시각을 정상 타겟팅하도록 수정.
* **거래소 실가용 예수금 연동**: 매 사이클 갱신 시 실가용 원화(`available_krw`)를 검사하여 회차 적립금을 전략 Pool에 안전하게 충전(전액 충전, 부분 충전, 부족 시 텔레그램 경고).
* **주문 재확인(Fail-Safe Guard) 가드**: 목표 미달 및 코인 미보유 상태에서 가용 Pool이 충분함에도 매수 주문이 0건으로 산출될 경우 현재가 - 1틱으로 최소 1건(5,000원)의 안전 매수를 강제 보정 생성.
* **파라미터 즉시 반영**: Pool 및 적립금 수정 시 목표 밸류($V$)와 밴드를 즉시 재계산하고 주문을 재배치하는 원클릭 자동화 구축.
* **거래소 지정가 주문 표준화 및 단일 레코드 관리**: `place_limit_order` 연동, 실체결 호가 정밀 기록(수수료 중복 왜곡 제거), 부분체결 후 잔여취소 시 체결완료(`done`) 승격 및 단일 주문 레코드 관리.
* **앱 재시작 시 실행 상태(`is_running: True`) 자동 복원**: `vr_state` 테이블의 실행 상태를 최우선 인식하여 프로그램 재기동 시 일시정지 없이 자동 재가동.

### 7.2. 거래소 보유 코인 수량(`holding_qty`) 동기화 정밀화 (2026-09-07)
* **현상 및 원인**:
  * 빗썸 API는 잔고 조회(`POST /info/balance`) 시 미체결 주문에 걸려있지 않은 가용 수량(`available_{currency}`)과 지정가 매도 주문에 묶여있는 수량(`in_use_{currency}`)을 분리 반환.
  * 기존에 `available` 값만 읽어올 경우 지정가 매도 주문에 묶인 코인이 누락되어 대시보드 평가액이 급감하는 왜곡 현상 발생 가능.
* **해결 조치**:
  * `self.holding_qty = float(b.get('available') or 0.0) + float(b.get('in_use') or 0.0)` 로 계산하여 주문 등록 여부와 상관없이 **실제 거래소 총 보유 수량**이 정확하게 산출 및 표출되도록 표준화.

### 7.3. 고정 매매단위(`trade_unit`) 분할 주문 및 자투리(Dust) 전량 합산 (2026-09-10)
* **고정 매매단위 $u$ 도입**: BTC 기본 `0.00005 BTC`, 타 코인 `0.001` 등 소수점 8자리 정밀 단위 지원.
* **10단계 분할 매도 및 자투리 합산**: 1 ~ ($n-1$)단계는 $u$ 단위로 순차 상향 호가 배치, 마지막 단계에서 잔여 미분할 수량(Dust) 전량을 합산 발주하여 미체결 먼지 수량 원천 차단.
* **원화 발주금액 정수화**: 거래소 주문 규격에 맞추어 `order_amount`를 `int(round(volume * price))` 정수로 산출.

### 7.4. Fail-Safe 타임라인 동기화, 시작시간 보존 및 `n사이클(n일차)` 뱃지 (2026-09-11 ~ 09-12)
* **사이클 경과시간 & 남은시간 보정**:
  * 최근 갱신 완료 시점(`last_rebalance_time`) 이후 경과시간 표출.
  * 갱신 예정 시각이 과거일 경우 즉시 익일 갱신 시각(다음날 22:00 KST)으로 전진 동기화하여 실시간 카운트다운 유지.
* **시작시간(`start_time`) 영구 보존**:
  * `save_strategy_config()`에서 `created_at` 덮어쓰기 방지 (최초 생성 시각 영구 보존).
  * `vr_state` 테이블에 `start_time` 컬럼 저장 및 복원 연동.
* **`n사이클(n일차)` 모드 뱃지**:
  * Bootstrap 해제 시 `bootstrap_days = 0`, `bootstrap_mode = False`를 보존하고, 정규 운용 시 `🟢 RUNNING ({cycle_count}사이클({day_count}일차))` 형태로 일차와 사이클을 동시 표기.
* **Fail-Safe 자동 보정 헬스체커**:
  * 갱신 예정 시각 2분 이상 지연 시 헬스체커가 자동 리밸런싱을 안전 집행.

### 7.5. 이전 가용 Pool 보존 및 텔레그램 메시지(시작/갱신) 가용 Pool 표준화 (2026-09-12)
* **이전 가용 Pool (`prev_pool`) 정상화**:
  * **기존 문제**: 사이클 롤오버 시 `self.prev_pool = self.pool_amount`로 대입되어, 어제의 실제 가용 잔고가 아닌 초기 설정 Pool(예: ₩35,000)이 매번 고정 대입되었음.
  * **개선 조치**:
    * `self.current_cycle_pool`을 도입하여 사이클별 기준 가용 Pool을 추적 관리.
    * 사이클 롤오버 시 적립금 충전 직전 시점의 가용 Pool(`self.current_cycle_pool` 또는 직전 가용 잔고)을 `self.prev_pool`에 보존.
    * 롤오버 완료 후 이번 회차 가용 잔고를 `self.current_cycle_pool`에 갱신하고 DB(`vr_state`)에 영구 보존.
    * 빗썸 VR 이식 시에도 동일한 롤오버 가용 Pool 보존 엔진 적용.
* **텔레그램 알림 메시지 가용 Pool 안내 표준화**:
  * **전략 시작 메시지**: 기존 `- 운용 Pool: ₩{self.pool_amount}` 대신 실제 가용 잔고를 반영한 `- <b>가용 Pool</b>: ₩{curr_usable:,.0f} (이전: ₩{self.prev_pool:,.0f}, 한도 {self.pool_limit_pct:.0f}%)` 표기.
  * **사이클 갱신 리포트**: 기존 `- 운용 Pool` 대신 대시보드 표기와 일관되게 `- <b>가용 Pool</b>: ₩{curr_usable:,.0f} (이전: ₩{self.prev_pool:,.0f})`로 표기. (사이클 적립금 충전 시 분리 안내)

---

## 8. 빗썸(Bithumb) 실전 이식 체크리스트 및 구현 가이드

내일부터 착수할 빗썸 거래소 VR 전략 이식을 위한 구체적인 기술 명세 및 개발 요구사항입니다.

### 8.1. API 클라이언트 연동 (`BithumbApiClient`)
* **인증 방식**: HMAC-SHA512 서명 (Api-Key, Api-Sign, Api-Nonce 헤더).
* **잔고 조회 (`POST /info/balance`)**:
  * 원화 가용 잔고: `available_krw`
  * 코인 총 보유 수량: `available_{coin} + in_use_{coin}` (주문 묶임 수량 합산 필수).
* **지정가 주문 (`POST /trade/place`)**:
  * `order_currency`: 코인 심볼 (예: `BTC`)
  * `payment_currency`: 결제 통화 (`KRW`)
  * `units`: 매매 수량 (소수점 4자리 절사)
  * `price`: 지정가 (빗썸 호가 틱룰 준수, 정수형 KRW)
  * `type`: `'bid'` (매수) / `'ask'` (매도)
* **주문 취소 (`POST /trade/cancel`)**:
  * `order_id`, `type`, `order_currency`, `payment_currency`
* **시세 조회 (`GET /public/ticker/{order_currency}_{payment_currency}`)**:
  * 최신 체결가(`closing_price`) 실시간 파싱.

### 8.2. 빗썸 호가 단위(Tick Rule) 및 주문 제약 준수
* **호가 단위표**:
  * 1,000,000원 이상: 1,000원 단위
  * 500,000원 ~ 1,000,000원 미만: 500원 단위
  * 100,000원 ~ 500,000원 미만: 100원 단위
  * 10,000원 ~ 100,000원 미만: 10원 단위
  * 1,000원 ~ 10,000원 미만: 1원 단위
* **최소 주문 금액**: KRW 마켓 건당 **5,000 KRW** 이상 필수.
* **주문금액 정수화**: `int(round(units * price))`로 정수 처리.

### 8.3. DB 물리적 분리 구조
```
data/
  ├── bithumb_vr_trading.db               <-- 빗썸 VR 설정, 백업, 계정 공통 DB
  └── strategies/
      └── bithumb_vr/
          └── {전략이름}.db               <-- 빗썸 VR 전략별 개별 주문/상태 DB
```

### 8.4. 대시보드 UI 연계
* 대시보드 상단 탭에 **`[ 💎 빗썸 VR ]`** 전용 서브 탭 배치 또는 거래소 셀렉터 연동.
* 업비트와 동일한 **`🟢 RUNNING ({n}사이클({n}일차))`**, **가용 Pool / 이전 가용 Pool**, **10단계 밴드 분할 주문**, **사이클 타임라인(최근 갱신 경과 / 익일 22:00 카운트다운)** 표출.

---

## 9. [2026-09-13] 손익분석 탭 VR 백테스트 시뮬레이션 및 듀얼 Y축 차트 구조 명세

미국주식 레버리지 백테스트(`D:\Python_D\kiwoom\data\backtest_result_TQQQ_VR.csv`)의 검증된 아키텍처를 가상자산(빗썸/업비트) 환경에 완벽 이식하여, 손익분석 탭(`tab3`)에 **`[ 💎 밸류 리밸런싱 VR 수익분석 ]`** 뷰를 구축하였습니다.

### 9.1. Plotly 듀얼 Y축 차트 시각화 아키텍처 (`build_vr_plotly_figure`)

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 듀얼 Y축 서브플롯 생성
fig = make_subplots(specs=[[{"secondary_y": True}]])
```

#### 1) 좌측 Y축 (`secondary_y=False`, 원화 금액 ₩)
* **Total Equity (총 평가 자산)**:
  * 실선 파란색 (`color='#1f77b4'`, `width=2.5`)
  * 계산식: `TotalEquity = Cash_Pool + (Holding_Shares * Close_Price)`
* **Target V (목표 밸류 $V$)**:
  * 주황색 대시선 (`color='#ff7f0e'`, `width=2`, `dash='dash'`)
  * 라오어 실력공식 V2에 의해 주기별로 계단형/곡선형 성장
* **Cash Pool (가용 원화 현금 풀)**:
  * 하늘색 점선 (`color='#00e5ff'`, `width=1.5`, `dash='dot'`)
  * 매수 시 차감, 매도 시 증액되는 실제 예수금 풀 궤적
* **Band Area (밸류 밴드 영역, $\pm\text{Band}\%$)**:
  * 하단 밴드 (`lower_band = Target_V * (1 - band_pct/100)`): 투명선 (`width=0`, `showlegend=False`)
  * 상단 밴드 (`upper_band = Target_V * (1 + band_pct/100)`): 투명선, `fill='tonexty'`, `fillcolor='rgba(255, 165, 0, 0.12)'`, `name=f'Band (±{band_pct}%)'`
  * 부드러운 살구색 반투명 영역으로 밸류 정상 범위를 직관적으로 표시

#### 2) 우측 Y축 (`secondary_y=True`, 코인 시세 ₩)
* **Close Price (코인 종가 시세)**:
  * 회색 점선 (`color='#888888'`, `width=1.2`, `dash='dot'`)
* **Buy Marker (매수 체결점)**:
  * 초록색 정삼각형 ▲ (`marker=dict(color='#00c853', size=8, symbol='triangle-up')`)
* **Sell Marker (매도 체결점)**:
  * 빨간색 역삼각형 ▼ (`marker=dict(color='#d50000', size=8, symbol='triangle-down')`)

#### 3) 공통 레이아웃 설정
```python
fig.update_layout(
    title=f"💎 [{ticker}] 밸류 리밸런싱 (VR) 자산 궤적 및 밴드 분석",
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=60, r=60, t=80, b=50),
    height=620
)
fig.update_yaxes(title_text="Total Equity (₩)", secondary_y=False, tickformat=",d")
fig.update_yaxes(title_text="Close Price (₩)", secondary_y=True, tickformat=",d")
fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.15)')
fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.15)', secondary_y=False)
```

---

### 9.2. 일별 시뮬레이션 결과 데이터셋 필드 규격 (13대 지표)
미국주식 백테스트 CSV(`backtest_result_TQQQ_VR.csv`)와 100% 호환되는 출력 스키마:
1. `Date`: 날짜 (`YYYY-MM-DD`)
2. `Close`: 코인 일봉 종가 (KRW)
3. `TotalEquity`: 총 평가 자산 (원화 현금 + 코인 평가액)
4. `Cash`: 가용 현금 (KRW)
5. `Shares`: 보유 코인 수량 (Float)
6. `AvgPrice`: 보유 코인 평단가 (KRW)
7. `CumulativeBuyAmount`: 누적 매수 투입금 (KRW)
8. `NetPrincipal`: 총 투입 순원금 (초기 자본 + 누적 적립금)
9. `Target_V`: 해당 일자의 목표 밸류 ($V$)
10. `Pool`: 가용 Pool 잔고 (KRW)
11. `Accumulation`: 해당 일자 추가 투입된 적립금 (KRW)
12. `Peak`: 자산 전고점 (`TotalEquity.cummax()`)
13. `Drawdown`: 전고점 대비 낙폭률 ($(\text{TotalEquity} - \text{Peak}) / \text{Peak}$)

---

### 9.3. 백테스트 결과 요약 리포트 (Text Format)
```text
=== Backtest Result ({ticker}) ===
Strategy:       VR
Ticker:         {ticker}
Period:         {days} days
Fee Rate:       {fee_rate*100:.4f}%
Initial Equity: ₩{initial_cash:,.2f}
Net Principal:  ₩{final_net_principal:,.2f}
Final Equity:   ₩{final_equity:,.2f}
Net Profit:     ₩{net_profit:,.2f}
Return:         {return_pct:.2f}%
CAGR:           {cagr_pct}
MDD:            {mdd_pct:.2f}%
Win Rate:       N/A
Result File:    data/backtest_result_{ticker}_VR.csv
```

---

### 9.4. 빗썸 일봉 캔들 API 수집 및 백테스트 실행 (`core/vr_backtest.py`)

* **엔드포인트**: `GET https://api.bithumb.com/v1/candles/days?market=KRW-{COIN}&count=200`
* **페이징 수집**: `to` 파라미터(`candle_date_time_utc`)를 활용하여 과거 300일 이상의 일봉을 누락 없이 연속 수집.
* **대시보드 손익분석 탭 통합**:
  * 파라미터 입력: 코인 티커(BTC, ETH 등), 시뮬레이션 기간(일), 초기 자본금, 목표값 계수 $G$, 밴드폭(%), 사이클 주기(일), 주기당 적립금(₩), 거래 수수료율(%).
  * 실행 결과: 요약 메트릭 카드(수익률, 순이익, MDD, CAGR) + 텍스트 서머리 + Plotly 인터랙티브 듀얼 축 차트 + 13대 지표 데이터테이블 & CSV 다운로드 버튼.

---

### 9.5. 필수 의존성(`plotly`) 및 OCI 배포/리버스 프록시 설정
* **패키지 의존성 (`requirements.txt`, `pyproject.toml`)**:
  * 듀얼 Y축 Plotly 인터랙티브 차트 생성을 위해 `plotly` (`plotly>=5.0.0`) 의존성 명시 필수.
* **리버스 프록시 및 Streamlit 환경 ([`.streamlit/config.toml`](file:///d:/Python_D/gridbithumb/.streamlit/config.toml))**:
  * OCI / Docker / Nginx Proxy Manager 환경에서 배포 시 CORS/XSRF 차단 및 CSS 프리로드 오류(`Unable to preload CSS`)를 방지하기 위해 다음 설정을 적용:
    ```toml
    [server]
    port = 8502
    enableCORS = false
    enableXsrfProtection = false
    headless = true

    [browser]
    gatherUsageStats = false
    ```
  * Nginx Proxy Manager(NPM) 설정: `Websockets Support` ON(필수), `Cache Assets` OFF(정적 파일 경로 왜곡 방지).
* **유틸리티 모듈 타입 힌트**:
  * [`core/utils.py`](file:///d:/Python_D/gridbithumb/core/utils.py)에 `from typing import Any, Optional, Union`을 명시하여 Linux 컨테이너 환경의 `NameError: name 'Any' is not defined` 원천 차단.

---

### 9.6. [2026-09-15] 밸류 리밸런싱(VR) 미체결 취소 주문 체결(done) 오인 방지 및 손익분석 탭 메트릭 고도화

1. **웹소켓 미체결 취소 주문의 `done` 오인 버그 차단 (`core/vr_strategy.py`, `core/database.py`)**:
   - **문제 현상**: 미체결 취소 시 웹소켓 메시지의 주문 호가가 체결단가(`exec_price`)로 잘못 대입되고, DB 저장 시 `executed_price > 0` 조건만으로 취소 주문이 `done`으로 승격되어 대시보드 체결 내역에 허위 매도 체결로 왜곡 집계될 수 있는 결함 차단.
   - **조치**:
     - `_process_websocket_message()`: 체결 완료(`raw_state == 'done'`) 또는 부분체결 잔여취소(`exec_vol > 0`)일 때만 체결 단가를 산출하고, 순수 미체결 취소는 `executed_price=0.0`으로 고정.
     - `save_order_record()`: 비고에 Cancel/취소가 명시되어 있거나 상태가 cancel/cancelled인 경우 `status='cancel'` 및 `executed_price=None`을 엄격히 보존.
     - `load_all_vr_order_history()`: 조회 시 미체결 취소 주문의 `status='cancel'`, `executed_price=None` 정규화 보강.
     - `clean_cancelled_vr_orders()`: DB 내 혹시 잘못 기재된 취소 주문을 일괄 `cancel` 및 `executed_price=NULL`로 정상 복원하는 헬퍼 함수 탑재.

2. **2회차 이상 운용 시 가용 Pool(`current_cycle_pool` / `prev_pool`) 복원 보장 (`core/vr_strategy.py`)**:
   - **문제**: 전략 재시작 시 초기 설정 Pool(예: 35,000원)을 기본값으로 불러와 직전 사이클의 실제 가용 잔고가 덮어써질 위험 차단.
   - **조치**: `from_backup` 및 `initialize()`에서 2회차 이상 운용 기록(`cycle_count >= 2`)이 존재할 경우 `vr_state`의 `current_cycle_pool` 및 `prev_pool`을 최우선 복원하도록 우선순위 정비 완료.

3. **손익분석 탭 VR 실전 메트릭 표기 정비 (`web_ui/dashboard.py`)**:
   - **개편**: 기존 `설정 Pool / G계수` 메트릭을 **`가용 Pool`** (메인: `₩{curr_usable_pool:,.0f}`), 하단 서브텍스트(delta) **`총투입금: ₩{tot_deposited:,.0f}`** (`total_pool_deposited` 적립 총액 연동)으로 개편하여 실제 누적 자본 대비 가용 잔고를 직관적으로 비교 파악 가능하도록 개선.
   - **체결 내역 정제**: 실제 체결 목록(`executed_orders`) 필터링 시 `cancel`/취소 비고를 가진 주문을 완벽 제외하여 순수 체결 건수 및 거래점만 표출.




