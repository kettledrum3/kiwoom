# CAVR (Cost Averaging & Value Rebalancing) 자동매매 시스템

**CAVR**은 키움증권(Kiwoom) REST API를 활용하여 **미국(US) 및 한국(KR) 주식 시장**에서 전략적 자동매매를 실행하는 프로젝트입니다. **무한매수법(Cost Averaging - CA)**과 **밸류 리밸런싱(Value Rebalancing - VR)** 전략을 자동화하여 감정을 배제한 규칙 기반 투자를 지원합니다.

---

## 📈 주요 기능 및 전략 (Features & Strategies)

이 시스템의 구체적인 매매 공식과 상세 규칙은 [strategy_formula.md](file:///d:/Python_D/kiwoom/strategy_formula.md) 문서에서 확인할 수 있습니다.

### 1. 무한매수법 V2.2 (CA)
*   **분할 매수 및 평단 관리**: 자본금을 $a$분할(기본 40분할)하여 매일 LOC(Limit On Close)로 분할 매수합니다.
*   **수익 실현 및 추세 추종**: 평단가 대비 목표 수익률(기본 10%) 도달 시 보유 물량의 75%는 지정가 매도, 남은 25%는 ⭐(Star)% LOC 주문을 통해 상승 추세를 추종합니다.
*   **쿼터 손절 모드**: 원금 소진율이 100%에 도달하고 손실률이 -10%를 초과하면 보유량의 25%를 종가 시장가(MOC)로 강제 손절하고, 확보한 자금을 10분할하여 평단가 -10% LOC 매수를 진행하는 방어 로직이 가동됩니다.
*   **자동 차수 전환(Cycling)**: 전량 매도 발생 시 해당 차수를 자동 종료하고, 즉시 다음 차수 별칭(예: TQQQ_1차 -> TQQQ_2차)을 생성하여 신규 1회차 매수로 자동 재진입합니다.

### 2. 무한매수법 V4.0 (신규 적용)
*   **유동적 T값 및 매수액**: 고정 회차가 아닌 누적 매수액 기반의 정밀한 T값을 사용하며, 남은 예수금에 맞춰 매일 1회 매수액을 재산출합니다.
*   **리버스 모드 (Reverse Mode)**: 원금 소진 시 손절 대신 '무한 매도'와 '쿼터 매수'를 통해 평단을 낮추고 현금을 확보하며 시장 반등을 기다리는 소생 로직을 탑재했습니다.
*   **5일 평균 별지점**: 리버스 모드에서 최근 1주일 평균 가격을 기준으로 매매 분기점을 설정하여 변동성에 대응합니다.

### 3. 밸류 리밸런싱 (VR)
*   **실력공식 곡선 가치추종**: 하락장에서 목표 밸류($V$)의 상승을 억제하는 변형 실력공식을 적용하여 현금(Pool)의 조기 소진을 방지합니다.
*   **자동화된 2주 예약 주문**: 밴드 범위(±15%)에 맞추어 1주씩 지정가 분할 매수 및 분할 매도 주문을 생성 및 실행합니다.
*   **투자성향별 POOL 한도 제어**: 자금 운용 한도를 적립식(Pool의 75%), 거치식(50%), 인출식(25%)으로 격리 관리하여 안정성을 강화했습니다.

### 4. 멀티 마켓 지원 및 한국 시장 최적화
*   **한국(KR) 및 미국(US) 시장 동시 지원**: 두 시장의 규격 및 거래 시간에 맞춰 병렬 실행이 가능합니다.
*   **LOC 모사 주문**: LOC 주문을 지원하지 않는 한국 시장을 위해 15:10에 지정가 주문을 일괄 발송하고 90초의 주문 간격을 두는 'LOC 모사' 기능을 탑재했습니다.
*   **수수료 및 세율 격리**: 한국 주식의 수수료 우대(0.0038%) 및 거래세(0.2%), 미국 주식 수수료 및 SEC Fee(0.00206%) 계산 체계를 완벽 분리했습니다.

### 5. 실시간 웹소켓 체결 & 장중 급락 감시
*   **초단위 실시간 체결 감시**: 키움증권 웹소켓 API(`core/ws_client.py`)를 이용해 실시간 거래 체결을 수신하고 평단가 및 수량을 즉시 DB와 동기화합니다.
*   **동적 장중 급락 번개매수**: 장중 전일 종가 대비 -3% 급락 시, 0.5T 예산에 해당하는 비례 수량을 자동으로 긴급 매수하며 직전 체결가를 기준점으로 삼아 다음 감시 기준을 동적으로 갱신합니다.

### 6. 데이터 무결성 및 인프라 안정성
*   **SQLite WAL 모드 데이터베이스**: 다중 프로세스(스케줄러, 웹소켓, 대시보드) 간의 동시성 제어 및 가용 데이터 보호를 위해 SQLite WAL 모드 데이터베이스(`database.py`)를 적용했습니다.
*   **동시성 토큰 관리 및 Soft Refresh**: 다중 스레드 동시 토큰 요청 시의 TPS 제한(`EGW00133`)을 방지하는 `_token_fetch_lock` 및 미국장 14시간 경과 시 기존 토큰 생존 상태에서 새 토큰 발급에 성공했을 때 갱신하는 Soft Refresh 기능을 지원합니다.
*   **스마트 휴장 점검**: 주말 점검 및 해외 실시간 현재가 미변동 판정 알고리즘을 이용해 휴장일에는 시스템 대기 모드로 자동 전환됩니다.

### 7. 다채널 리포팅 및 분석 대시보드
*   **실시간 텔레그램 알림**: 주문 제출, 실시간 체결(유형 및 발생시각 포함), 일일 계좌 상태 및 토큰 오류를 즉각 발송합니다.
*   **HTML 이메일 일일/월간 보고서**: Zoho SMTP를 연동하여 장 마감 후 수익률 및 환율 변동 추이를 담은 일일 보고서를 자동 발송하며, 매월 1일 Matplotlib으로 자동 드로잉한 수익 곡선 차트를 포함한 월간 투자 리포트를 발송합니다.

---

## 📂 프로젝트 구조 (Project Structure)

```text
kiwoom/
├── core/                       # 백엔드 핵심 엔진 및 서비스
│   ├── brokers/                # 시장별 API 브로커 인터페이스
│   │   ├── base.py             # 브로커 추상 기본 클래스
│   │   ├── kiwoom_kr.py        # 키움 한국 시장 API 구현체
│   │   └── kiwoom_us.py        # 키움 미국 시장 API 구현체
│   ├── cavr.py                 # 무한매수법(CA) & 밸류리밸런싱(VR) 엔진
│   ├── backtest.py             # 백테스트 시뮬레이션 엔진
│   ├── fetch_data.py           # 과거 시세 수집 모듈
│   ├── database.py             # SQLite DB 핸들링 및 토큰/상태 트랙킹
│   ├── scheduler.py            # 스케줄러 (Prepare/Open 작업 이원화 실행)
│   ├── ws_client.py            # 웹소켓 실시간 체결 수신 및 스레드 풀 구동
│   ├── notifier.py             # 텔레그램 알림 인터페이스
│   ├── email_service.py        # Zoho SMTP 메일 발송 및 Matplotlib 차트 빌더
│   ├── auth.py                 # OTP 기반 비밀번호/인증 시스템
│   └── utils.py                # 종목명 포맷팅 및 공통 헬퍼 함수
├── env/                        # 환경 설정 및 종목 리스트
│   ├── .env.kr                 # 한국 시장 키움 API Key 및 계좌 정보
│   ├── .env.us                 # 미국 시장 키움 API Key 및 계좌 정보
│   ├── ETF_list_kr.txt         # 한국 시장 감시/거래 종목 파일
│   └── ETF_list_us.txt         # 미국 시장 감시/거래 종목 파일
├── cleanup_db.py               # 불완전 거래 정리 및 DB 날짜 포맷 클린업 유틸
├── dashboard.py                # Streamlit 기반 다기능 웹 UI 대시보드
├── dockerfile                  # 대시보드 및 시스템 이미지 빌드 정의
├── docker-compose.yml          # 다중 컨테이너 Orchestration
├── strategy_formula.md         # 전략 매매 공식 및 시간 규격 레퍼런스
├── project_context.md          # 날짜별 개발 이력 및 트러블슈팅 아카이브
├── requirements.txt            # 의존성 패키지 명세
└── README.md                   # 본 프로젝트 소개 및 설치 가이드
```

---

## 🚀 설치 및 실행 (Getting Started)

### 1. 가상환경 및 의존성 패키지 설치
Python 3.10 이상 사용을 권장합니다.
```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 환경 변수 설정
`env/.env.kr` 및 `env/.env.us` 파일을 생성하고 다음 정보를 각각 입력합니다.
```ini
KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key
KIWOOM_CLIENT_ID=your_client_id
KIWOOM_CLIENT_SECRET=your_client_secret
KIWOOM_ACCOUNT_NO=5727882910
KIWOOM_BASE_URL=https://api.kiwoom.com
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=465
SMTP_USER=your_email@zoho.com
SMTP_PASSWORD=your_email_password
```

### 3. Streamlit 대시보드 실행
```bash
streamlit run dashboard.py
```
*   최초 실행 시 로그인 화면이 출력되며, OTP 인증을 통한 회원가입 절차(비밀번호 정책 적용)를 거쳐 접속할 수 있습니다.
*   대시보드 상에서 **'손익분석' 탭**, **'종목 리스트 관리(st.data_editor 연동)'** 등 실시간 컨트롤러를 제공합니다.

### 4. 백그라운드 스케줄러 실행
실시간 체결 모니터링(WebSocket) 및 시간대별 주문 스케줄러(`APScheduler`)를 구동합니다.
```bash
python core/scheduler.py
```

### 5. Docker Compose를 통한 배포 (권장)
컨테이너 환경에서 독립적이고 안정적으로 시스템을 배포 및 구동하려면 아래 명령어를 사용합니다.
```bash
docker-compose up -d --build
```
*   `restart: on-failure` 정책이 적용되어 예기치 못한 크래시 시 자동 복구되며, 사용자가 대시보드에서 시스템 종료 요청 시에는 의도대로 가동이 정지됩니다.

---

## 🛠️ 유지보수 및 디버깅

*   **데이터 클린업**: `python cleanup_db.py`를 실행하여 0원/0주짜리 유령 주문 내역을 소거하고, 날짜 필드의 노이즈 문자열을 정제할 수 있습니다.
*   **로그 모니터링**: 
    *   스케줄러 동작: `logs/scheduler.log`
    *   메시지 전송 이력: `logs/message_log.txt`
    *   웹소켓 체결 로그: `logs/websocket_connection.log` (또는 지정된 DB 로그)
*   **API 명세서 변환 규칙**: 키움증권 REST API 가이드를 토대로 작성된 인덱스 및 수신 규격 정보는 `API_SPEC.md`를 참고하여 최신화하십시오.
