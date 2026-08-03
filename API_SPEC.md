# Kiwoom REST API Specification
본 문서는 `KIWOOM_REST_API_Doc_Stocks.xlsx`와 `키움 REST API 문서.xlsx`를 병합 및 분석하여 자동 생성한 키움증권 REST API 명세서입니다.

## [au10001] 접근토큰 발급
- **메뉴 위치**: OAuth 인증 > 접근토큰발급 > 접근토큰 발급(au10001)
- **HTTP Method**: `POST`
- **Request URL**: `/oauth2/token`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `grant_type` | grant_type |  | Y |  | client_credentials 입력 |
| Body | `appkey` | 앱키 |  | Y |  |  |
| Body | `secretkey` | 시크릿키 |  | Y |  |  |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `expires_dt` | 만료일 |  | Y |  |  |
| Body | `token_type` | 토큰타입 |  | Y |  |  |
| Body | `token` | 접근토큰 |  | Y |  |  |

### Request Example
```json
{
    "grant_type": "client_credentials",
    "appkey": "AxserEsdcredca.....",
    "secretkey": "SEefdcwcforehDre2fdvc...."
}
```

### Response Example
```json
{
    "expires_dt":"20241107083713",
    "token_type":"bearer",
    "token":"WQJCwyqInphKnR3bSRtB9NE1lv..."
    "return_code":0,
    "return_msg":"정상적으로 처리되었습니다"
}
```

---

## [au10002] 접근토큰폐기
- **메뉴 위치**: OAuth 인증 > 접근토큰폐기 > 접근토큰폐기(au10002)
- **HTTP Method**: `POST`
- **Request URL**: `/oauth2/revoke`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `appkey` | 앱키 |  | Y |  |  |
| Body | `secretkey` | 시크릿키 |  | Y |  |  |
| Body | `token` | 접근토큰 |  | Y |  |  |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |

### Request Example
```json
{
    "appkey": "AxserEsdcredca.....",
    "secretkey": "SEefdcwcforehDre2fdvc....",
    "token": "WQJCwyqInphKnR3bSRtB9NE1lv..."
}
```

### Response Example
```json
{
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka00001] 계좌번호조회
- **메뉴 위치**: 국내주식 > 계좌 > 계좌번호조회(ka00001)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 현재 토큰의 계좌번호를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `acctNo` | 계좌번호 |  | N | 20 | 10자리 숫자가 출력됩니다. 뒤에 2자리는 당사에서 계좌를 분류하기 위한 값입니다. |

### Request Example
```json
{}
```

### Response Example
```json
{
    "acctNo": "0123456789"
    "return_code":0,
    "return_msg":"정상적으로 처리되었습니다"
}
```

---

## [ka00198] 실시간종목조회순위
- **메뉴 위치**: 국내주식 > 종목정보 > 실시간종목조회순위(ka00198)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/stkinfo`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 실시간 종목 순위 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `qry_tp` | 구분 |  | Y | 1 | 1:1분, 2:10분, 3:1시간, 4:당일 누적, 5:30초 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `item_inq_rank` | 실시간종목조회순위 |  | N |  |  |
| Body | `- stk_nm` | 종목명 |  | N | 40 |  |
| Body | `- bigd_rank` | 빅데이터 순위 |  | N | 20 | 0: 순위 변동 없음 |
| Body | `- rank_chg` | 순위 등락 |  | N | 20 | 순위 변동 없음(rank_chg=0)인 경우 빈값('') 출력 |
| Body | `- rank_chg_sign` | 순위 등락 부호 |  | N | 20 | 순위상승: +, 순위하락: -, 순위변동없음: ' |
| Body | `- past_curr_prc` | 과거 현재가 |  | N | 20 | 기준 시점 주가, 부호가 포함된 원화 값 |
| Body | `- base_comp_sign` | 기준가 대비 부호 |  | N | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| Body | `- base_comp_chgr` | 기준가 대비 등락율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- prev_base_sign` | 직전 기준 대비 부호 |  | N | 20 |  |
| Body | `- prev_base_chgr` | 직전 기준 대비 등락율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- dt` | 일자 |  | N | 20 | 기준 일자, YYYYMMDD |
| Body | `- tm` | 시간 |  | N | 20 | 기준 시간, HHmmss |
| Body | `- stk_cd` | 종목코드 |  | N | 20 |  |

### Request Example
```json
{
    "qry_tp": "1"
}
```

### Response Example
```json
{
    "item_inq_rank": [
        {
            "stk_nm": "키움증권",
            "bigd_rank": "1",
            "rank_chg": "0",
            "rank_chg_sign": "N",
            "past_curr_prc": "+70700",
            "base_comp_sign": "2",
            "base_comp_chgr": "+0.57",
            "prev_base_sign": "3",
            "prev_base_chgr": "0.00",
            "dt": "20250827",
            "tm": "085900",
            "stk_cd": "005930"
        },
        {
            "stk_nm": "키움증권",
            "bigd_rank": "2",
            "rank_chg": "-1",
            "rank_chg_sign": "-",
            "past_curr_prc": "+206000",
            "base_comp_sign": "2",
            "base_comp_chgr": "+0.49",
            "prev_base_sign": "3",
            "prev_base_chgr": "0.00",
            "dt": "20250827",
            "tm": "085900",
            "stk_cd": "039490"
        },
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka01690] 일별잔고수익률
- **메뉴 위치**: 국내주식 > 계좌 > 일별잔고수익률(ka01690)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 해당 API는 영웅문4 [1690] 자동일지(T) - 일별 잔고 수익률 화면과 같은 데이터를 제공합니다.

해당 API는 모의투자를 지원하지 않습니다

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `qry_dt` | 조회일자 |  | Y | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `dt` | 일자 |  | N | 20 | YYYYMMDD |
| Body | `tot_buy_amt` | 총 매입가 |  | N | 20 | 단위 : 원 |
| Body | `tot_evlt_amt` | 총 평가금액 |  | N | 20 | 단위 : 원 |
| Body | `tot_evltv_prft` | 총 평가손익 |  | N | 20 | 단위 : 원 |
| Body | `tot_prft_rt` | 수익률 |  | N | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `dbst_bal` | 예수금 |  | N | 20 | 단위 : 원 |
| Body | `day_stk_asst` | 추정자산 |  | N | 20 | 단위 : 원 |
| Body | `buy_wght` | 현금비중 |  | N | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `day_bal_rt` | 일별잔고수익률 |  | N |  |  |
| Body | `- cur_prc` | 현재가 |  | N | 20 | 단위 : 원 |
| Body | `- stk_cd` | 종목코드 |  | N | 20 |  |
| Body | `- stk_nm` | 종목명 |  | N | 20 |  |
| Body | `- rmnd_qty` | 보유 수량 |  | N | 20 | 단위 : 1주 |
| Body | `- buy_uv` | 매입 단가 |  | N | 20 | 단위 : 원 |
| Body | `- buy_wght` | 매수비중 |  | N | 20 | 단위: %, 소수점 첫째 자리까지 포맷된 백분율 |
| Body | `- evltv_prft` | 평가손익 |  | N | 20 | 단위 : 원 |
| Body | `- prft_rt` | 수익률 |  | N | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- evlt_amt` | 평가금액 |  | N | 20 | 단위 : 원 |
| Body | `- evlt_wght` | 평가비중 |  | N | 20 | 단위: %, 소수점 첫째 자리까지 포맷된 백분율 |

### Request Example
```json
{
    "qry_dt": "20250825"
}
```

### Response Example
```json
{
    "dt": "20250306",
    "tot_buy_amt": "192328073",
    "tot_evlt_amt": "0",
    "tot_evltv_prft": "-192359839",
    "tot_prft_rt": "-100.02",
    "dbst_bal": "0",
    "day_stk_asst": "0",
    "buy_wght": "0.00",
    "day_bal_rt": [
        {
            "cur_prc": "0",
            "stk_cd": "205100",
            "stk_nm": "엑셈",
            "rmnd_qty": "117478",
            "buy_uv": "1362",
            "buy_wght": "83.2",
            "evltv_prft": "-160071534",
            "prft_rt": "-100.01",
            "evlt_amt": "0",
            "evlt_wght": "0.0"
        },
        {
            "cur_prc": "0",
            "stk_cd": "005930",
            "stk_nm": "삼성전자",
            "rmnd_qty": "187",
            "buy_uv": "78526",
            "buy_wght": "7.6",
            "evltv_prft": "-14689466",
            "prft_rt": "-100.04",
            "evlt_amt": "0",
            "evlt_wght": "0.0"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka10001] 주식기본정보요청
- **메뉴 위치**: 국내주식 > 종목정보 > 주식기본정보요청(ka10001)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/stkinfo`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 종목 코드로 주식 기본 정보를 조회한다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | Y | 20 | 거래소별 종목코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `stk_cd` | 종목코드 |  | N | 20 |  |
| Body | `stk_nm` | 종목명 |  | N | 40 |  |
| Body | `setl_mm` | 결산월 |  | N | 20 |  |
| Body | `fav` | 액면가 |  | N | 20 | 단위: 원 |
| Body | `cap` | 자본금 |  | N | 20 | 단위: 억원 |
| Body | `flo_stk` | 상장주식 |  | N | 20 | 단위: 천원 |
| Body | `crd_rt` | 신용비율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `oyr_hgst` | 연중최고 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `oyr_lwst` | 연중최저 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `mac` | 시가총액 |  | N | 20 | 단위: 억원 |
| Body | `mac_wght` | 시가총액비중 |  | N | 20 |  |
| Body | `for_exh_rt` | 외인소진률 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `repl_pric` | 대용가 |  | N | 20 | 단위: 원 |
| Body | `per` | PER |  | N | 20 | [ 주의 ] PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| Body | `eps` | EPS |  | N | 20 |  |
| Body | `roe` | ROE |  | N | 20 | [ 주의 ]  PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| Body | `pbr` | PBR |  | N | 20 |  |
| Body | `ev` | EV |  | N | 20 |  |
| Body | `bps` | BPS |  | N | 20 |  |
| Body | `sale_amt` | 매출액 |  | N | 20 | 단위: 억원 |
| Body | `bus_pro` | 영업이익 |  | N | 20 | 단위: 억원 |
| Body | `cup_nga` | 당기순이익 |  | N | 20 | 단위: 억원 |
| Body | `250hgst` | 250최고 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `250lwst` | 250최저 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `high_pric` | 고가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `open_pric` | 시가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `low_pric` | 저가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `upl_pric` | 상한가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `lst_pric` | 하한가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `base_pric` | 기준가 |  | N | 20 | 단위: 원 |
| Body | `exp_cntr_pric` | 예상체결가 |  | N | 20 |  |
| Body | `exp_cntr_qty` | 예상체결수량 |  | N | 20 |  |
| Body | `250hgst_pric_dt` | 250최고가일 |  | N | 20 | YYYYMMDD |
| Body | `250hgst_pric_pre_rt` | 250최고가대비율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `250lwst_pric_dt` | 250최저가일 |  | N | 20 | YYYYMMDD |
| Body | `250lwst_pric_pre_rt` | 250최저가대비율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `cur_prc` | 현재가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `pre_sig` | 대비기호 |  | N | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| Body | `pred_pre` | 전일대비 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `flu_rt` | 등락율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `trde_qty` | 거래량 |  | N | 20 | 단위: 1주 |
| Body | `trde_pre` | 거래대비 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `fav_unit` | 액면가단위 |  | N | 20 |  |
| Body | `dstr_stk` | 유통주식 |  | N | 20 | 단위: 1주 |
| Body | `dstr_rt` | 유통비율 |  | N | 20 | 단위: %, 부호 포함 소수점 첫째 자리까지 포맷된 백분율 |

### Request Example
```json
{
    "stk_cd": "005930"
}
```

### Response Example
```json
{
    "stk_cd": "005930",
    "stk_nm": "삼성전자",
    "setl_mm": "12",
    "fav": "5000",
    "cap": "1311",
    "flo_stk": "25527",
    "crd_rt": "+0.08",
    "oyr_hgst": "+181400",
    "oyr_lwst": "-91200",
    "mac": "24352",
    "mac_wght": "",
    "for_exh_rt": "0.00",
    "repl_pric": "66780",
    "per": "",
    "eps": "",
    "roe": "",
    "pbr": "",
    "ev": "",
    "bps": "-75300",
    "sale_amt": "0",
    "bus_pro": "0",
    "cup_nga": "0",
    "250hgst": "+124000",
    "250lwst": "-66800",
    "high_pric": "95400",
    "open_pric": "-0",
    "low_pric": "0",
    "upl_pric": "20241016",
    "lst_pric": "-47.41",
    "base_pric": "20231024",
    "exp_cntr_pric": "+26.69",
    "exp_cntr_qty": "95400",
    "250hgst_pric_dt": "3",
    "250hgst_pric_pre_rt": "0",
    "250lwst_pric_dt": "0.00",
    "250lwst_pric_pre_rt": "0",
    "cur_prc": "0.00",
    "pre_sig": "",
    "pred_pre": "",
    "flu_rt": "0",
    "trde_qty": "0",
    "trde_pre": "0",
    "fav_unit": "0",
    "dstr_stk": "0",
    "dstr_rt": "0",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka10004] 주식호가요청
- **메뉴 위치**: 국내주식 > 시세 > 주식호가요청(ka10004)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/mrkcond`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 종목 코드로 호가 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | Y | 20 | 거래소별 종목코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `bid_req_base_tm` | 호가잔량기준시간 |  | N | 20 | YYYYMMDD |
| Body | `sel_10th_pre_req_pre` | 매도10차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_10th_pre_req` | 매도10차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_10th_pre_bid` | 매도10차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_9th_pre_req_pre` | 매도9차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_9th_pre_req` | 매도9차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_9th_pre_bid` | 매도9차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_8th_pre_req_pre` | 매도8차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_8th_pre_req` | 매도8차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_8th_pre_bid` | 매도8차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_7th_pre_req_pre` | 매도7차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_7th_pre_req` | 매도7차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_7th_pre_bid` | 매도7차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_6th_pre_req_pre` | 매도6차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_6th_pre_req` | 매도6차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_6th_pre_bid` | 매도6차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_5th_pre_req_pre` | 매도5차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_5th_pre_req` | 매도5차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_5th_pre_bid` | 매도5차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_4th_pre_req_pre` | 매도4차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_4th_pre_req` | 매도4차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_4th_pre_bid` | 매도4차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_3th_pre_req_pre` | 매도3차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_3th_pre_req` | 매도3차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_3th_pre_bid` | 매도3차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_2th_pre_req_pre` | 매도2차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_2th_pre_req` | 매도2차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_2th_pre_bid` | 매도2차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `sel_1th_pre_req_pre` | 매도1차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `sel_fpr_req` | 매도최우선잔량 |  | N | 20 | 단위: 1주 |
| Body | `sel_fpr_bid` | 매도최우선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_fpr_bid` | 매수최우선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_fpr_req` | 매수최우선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_1th_pre_req_pre` | 매수1차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_2th_pre_bid` | 매수2차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_2th_pre_req` | 매수2차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_2th_pre_req_pre` | 매수2차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_3th_pre_bid` | 매수3차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_3th_pre_req` | 매수3차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_3th_pre_req_pre` | 매수3차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_4th_pre_bid` | 매수4차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_4th_pre_req` | 매수4차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_4th_pre_req_pre` | 매수4차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_5th_pre_bid` | 매수5차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_5th_pre_req` | 매수5차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_5th_pre_req_pre` | 매수5차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_6th_pre_bid` | 매수6차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_6th_pre_req` | 매수6차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_6th_pre_req_pre` | 매수6차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_7th_pre_bid` | 매수7차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_7th_pre_req` | 매수7차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_7th_pre_req_pre` | 매수7차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_8th_pre_bid` | 매수8차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_8th_pre_req` | 매수8차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_8th_pre_req_pre` | 매수8차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_9th_pre_bid` | 매수9차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_9th_pre_req` | 매수9차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_9th_pre_req_pre` | 매수9차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `buy_10th_pre_bid` | 매수10차선호가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `buy_10th_pre_req` | 매수10차선잔량 |  | N | 20 | 단위: 1주 |
| Body | `buy_10th_pre_req_pre` | 매수10차선잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `tot_sel_req_jub_pre` | 총매도잔량직전대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `tot_sel_req` | 총매도잔량 |  | N | 20 | 단위: 1주 |
| Body | `tot_buy_req` | 총매수잔량 |  | N | 20 | 단위: 1주 |
| Body | `tot_buy_req_jub_pre` | 총매수잔량직전대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `ovt_sel_req_pre` | 시간외매도잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자 |
| Body | `ovt_sel_req` | 시간외매도잔량 |  | N | 20 | 단위: 1주, 시간외 매도호가 총잔량 |
| Body | `ovt_buy_req` | 시간외매수잔량 |  | N | 20 | 단위: 1주, 시간외 매수호가 총잔량 |
| Body | `ovt_buy_req_pre` | 시간외매수잔량대비 |  | N | 20 | 단위: 1주, 부호가 포함된 숫자, 시간외 매수호가 총잔량 직전대비 |

### Request Example
```json
{
    "stk_cd": "005930"
}
```

### Response Example
```json
{
    "bid_req_base_tm": "162000",
    "sel_10th_pre_req_pre": "0",
    "sel_10th_pre_req": "0",
    "sel_10th_pre_bid": "0",
    "sel_9th_pre_req_pre": "0",
    "sel_9th_pre_req": "0",
    "sel_9th_pre_bid": "0",
    "sel_8th_pre_req_pre": "0",
    "sel_8th_pre_req": "0",
    "sel_8th_pre_bid": "0",
    "sel_7th_pre_req_pre": "0",
    "sel_7th_pre_req": "0",
    "sel_7th_pre_bid": "0",
    "sel_6th_pre_req_pre": "0",
    "sel_6th_pre_req": "0",
    "sel_6th_pre_bid": "0",
    "sel_5th_pre_req_pre": "0",
    "sel_5th_pre_req": "0",
    "sel_5th_pre_bid": "0",
    "sel_4th_pre_req_pre": "0",
    "sel_4th_pre_req": "0",
    "sel_4th_pre_bid": "0",
    "sel_3th_pre_req_pre": "0",
    "sel_3th_pre_req": "0",
    "sel_3th_pre_bid": "0",
    "sel_2th_pre_req_pre": "0",
    "sel_2th_pre_req": "0",
    "sel_2th_pre_bid": "0",
    "sel_1th_pre_req_pre": "0",
    "sel_fpr_req": "0",
    "sel_fpr_bid": "0",
    "buy_fpr_bid": "0",
    "buy_fpr_req": "0",
    "buy_1th_pre_req_pre": "0",
    "buy_2th_pre_bid": "0",
    "buy_2th_pre_req": "0",
    "buy_2th_pre_req_pre": "0",
    "buy_3th_pre_bid": "0",
    "buy_3th_pre_req": "0",
    "buy_3th_pre_req_pre": "0",
    "buy_4th_pre_bid": "0",
    "buy_4th_pre_req": "0",
    "buy_4th_pre_req_pre": "0",
    "buy_5th_pre_bid": "0",
    "buy_5th_pre_req": "0",
    "buy_5th_pre_req_pre": "0",
    "buy_6th_pre_bid": "0",
    "buy_6th_pre_req": "0",
    "buy_6th_pre_req_pre": "0",
    "buy_7th_pre_bid": "0",
    "buy_7th_pre_req": "0",
    "buy_7th_pre_req_pre": "0",
    "buy_8th_pre_bid": "0",
    "buy_8th_pre_req": "0",
    "buy_8th_pre_req_pre": "0",
    "buy_9th_pre_bid": "0",
    "buy_9th_pre_req": "0",
    "buy_9th_pre_req_pre": "0",
    "buy_10th_pre_bid": "0",
    "buy_10th_pre_req": "0",
    "buy_10th_pre_req_pre": "0",
    "tot_sel_req_jub_pre": "0",
    "tot_sel_req": "0",
    "tot_buy_req": "0",
    "tot_buy_req_jub_pre": "0",
    "ovt_sel_req_pre": "0",
    "ovt_sel_req": "0",
    "ovt_buy_req": "0",
    "ovt_buy_req_pre": "0",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka10072] 일자별종목별실현손익요청_일자
- **메뉴 위치**: 국내주식 > 계좌 > 일자별종목별실현손익요청_일자(ka10072)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 일자, 종목코드로 실현손익 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | N | 6 | 종목코드 6자리 |
| Body | `strt_dt` | 시작일자 |  | Y | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `dt_stk_div_rlzt_pl` | 일자별종목별실현손익 |  | N |  |  |
| Body | `- stk_nm` | 종목명 |  | N | 40 |  |
| Body | `- cntr_qty` | 체결량 |  | N | 20 | 단위: 1주 |
| Body | `- buy_uv` | 매입단가 |  | N | 20 | 단위: 원 |
| Body | `- cntr_pric` | 체결가 |  | N | 20 | 단위: 원 |
| Body | `- tdy_sel_pl` | 당일매도손익 |  | N | 20 | 단위: 원 |
| Body | `- pl_rt` | 손익율 |  | N | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- stk_cd` | 종목코드 |  | N | 20 | 종목코드 6자리 |
| Body | `- tdy_trde_cmsn` | 당일매매수수료 |  | N | 20 | 단위: 원 |
| Body | `- tdy_trde_tax` | 당일매매세금 |  | N | 20 | 단위: 원 |
| Body | `- wthd_alowa` | 인출가능금액 |  | N | 20 | 단위: 원 |
| Body | `- loan_dt` | 대출일 |  | N | 20 | YYYYMMDD |
| Body | `- crd_tp` | 신용구분 |  | N | 20 |  |
| Body | `- stk_cd_1` | 종목코드1 |  | N | 20 |  |
| Body | `- tdy_sel_pl_1` | 당일매도손익1 |  | N | 20 |  |

### Request Example
```json
{
    "stk_cd": "005930",
    "strt_dt": "20241128"
}
```

### Response Example
```json
{
    "dt_stk_div_rlzt_pl": [
        {
            "stk_nm": "삼성전자",
            "cntr_qty": "1",
            "buy_uv": "97602.96",
            "cntr_pric": "158200",
            "tdy_sel_pl": "59813.04",
            "pl_rt": "+61.28",
            "stk_cd": "A005930",
            "tdy_trde_cmsn": "500",
            "tdy_trde_tax": "284",
            "wthd_alowa": "0",
            "loan_dt": "",
            "crd_tp": "현금잔고",
            "stk_cd_1": "A005930",
            "tdy_sel_pl_1": "59813.04"
        },
        {
            "stk_nm": "삼성전자",
            "cntr_qty": "1",
            "buy_uv": "97602.96",
            "cntr_pric": "158200",
            "tdy_sel_pl": "59813.04",
            "pl_rt": "+61.28",
            "stk_cd": "A005930",
            "tdy_trde_cmsn": "500",
            "tdy_trde_tax": "284",
            "wthd_alowa": "0",
            "loan_dt": "",
            "crd_tp": "현금잔고",
            "stk_cd_1": "A005930",
            "tdy_sel_pl_1": "59813.04"
        }
    ],
    "return_code": 0,
    "return_msg": " 조회가 완료되었습니다."
}
```

---

## [ka10073] 일자별종목별실현손익요청_기간
- **메뉴 위치**: 국내주식 > 계좌 > 일자별종목별실현손익요청_기간(ka10073)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 종목코드와 기간을 설정하여 실현 손익 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | N | 6 | 종목코드 6자리 |
| Body | `strt_dt` | 시작일자 |  | Y | 8 | YYYYMMDD |
| Body | `end_dt` | 종료일자 |  | Y | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `dt_stk_rlzt_pl` | 일자별종목별실현손익 |  | N |  |  |
| Body | `- dt` | 일자 |  | N | 20 | YYYYMMDD |
| Body | `- tdy_htssel_cmsn` | 당일hts매도수수료 |  | N | 20 | 단위: 원 |
| Body | `- stk_nm` | 종목명 |  | N | 40 |  |
| Body | `- cntr_qty` | 체결량 |  | N | 20 | 단위: 1주 |
| Body | `- buy_uv` | 매입단가 |  | N | 20 | 단위: 원 |
| Body | `- cntr_pric` | 체결가 |  | N | 20 | 단위: 원 |
| Body | `- tdy_sel_pl` | 당일매도손익 |  | N | 20 | 단위: 원 |
| Body | `- pl_rt` | 손익율 |  | N | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- stk_cd` | 종목코드 |  | N | 20 | 종목코드 6자리 |
| Body | `- tdy_trde_cmsn` | 당일매매수수료 |  | N | 20 | 단위: 원 |
| Body | `- tdy_trde_tax` | 당일매매세금 |  | N | 20 | 단위: 원 |
| Body | `- wthd_alowa` | 인출가능금액 |  | N | 20 | 단위: 원 |
| Body | `- loan_dt` | 대출일 |  | N | 20 | YYYYMMDD |
| Body | `- crd_tp` | 신용구분 |  | N | 20 |  |

### Request Example
```json
{
    "stk_cd": "005930",
    "strt_dt": "20241128",
    "end_dt": "20241128"
}
```

### Response Example
```json
{
    "dt_stk_rlzt_pl": [
        {
            "dt": "20241128",
            "tdy_htssel_cmsn": "현금",
            "stk_nm": "삼성전자",
            "cntr_qty": "1",
            "buy_uv": "97602.96",
            "cntr_pric": "158200",
            "tdy_sel_pl": "59813.04",
            "pl_rt": "+61.28",
            "stk_cd": "A005930",
            "tdy_trde_cmsn": "500",
            "tdy_trde_tax": "284",
            "wthd_alowa": "0",
            "loan_dt": "",
            "crd_tp": "현금잔고"
        },
        {
            "dt": "20241128",
            "tdy_htssel_cmsn": "현금",
            "stk_nm": "삼성전자",
            "cntr_qty": "1",
            "buy_uv": "97602.96",
            "cntr_pric": "158200",
            "tdy_sel_pl": "59813.04",
            "pl_rt": "+61.28",
            "stk_cd": "A005930",
            "tdy_trde_cmsn": "500",
            "tdy_trde_tax": "284",
            "wthd_alowa": "0",
            "loan_dt": "",
            "crd_tp": "현금잔고"
        },
        {
            "dt": "20241128",
            "tdy_htssel_cmsn": "현금",
            "stk_nm": "삼성전자",
            "cntr_qty": "1",
            "buy_uv": "97602.96",
            "cntr_pric": "158200",
            "tdy_sel_pl": "59813.04",
            "pl_rt": "+61.28",
            "stk_cd": "A005930",
            "tdy_trde_cmsn": "500",
            "tdy_trde_tax": "284",
            "wthd_alowa": "0",
            "loan_dt": "",
            "crd_tp": "현금잔고"
        }
    ],
    "return_code": 0,
    "return_msg": " 조회가 완료되었습니다."
}
```

---

## [ka10074] 일자별실현손익요청
- **메뉴 위치**: 국내주식 > 계좌 > 일자별실현손익요청(ka10074)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 기간을 설정하고 해당 기간에 대한 실현 손익 정보를 조회합니다.
[ 주의 ] 실현손익이 발생한 일자에대해서만 데이터가 채워짐.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `strt_dt` | 시작일자 |  | Y | 8 | YYYYMMDD |
| Body | `end_dt` | 종료일자 |  | Y | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `tot_buy_amt` | 총매수금액 |  | N |  | 단위: 원 |
| Body | `tot_sell_amt` | 총매도금액 |  | N |  | 단위: 원 |
| Body | `rlzt_pl` | 실현손익 |  | N |  | 단위: 원 |
| Body | `trde_cmsn` | 매매수수료 |  | N |  | 단위: 원 |
| Body | `trde_tax` | 매매세금 |  | N |  | 단위: 원 |
| Body | `dt_rlzt_pl` | 일자별실현손익 |  | N |  |  |
| Body | `- dt` | 일자 |  | N | 20 | YYYYMMDD |
| Body | `- buy_amt` | 매수금액 |  | N | 20 | 단위: 원 |
| Body | `- sell_amt` | 매도금액 |  | N | 20 | 단위: 원 |
| Body | `- tdy_sel_pl` | 당일매도손익 |  | N | 20 | 단위: 원 |
| Body | `- tdy_trde_cmsn` | 당일매매수수료 |  | N | 20 | 단위: 원 |
| Body | `- tdy_trde_tax` | 당일매매세금 |  | N | 20 | 단위: 원 |

### Request Example
```json
{
    "strt_dt": "20241128",
    "end_dt": "20241128"
}
```

### Response Example
```json
{
    "tot_buy_amt": "0",
    "tot_sell_amt": "474600",
    "rlzt_pl": "179419",
    "trde_cmsn": "940",
    "trde_tax": "852",
    "dt_rlzt_pl": [
        {
            "dt": "20241128",
            "buy_amt": "0",
            "sell_amt": "474600",
            "tdy_sel_pl": "179419",
            "tdy_trde_cmsn": "940",
            "tdy_trde_tax": "852"
        }
    ],
    "return_code": 0,
    "return_msg": " 조회가 완료되었습니다."
}
```

---

## [ka10080] 주식분봉차트조회요청
- **메뉴 위치**: 국내주식 > 차트 > 주식분봉차트조회요청(ka10080)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/chart`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 주식 분봉 차트 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | Y | 20 | 거래소별 종목코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| Body | `tic_scope` | 틱범위 |  | Y | 2 | 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분 |
| Body | `upd_stkpc_tp` | 수정주가구분 |  | Y | 1 | 0 or 1 |
| Body | `base_dt` | 기준일자 |  | N | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `stk_cd` | 종목코드 |  | N | 6 |  |
| Body | `stk_min_pole_chart_qry` | 주식분봉차트조회 |  | N |  |  |
| Body | `- cur_prc` | 현재가(종가) |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `- trde_qty` | 거래량 |  | N | 20 | 단위: 1주 |
| Body | `- cntr_tm` | 체결시간 |  | N | 20 | YYYYMMDDHHmmss |
| Body | `- open_pric` | 시가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `- high_pric` | 고가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `- low_pric` | 저가 |  | N | 20 | 단위: 원, 부호가 포함된 숫자 |
| Body | `- pred_pre` | 전일대비 |  | N | 20 | 현재가 - 전일종가 |
| Body | `- pred_pre_sig` | 전일대비 기호 |  | N | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |

### Request Example
```json
{
    "stk_cd": "005930",
    "tic_scope": "1",
    "upd_stkpc_tp": "1",
    "base_dt": "20260202"
}
```

### Response Example
```json
{
    "stk_cd": "005930",
    "stk_min_pole_chart_qry": [
        {
            "cur_prc": "-78800",
            "trde_qty": "7913",
            "cntr_tm": "20250917132000",
            "open_pric": "-78850",
            "high_pric": "-78900",
            "low_pric": "-78800",
            "acc_trde_qty": "14947571",
            "pred_pre": "-600",
            "pred_pre_sig": "5"
        },
        {
            "cur_prc": "-78900",
            "trde_qty": "16084",
            "cntr_tm": "20250917131900",
            "open_pric": "-78900",
            "high_pric": "-78900",
            "low_pric": "-78800",
            "acc_trde_qty": "14939658",
            "pred_pre": "-500",
            "pred_pre_sig": "5"
        },
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka10081] 주식일봉차트조회요청
- **메뉴 위치**: 국내주식 > 차트 > 주식일봉차트조회요청(ka10081)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/chart`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 주식 일봉 차트 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | Y | 20 | 거래소별 종목코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| Body | `base_dt` | 기준일자 |  | Y | 8 | YYYYMMDD |
| Body | `upd_stkpc_tp` | 수정주가구분 |  | Y | 1 | 0 or 1 / 수정주가 적용을 원하시는 경우, 권리발생일 이후 일자를 base_dt에 넣어 조회 또는 연속조회해주시기 바랍니다. 예를 들어 삼성전자 2018년 05월 04일 (액면분할 권리발생일)을 base_dt에 넣고 수정주가적용(1)로 조회하면 2018년 05월 04일 이전 데이터는 수정주가 적용된 3만원대 가격이 나옵니다. 연속조회도 동일합니다. 권리 발생일 이전인 2018년 05월 03일 이전 일자로 base_dt 조회 시 수정주가 적용되지 않아 200만원 이상 가격대가 나옵니다. 수정주가 적용을 원하는 과거 차트 데이터 조회를 위해서는 해당 권리발생일 이후로 base_dt를 세팅하고, 수정주가 적용(1)로 세팅하고 조회 및 연속조회하여야합니다. |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `stk_cd` | 종목코드 |  | N | 6 |  |
| Body | `stk_dt_pole_chart_qry` | 주식일봉차트조회 |  | N |  |  |
| Body | `- cur_prc` | 현재가 |  | N | 20 | 단위: 원 |
| Body | `- trde_qty` | 거래량 |  | N | 20 | 단위: 1주 |
| Body | `- trde_prica` | 거래대금 |  | N | 20 | 단위: 백만원 |
| Body | `- dt` | 일자 |  | N | 20 | YYYYMMDD |
| Body | `- open_pric` | 시가 |  | N | 20 | 단위: 원 |
| Body | `- high_pric` | 고가 |  | N | 20 | 단위: 원 |
| Body | `- low_pric` | 저가 |  | N | 20 | 단위: 원 |
| Body | `- pred_pre` | 전일대비 |  | N | 20 | 현재가 - 전일종가 |
| Body | `- pred_pre_sig` | 전일대비기호 |  | N | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| Body | `- trde_tern_rt` | 거래회전율 |  | N | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

### Request Example
```json
{
    "stk_cd": "005930",
    "base_dt": "20250908",
    "upd_stkpc_tp": "1"
}
```

### Response Example
```json
{
    "stk_cd": "005930",
    "stk_dt_pole_chart_qry": [
        {
            "cur_prc": "70100",
            "trde_qty": "9263135",
            "trde_prica": "648525",
            "dt": "20250908",
            "open_pric": "69800",
            "high_pric": "70500",
            "low_pric": "69600",
            "pred_pre": "+600",
            "pred_pre_sig": "2",
            "trde_tern_rt": "+0.16"
        },
        {
            "cur_prc": "69500",
            "trde_qty": "11526724",
            "trde_prica": "804642",
            "dt": "20250905",
            "open_pric": "70300",
            "high_pric": "70400",
            "low_pric": "69500",
            "pred_pre": "-600",
            "pred_pre_sig": "5",
            "trde_tern_rt": "+0.19"
        },
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ka10099] 종목정보 리스트
- **메뉴 위치**: 국내주식 > 종목정보 > 종목정보 리스트(ka10099)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/stkinfo`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 시장을 선택하여 종목 리스트를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `mrkt_tp` | 시장구분 |  | Y | 2 | 0 : 코스피,<br>10 : 코스닥,<br>30 : K-OTC,<br>50 : 코넥스,<br>60 : ETN,<br>70 : 손실제한 ETN,<br>80 : 금현물,<br>90 : 변동성 ETN,<br>2 : 인프라투융자,<br>3 : ELW,<br>4 : 뮤추얼펀드,<br>5 : 신주인수권,<br>6 : 리츠종목,<br>7 : 신주인수권증서,<br>8 : ETF,<br>9 : 하이일드펀드 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `list` | 종목리스트 |  | N |  |  |
| Body | `- code` | 종목코드 |  | N | 20 | 단축코드 |
| Body | `- name` | 종목명 |  | N | 40 |  |
| Body | `- listCount` | 상장주식수 |  | N | 20 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 16자리 숫자 |
| Body | `- auditInfo` | 감리구분 |  | N | 20 |  |
| Body | `- regDay` | 상장일 |  | N | 20 | YYYYMMDD |
| Body | `- lastPrice` | 전일종가 |  | N | 20 | 단위: 원, 좌측 0-padding 처리된 부호 포함 8자리 숫자 |
| Body | `- state` | 종목상태 |  | N | 20 |  |
| Body | `- marketCode` | 시장구분코드 |  | N | 20 |  |
| Body | `- marketName` | 시장명 |  | N | 20 |  |
| Body | `- upName` | 업종명 |  | N | 20 |  |
| Body | `- upSizeName` | 회사크기분류 |  | N | 20 |  |
| Body | `- orderWarning` | 투자유의종목여부 |  | N | 20 | 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달 |
| Body | `- companyClassName` | 회사분류 |  | N | 20 | 코스닥만 존재함 |
| Body | `- nxtEnable` | NXT가능여부 |  | N | 20 | Y: 가능 |

### Request Example
```json
{
    "mrkt_tp": "0"
}
```

### Response Example
```json
{
    "return_msg": "정상적으로 처리되었습니다",
    "return_code": 0,
    "list": [
        {
            "code": "005930",
            "name": "삼성전자",
            "listCount": "0000000123759593",
            "auditInfo": "투자주의환기종목",
            "regDay": "20091204",
            "lastPrice": "00000197",
            "state": "관리종목",
            "marketCode": "10",
            "marketName": "코스닥",
            "upName": "",
            "upSizeName": "",
            "companyClassName": "",
            "orderWarning": "0",
            "nxtEnable": "Y"
        },
        {
            "code": "005930",
            "name": "삼성전자",
            "listCount": "0000000136637536",
            "auditInfo": "정상",
            "regDay": "20100423",
            "lastPrice": "00000213",
            "state": "증거금100%",
            "marketCode": "10",
            "marketName": "코스닥",
            "upName": "",
            "upSizeName": "",
            "companyClassName": "외국기업",
            "orderWarning": "0",
            "nxtEnable": "Y"
        },
        {
            "code": "005930",
            "name": "삼성전자",
            "listCount": "0000000080000000",
            "auditInfo": "정상",
            "regDay": "20160818",
            "lastPrice": "00000614",
            "state": "증거금100%",
            "marketCode": "10",
            "marketName": "코스닥",
            "upName": "",
            "upSizeName": "",
            "companyClassName": "외국기업",
            "orderWarning": "0",
            "nxtEnable": "Y"
        },
        {
            "code": "005930",
            "name": "삼성전자",
            "listCount": "0000000141781250",
            "auditInfo": "정상",
            "regDay": "20160630",
            "lastPrice": "00000336",
            "state": "증거금100%",
            "marketCode": "10",
            "marketName": "코스닥",
            "upName": "",
            "upSizeName": "",
            "companyClassName": "외국기업",
            "orderWarning": "0",
            "nxtEnable": "Y"
        },
        {
            "code": "005930",
            "name": "삼성전자",
            "listCount": "0000000067375000",
            "auditInfo": "투자주의환기종목",
            "regDay": "20161025",
            "lastPrice": "00000951",
            "state": "관리종목",
            "marketCode": "10",
            "marketName": "코스닥",
            "upName": "",
            "upSizeName": "",
            "companyClassName": "",
            "orderWarning": "0",
            "nxtEnable": "Y"
        }
    ]
}
```

---

## [ka10171] 조건검색 목록조회
- **메뉴 위치**: 국내주식 > 조건검색 > 조건검색 목록조회(ka10171)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 조건검색은 영웅문4에서 만드실 수 있습니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | TR명 |  | Y | 7 | CNSRLST고정값 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 정상 : 0 |
| Body | `return_msg` | 결과메시지 |  | N |  | 정상인 경우는 메시지 없음 |
| Body | `trnm` | 서비스명 |  | N | 7 | CNSRLST 고정값 |
| Body | `data` | 조건검색식 목록 |  | N |  |  |
| Body | `- seq` | 조건검색식 일련번호 |  | N |  |  |
| Body | `- name` | 조건검색식 명 |  | N |  |  |

### Request Example
```json
{
    "trnm": "CNSRLST"
}
```

### Response Example
```json
{
    'trnm': 'CNSRLST',
    'return_code': 0,
    'return_msg': '',
    'data': [
        ['0','조건1'],
        ['1','조건2'],
        ['2','조건3'],
        ['3','조건4'],
        ['4','조건5']
    ]
}
```

---

## [ka10173] 조건검색 요청 실시간
- **메뉴 위치**: 국내주식 > 조건검색 > 조건검색 요청 실시간(ka10173)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 조건검색 실시간 조회는 시스템 내부구조상 조건검색 목록 조회를 먼저 진행한 후에 실시간 조회를 이용할 수 있습니다. 
조건검색은 영웅문4에서 만드실 수 있습니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y | 7 | CNSRREQ 고정값 |
| Body | `seq` | 조건검색식 일련번호 |  | Y | 3 |  |
| Body | `search_type` | 조회타입 |  | Y | 1 | 1: 조건검색+실시간조건검색 |
| Body | `stex_tp` | 거래소구분 |  | Y | 1 | K:KRX |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `조회 데이터` |  |  |  |  |  |
| Body | `return_code` | 결과코드 |  | N |  | 정상:0 나머지:에러 |
| Body | `return_msg` | 결과메시지 |  | N |  | 정상인 경우는 메시지 없음 |
| Body | `trnm` | 서비스명 |  | N |  | CNSRREQ |
| Body | `seq` | 조건검색식 일련번호 |  | N |  |  |
| Body | `data` | 검색결과데이터 |  | N |  |  |
| Body | `- jmcode` | 종목코드 |  | N |  | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| Body | `실시간 데이터` |  |  |  |  |  |
| Body | `data` | 검색결과데이터 | List<Map> | Y |  |  |
| Body | `trnm` | 서비스명 | String | Y |  | REAL |
| Body | `- type` | 실시간 항목 | String | Y | 2 | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 | String | Y |  | 종목코드 |
| Body | `- values` | 실시간 수신 값 | Object | Y |  |  |
| Body | `- - 841` | 일련번호 | String | Y |  |  |
| Body | `- - 9001` | 종목코드 | String | Y |  |  |
| Body | `- - 843` | 삽입삭제 구분 | String | Y |  | I: 삽입, D: 삭제 |
| Body | `- - 20` | 체결시간 | String | Y |  |  |
| Body | `- - 907` | 매도/수 구분 | String | Y |  |  |

### Request Example
```json
{
    "trnm": "CNSRREQ",
    "seq": "4",
    "search_type": "1",
    "stex_tp": "K"
}
```

### Response Example
```json
#조회데이터
{
    'trnm': 'CNSRREQ',
    'seq': '4',
    'return_code': 0,
    'data': [
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'},
        {'jmcode': 'A005930'}
    ]
}

#실시간데이터
{
    'data': [
        {
            'values': {
                '841': '4',
                '9001': '005930',
                '843': 'I',
                '20': '152028',
                '907': '2'
            },
            'type': '02',
            'name': '조건검색',
            'item': '005930'
        }
    ],
    'trnm': 'REAL'
}
```

---

## [kt00001] 예수금상세현황요청
- **메뉴 위치**: 국내주식 > 계좌 > 예수금상세현황요청(kt00001)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 예수금 상세 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `qry_tp` | 조회구분 |  | Y | 1 | 3:추정조회, 2:일반조회 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `entr` | 예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `profa_ch` | 주식증거금현금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `bncr_profa_ch` | 수익증권증거금현금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `nxdy_bncr_sell_exct` | 익일수익증권매도정산대금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `fc_stk_krw_repl_set_amt` | 해외주식원화대용설정금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnta_ch` | 신용보증금현금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnt_ch` | 신용담보금현금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `add_grnt_ch` | 추가담보금현금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `etc_profa` | 기타증거금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `uncl_stk_amt` | 미수확보금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `shrts_prica` | 공매도대금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_set_grnta` | 신용설정평가금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `chck_ina_amt` | 수표입금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `etc_chck_ina_amt` | 기타수표입금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnt_ruse` | 신용담보재사용 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `knx_asset_evltv` | 코넥스기본예탁금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `elwdpst_evlta` | ELW예탁평가금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_ls_rght_frcs_amt` | 신용대주권리예정금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `lvlh_join_amt` | 생계형가입금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `lvlh_trns_alowa` | 생계형입금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `repl_amt` | 대용금평가금액(합계) |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `remn_repl_evlta` | 잔고대용평가금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `trst_remn_repl_evlta` | 위탁대용잔고평가금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `bncr_remn_repl_evlta` | 수익증권대용평가금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `profa_repl` | 위탁증거금대용 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnta_repl` | 신용보증금대용 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnt_repl` | 신용담보금대용 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `add_grnt_repl` | 추가담보금대용 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `rght_repl_amt` | 권리대용금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `pymn_alow_amt` | 출금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `wrap_pymn_alow_amt` | 랩출금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `ord_alow_amt` | 주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `bncr_buy_alowa` | 수익증권매수가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `20stk_ord_alow_amt` | 20%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `30stk_ord_alow_amt` | 30%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `40stk_ord_alow_amt` | 40%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `100stk_ord_alow_amt` | 100%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `ch_uncla` | 현금미수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `ch_uncla_dlfe` | 현금미수연체료 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `ch_uncla_tot` | 현금미수금합계 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_int_npay` | 신용이자미납 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `int_npay_amt_dlfe` | 신용이자미납연체료 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `int_npay_amt_tot` | 신용이자미납합계 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `etc_loana` | 기타대여금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `etc_loana_dlfe` | 기타대여금연체료 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `etc_loan_tot` | 기타대여금합계 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `nrpy_loan` | 미상환융자금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `loan_sum` | 융자금합계 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `ls_sum` | 대주금합계 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `crd_grnt_rt` | 신용담보비율 |  | N | 15 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `mdstrm_usfe` | 중도이용료 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `min_ord_alow_yn` | 최소주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `loan_remn_evlt_amt` | 대출총평가금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `dpst_grntl_remn` | 예탁담보대출잔고 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `sell_grntl_remn` | 매도담보대출잔고 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_entra` | d+1추정예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_slby_exct_amt` | d+1매도매수정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_buy_exct_amt` | d+1매수정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_out_rep_mor` | d+1미수변제소요금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_sel_exct_amt` | d+1매도정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d1_pymn_alow_amt` | d+1출금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_entra` | d+2추정예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_slby_exct_amt` | d+2매도매수정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_buy_exct_amt` | d+2매수정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_out_rep_mor` | d+2미수변제소요금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_sel_exct_amt` | d+2매도정산금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_pymn_alow_amt` | d+2출금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `50stk_ord_alow_amt` | 50%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `60stk_ord_alow_amt` | 60%종목주문가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `stk_entr_prst` | 종목별예수금 |  | N |  |  |
| Body | `- crnc_cd` | 통화코드 |  | N | 3 | 통화코드 3자리 |
| Body | `- fx_entr` | 외화예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- fc_krw_repl_evlta` | 원화대용평가금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- fc_trst_profa` | 해외주식증거금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- pymn_alow_amt_entr` | 출금가능금액(예수금) |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- pymn_alow_amt` | 출금가능금액 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- ord_alow_amt_entr` | 주문가능금액(예수금) |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- fc_uncla` | 외화미수(합계) |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- fc_ch_uncla` | 외화현금미수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- dly_amt` | 연체료 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- d1_fx_entr` | d+1외화예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- d2_fx_entr` | d+2외화예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- d3_fx_entr` | d+3외화예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `- d4_fx_entr` | d+4외화예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |

### Request Example
```json
{
    "qry_tp": "3"
}
```

### Response Example
```json
{
    "entr": "000000000017534",
    "profa_ch": "000000000032193",
    "bncr_profa_ch": "000000000000000",
    "nxdy_bncr_sell_exct": "000000000000000",
    "fc_stk_krw_repl_set_amt": "000000000000000",
    "crd_grnta_ch": "000000000000000",
    "crd_grnt_ch": "000000000000000",
    "add_grnt_ch": "000000000000000",
    "etc_profa": "000000000000000",
    "uncl_stk_amt": "000000000000000",
    "shrts_prica": "000000000000000",
    "crd_set_grnta": "000000000000000",
    "chck_ina_amt": "000000000000000",
    "etc_chck_ina_amt": "000000000000000",
    "crd_grnt_ruse": "000000000000000",
    "knx_asset_evltv": "000000000000000",
    "elwdpst_evlta": "000000000031269",
    "crd_ls_rght_frcs_amt": "000000000000000",
    "lvlh_join_amt": "000000000000000",
    "lvlh_trns_alowa": "000000000000000",
    "repl_amt": "000000003915500",
    "remn_repl_evlta": "000000003915500",
    "trst_remn_repl_evlta": "000000000000000",
    "bncr_remn_repl_evlta": "000000000000000",
    "profa_repl": "000000000000000",
    "crd_grnta_repl": "000000000000000",
    "crd_grnt_repl": "000000000000000",
    "add_grnt_repl": "000000000000000",
    "rght_repl_amt": "000000000000000",
    "pymn_alow_amt": "000000000085341",
    "wrap_pymn_alow_amt": "000000000000000",
    "ord_alow_amt": "000000000085341",
    "bncr_buy_alowa": "000000000085341",
    "20stk_ord_alow_amt": "000000000012550",
    "30stk_ord_alow_amt": "000000000012550",
    "40stk_ord_alow_amt": "000000000012550",
    "100stk_ord_alow_amt": "000000000012550",
    "ch_uncla": "000000000000000",
    "ch_uncla_dlfe": "000000000000000",
    "ch_uncla_tot": "000000000000000",
    "crd_int_npay": "000000000000000",
    "int_npay_amt_dlfe": "000000000000000",
    "int_npay_amt_tot": "000000000000000",
    "etc_loana": "000000000000000",
    "etc_loana_dlfe": "000000000000000",
    "etc_loan_tot": "000000000000000",
    "nrpy_loan": "000000000000000",
    "loan_sum": "000000000000000",
    "ls_sum": "000000000000000",
    "crd_grnt_rt": "0.00",
    "mdstrm_usfe": "000000000388388",
    "min_ord_alow_yn": "000000000000000",
    "loan_remn_evlt_amt": "000000000000000",
    "dpst_grntl_remn": "000000000000000",
    "sell_grntl_remn": "000000000000000",
    "d1_entra": "000000000017450",
    "d1_slby_exct_amt": "-00000000000084",
    "d1_buy_exct_amt": "000000000048240",
    "d1_out_rep_mor": "000000000000000",
    "d1_sel_exct_amt": "000000000048156",
    "d1_pymn_alow_amt": "000000000012550",
    "d2_entra": "000000000012550",
    "d2_slby_exct_amt": "-00000000004900",
    "d2_buy_exct_amt": "000000000004900",
    "d2_out_rep_mor": "000000000000000",
    "d2_sel_exct_amt": "000000000000000",
    "d2_pymn_alow_amt": "000000000012550",
    "50stk_ord_alow_amt": "000000000012550",
    "60stk_ord_alow_amt": "000000000012550",
    "stk_entr_prst": [],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---

## [kt00004] 계좌평가현황요청
- **메뉴 위치**: 국내주식 > 계좌 > 계좌평가현황요청(kt00004)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 계좌 평가 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `qry_tp` | 상장폐지조회구분 |  | Y | 1 | 0:전체, 1:상장폐지종목제외 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 6 | KRX:한국거래소,NXT:넥스트트레이드 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `acnt_nm` | 계좌명 |  | N | 30 |  |
| Body | `brch_nm` | 지점명 |  | N | 30 |  |
| Body | `entr` | 예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `d2_entra` | D+2추정예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tot_est_amt` | 유가잔고평가액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `aset_evlt_amt` | 예탁자산평가액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tot_pur_amt` | 총매입금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `prsm_dpst_aset_amt` | 추정예탁자산 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tot_grnt_sella` | 매도담보대출금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tdy_lspft_amt` | 당일투자원금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `invt_bsamt` | 당월투자원금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `lspft_amt` | 누적투자원금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tdy_lspft` | 당일투자손익 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `lspft2` | 당월투자손익 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `lspft` | 누적투자손익 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tdy_lspft_rt` | 당일손익율 |  | N | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `lspft_ratio` | 당월손익율 |  | N | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `lspft_rt` | 누적손익율 |  | N | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `stk_acnt_evlt_prst` | 종목별계좌평가현황 |  | N |  |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| Body | `- stk_nm` | 종목명 |  | N | 30 |  |
| Body | `- rmnd_qty` | 보유수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- avg_prc` | 평균단가 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- cur_prc` | 현재가 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- evlt_amt` | 평가금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pl_amt` | 손익금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pl_rt` | 손익율 |  | N | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |
| Body | `- loan_dt` | 대출일 |  | N | 10 | YYYYMMDD |
| Body | `- pur_amt` | 매입금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- setl_remn` | 결제잔고 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pred_buyq` | 전일매수수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pred_sellq` | 전일매도수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- tdy_buyq` | 금일매수수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- tdy_sellq` | 금일매도수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

### Request Example
```json
{
    "qry_tp": "0",
    "dmst_stex_tp": "KRX"
}
```

### Response Example
```json
{
    "acnt_nm": "김키움",
    "brch_nm": "키움은행",
    "entr": "000000017534",
    "d2_entra": "000000012550",
    "tot_est_amt": "000000000342",
    "aset_evlt_amt": "000000761950",
    "tot_pur_amt": "000000002786",
    "prsm_dpst_aset_amt": "000000749792",
    "tot_grnt_sella": "000000000000",
    "tdy_lspft_amt": "000000000000",
    "invt_bsamt": "000000000000",
    "lspft_amt": "000000000000",
    "tdy_lspft": "000000000000",
    "lspft2": "000000000000",
    "lspft": "000000000000",
    "tdy_lspft_rt": "0.00",
    "lspft_ratio": "0.00",
    "lspft_rt": "0.00",
    "stk_acnt_evlt_prst": [
        {
            "stk_cd": "A005930",
            "stk_nm": "삼성전자",
            "rmnd_qty": "000000000003",
            "avg_prc": "000000124500",
            "cur_prc": "000000070000",
            "evlt_amt": "000000209542",
            "pl_amt": "-00000163958",
            "pl_rt": "-43.8977",
            "loan_dt": "",
            "pur_amt": "000000373500",
            "setl_remn": "000000000003",
            "pred_buyq": "000000000000",
            "pred_sellq": "000000000000",
            "tdy_buyq": "000000000000",
            "tdy_sellq": "000000000000"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---

## [kt00005] 체결잔고요청
- **메뉴 위치**: 국내주식 > 계좌 > 체결잔고요청(kt00005)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 체결 잔고 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 6 | KRX:한국거래소,NXT:넥스트트레이드 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `entr` | 예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `entr_d1` | 예수금D+1 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `entr_d2` | 예수금D+2 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `pymn_alow_amt` | 출금가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `uncl_stk_amt` | 미수확보금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `repl_amt` | 대용금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `rght_repl_amt` | 권리대용금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `ord_alowa` | 주문가능현금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `ch_uncla` | 현금미수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `crd_int_npay_gold` | 신용이자미납금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `etc_loana` | 기타대여금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `nrpy_loan` | 미상환융자금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `profa_ch` | 증거금현금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `repl_profa` | 증거금대용 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `stk_buy_tot_amt` | 주식매수총액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `evlt_amt_tot` | 평가금액합계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tot_pl_tot` | 총손익합계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `tot_pl_rt` | 총손익률 |  | N | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |
| Body | `tot_re_buy_alowa` | 총재매수가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `20ord_alow_amt` | 20%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `30ord_alow_amt` | 30%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `40ord_alow_amt` | 40%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `50ord_alow_amt` | 50%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `60ord_alow_amt` | 60%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `100ord_alow_amt` | 100%주문가능금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `crd_loan_tot` | 신용융자합계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `crd_loan_ls_tot` | 신용융자대주합계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `crd_grnt_rt` | 신용담보비율 |  | N | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `dpst_grnt_use_amt_amt` | 예탁담보대출금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `grnt_loan_amt` | 매도담보대출금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `stk_cntr_remn` | 종목별체결잔고 |  | N |  |  |
| Body | `- crd_tp` | 신용구분 |  | N | 2 |  |
| Body | `- loan_dt` | 대출일 |  | N | 8 | YYYMMDD |
| Body | `- expr_dt` | 만기일 |  | N | 8 | YYYMMDD |
| Body | `- stk_cd` | 종목번호 |  | N | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| Body | `- stk_nm` | 종목명 |  | N | 30 |  |
| Body | `- setl_remn` | 결제잔고 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- cur_qty` | 현재잔고 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- cur_prc` | 현재가 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- buy_uv` | 매입단가 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pur_amt` | 매입금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- evlt_amt` | 평가금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- evltv_prft` | 평가손익 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `- pl_rt` | 손익률 |  | N | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |

### Request Example
```json
{
    "dmst_stex_tp": "KRX"
}
```

### Response Example
```json
{
    "entr": "000000017534",
    "entr_d1": "000000017450",
    "entr_d2": "000000012550",
    "pymn_alow_amt": "000000085341",
    "uncl_stk_amt": "000000000000",
    "repl_amt": "000003915500",
    "rght_repl_amt": "000000000000",
    "ord_alowa": "000000085341",
    "ch_uncla": "000000000000",
    "crd_int_npay_gold": "000000000000",
    "etc_loana": "000000000000",
    "nrpy_loan": "000000000000",
    "profa_ch": "000000032193",
    "repl_profa": "000000000000",
    "stk_buy_tot_amt": "000006122786",
    "evlt_amt_tot": "000006236342",
    "tot_pl_tot": "000000113556",
    "tot_pl_rt": "1.8546",
    "tot_re_buy_alowa": "000000135970",
    "20ord_alow_amt": "000000012550",
    "30ord_alow_amt": "000000012550",
    "40ord_alow_amt": "000000012550",
    "50ord_alow_amt": "000000012550",
    "60ord_alow_amt": "000000012550",
    "100ord_alow_amt": "000000012550",
    "crd_loan_tot": "000000000000",
    "crd_loan_ls_tot": "000000000000",
    "crd_grnt_rt": "0.00",
    "dpst_grnt_use_amt_amt": "000000000000",
    "grnt_loan_amt": "000000000000",
    "stk_cntr_remn": [
        {
            "crd_tp": "00",
            "loan_dt": "",
            "expr_dt": "",
            "stk_cd": "A005930",
            "stk_nm": "삼성전자",
            "setl_remn": "000000000003",
            "cur_qty": "000000000003",
            "cur_prc": "000000070000",
            "buy_uv": "000000124500",
            "pur_amt": "000000373500",
            "evlt_amt": "000000209542",
            "evltv_prft": "-00000163958",
            "pl_rt": "-43.8977"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---

## [kt00007] 계좌별주문체결내역상세요청
- **메뉴 위치**: 국내주식 > 계좌 > 계좌별주문체결내역상세요청(kt00007)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 계좌별 주문 체결 내역 상세 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `ord_dt` | 주문일자 |  | N | 8 | YYYYMMDD |
| Body | `qry_tp` | 조회구분 |  | Y | 1 | 1:주문순, 2:역순, 3:미체결, 4:체결내역만 |
| Body | `stk_bond_tp` | 주식채권구분 |  | Y | 1 | 0:전체, 1:주식, 2:채권 |
| Body | `sell_tp` | 매도수구분 |  | Y | 1 | 0:전체, 1:매도, 2:매수 |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 전체 종목 조회는 빈값('')으로 설정 |
| Body | `fr_ord_no` | 시작주문번호 |  | N | 7 | 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는 빈값('')으로 설정 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `acnt_ord_cntr_prps_dtl` | 계좌별주문체결내역상세 |  | N |  |  |
| Body | `- ord_no` | 주문번호 |  | N | 7 | 고유 주문번호 7자리 |
| Body | `- stk_cd` | 종목번호 |  | N | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| Body | `- trde_tp` | 매매구분 |  | N | 20 |  |
| Body | `- crd_tp` | 신용구분 |  | N | 20 |  |
| Body | `- ord_qty` | 주문수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- ord_uv` | 주문단가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- cnfm_qty` | 확인수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- acpt_tp` | 접수구분 |  | N | 20 |  |
| Body | `- rsrv_tp` | 반대여부 |  | N | 20 |  |
| Body | `- ord_tm` | 주문시간 |  | N | 8 | HH:mm:ss |
| Body | `- ori_ord` | 원주문 |  | N | 7 |  |
| Body | `- stk_nm` | 종목명 |  | N | 40 |  |
| Body | `- io_tp_nm` | 주문구분 |  | N | 20 |  |
| Body | `- loan_dt` | 대출일 |  | N | 8 | YYYYMMDD |
| Body | `- cntr_qty` | 체결수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- cntr_uv` | 체결단가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- ord_remnq` | 주문잔량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- comm_ord_tp` | 통신구분 |  | N | 20 |  |
| Body | `- mdfy_cncl` | 정정취소 |  | N | 20 |  |
| Body | `- cnfm_tm` | 확인시간 |  | N | 8 | HH:mm:ss |
| Body | `- dmst_stex_tp` | 국내거래소구분 |  | N | 8 |  |
| Body | `- cond_uv` | 스톱가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

### Request Example
```json
{
    "ord_dt": "",
    "qry_tp": "1",
    "stk_bond_tp": "0",
    "sell_tp": "0",
    "stk_cd": "005930",
    "fr_ord_no": "",
    "dmst_stex_tp": "%"
}
```

### Response Example
```json
{
    "acnt_ord_cntr_prps_dtl": [
        {
            "ord_no": "0000050",
            "stk_cd": "A069500",
            "trde_tp": "시장가",
            "crd_tp": "보통매매",
            "ord_qty": "0000000001",
            "ord_uv": "0000000000",
            "cnfm_qty": "0000000000",
            "acpt_tp": "접수",
            "rsrv_tp": "",
            "ord_tm": "13:05:43",
            "ori_ord": "0000000",
            "stk_nm": "KODEX 200",
            "io_tp_nm": "현금매수",
            "loan_dt": "",
            "cntr_qty": "0000000001",
            "cntr_uv": "0000004900",
            "ord_remnq": "0000000000",
            "comm_ord_tp": "영웅문4",
            "mdfy_cncl": "",
            "cnfm_tm": "",
            "dmst_stex_tp": "KRX",
            "cond_uv": "0000000000"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다"
}
```

---

## [kt00009] 계좌별주문체결현황요청
- **메뉴 위치**: 국내주식 > 계좌 > 계좌별주문체결현황요청(kt00009)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 계좌별 주문 체결 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `ord_dt` | 주문일자 |  | N | 8 | YYYYMMDD |
| Body | `stk_bond_tp` | 주식채권구분 |  | Y | 1 | 0:전체, 1:주식, 2:채권 |
| Body | `mrkt_tp` | 시장구분 |  | Y | 1 | 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN |
| Body | `sell_tp` | 매도수구분 |  | Y | 1 | 0:전체, 1:매도, 2:매수 |
| Body | `qry_tp` | 조회구분 |  | Y | 1 | 0:전체, 1:체결 |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 전문 조회할 종목코드 |
| Body | `fr_ord_no` | 시작주문번호 |  | N | 7 | 시작주문번호의 이전 주문은 조회 되지 않으며 약정금액에도 포함 되지 않음 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `sell_grntl_engg_amt` | 매도약정금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `buy_engg_amt` | 매수약정금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `engg_amt` | 약정금액 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `acnt_ord_cntr_prst_array` | 계좌별주문체결현황배열 |  | N |  |  |
| Body | `- stk_bond_tp` | 주식채권구분 |  | N | 1 |  |
| Body | `- ord_no` | 주문번호 |  | N | 7 | 고유 주문번호 7자리 |
| Body | `- stk_cd` | 종목번호 |  | N | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| Body | `- trde_tp` | 매매구분 |  | N | 15 |  |
| Body | `- io_tp_nm` | 주문유형구분 |  | N | 20 |  |
| Body | `- ord_qty` | 주문수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- ord_uv` | 주문단가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- cnfm_qty` | 확인수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- rsrv_oppo` | 예약/반대 |  | N | 4 |  |
| Body | `- cntr_no` | 체결번호 |  | N | 7 | 체결번호 7자리 |
| Body | `- acpt_tp` | 접수구분 |  | N | 8 |  |
| Body | `- orig_ord_no` | 원주문번호 |  | N | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| Body | `- stk_nm` | 종목명 |  | N | 20 |  |
| Body | `- setl_tp` | 결제구분 |  | N | 8 |  |
| Body | `- crd_deal_tp` | 신용거래구분 |  | N | 20 |  |
| Body | `- cntr_qty` | 체결수량 |  | N | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- cntr_uv` | 체결단가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| Body | `- comm_ord_tp` | 통신구분 |  | N | 8 |  |
| Body | `- mdfy_cncl_tp` | 정정/취소구분 |  | N | 12 |  |
| Body | `- cntr_tm` | 체결시간 |  | N | 8 | HH:mm:ss |
| Body | `- dmst_stex_tp` | 국내거래소구분 |  | N | 6 |  |
| Body | `- cond_uv` | 스톱가 |  | N | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

### Request Example
```json
{
    "ord_dt": "",
    "stk_bond_tp": "0",
    "mrkt_tp": "0",
    "sell_tp": "0",
    "qry_tp": "0",
    "stk_cd": "",
    "fr_ord_no": "",
    "dmst_stex_tp": "KRX"
}
```

### Response Example
```json
{
    "sell_grntl_engg_amt": "000000000000",
    "buy_engg_amt": "000000004900",
    "engg_amt": "000000004900",
    "acnt_ord_cntr_prst_array": [
        {
            "stk_bond_tp": "1",
            "ord_no": "0000050",
            "stk_cd": "A069500",
            "trde_tp": "시장가",
            "io_tp_nm": "현금매수",
            "ord_qty": "0000000001",
            "ord_uv": "0000000000",
            "cnfm_qty": "0000000000",
            "rsrv_oppo": "",
            "cntr_no": "0000001",
            "acpt_tp": "접수",
            "orig_ord_no": "0000000",
            "stk_nm": "KODEX 200",
            "setl_tp": "삼일결제",
            "crd_deal_tp": "보통매매",
            "cntr_qty": "0000000001",
            "cntr_uv": "0000004900",
            "comm_ord_tp": "영웅문4",
            "mdfy_cncl_tp": "",
            "cntr_tm": "13:07:47",
            "dmst_stex_tp": "KRX",
            "cond_uv": "0000000000"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다"
}
```

---

## [kt10000] 주식 매수주문
- **메뉴 위치**: 국내주식 > 주문 > 주식 매수주문(kt10000)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/ordr`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 주식 매수 주문을 요청합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 3 | KRX,NXT,SOR |
| Body | `stk_cd` | 종목코드 |  | Y | 12 |  |
| Body | `ord_qty` | 주문수량 |  | Y | 12 | 단위: 1주 |
| Body | `ord_uv` | 주문단가 |  | N | 12 | 단위: 원 |
| Body | `trde_tp` | 매매구분 |  | Y | 2 | 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK) |
| Body | `cond_uv` | 조건단가 |  | N | 12 | 단위: 원 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `ord_no` | 주문번호 |  | N | 7 | 7자리 주문번호 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | N | 6 | KRX, NXT, SOR |

### Request Example
```json
{
    "dmst_stex_tp": "KRX",
    "stk_cd": "005930",
    "ord_qty": "1",
    "ord_uv": "",
    "trde_tp": "3",
    "cond_uv": ""
}
```

### Response Example
```json
{
    "ord_no" : "00024"
    "return_code":0,
    "return_msg":"정상적으로 처리되었습니다"
}
```

---

## [kt10001] 주식 매도주문
- **메뉴 위치**: 국내주식 > 주문 > 주식 매도주문(kt10001)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/ordr`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 주식 매도 주문을 요청합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | Y | 3 | KRX,NXT,SOR |
| Body | `stk_cd` | 종목코드 |  | Y | 12 |  |
| Body | `ord_qty` | 주문수량 |  | Y | 12 | 단위: 1주 |
| Body | `ord_uv` | 주문단가 |  | N | 12 | 단위: 원 |
| Body | `trde_tp` | 매매구분 |  | Y | 2 | 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK) |
| Body | `cond_uv` | 조건단가 |  | N | 12 | 단위: 원 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `ord_no` | 주문번호 |  | N | 7 | 7자리 주문번호 |
| Body | `dmst_stex_tp` | 국내거래소구분 |  | N | 6 | KRX, NXT, SOR |

### Request Example
```json
{
    "dmst_stex_tp": "KRX",
    "stk_cd": "005930",
    "ord_qty": "1",
    "ord_uv": "",
    "trde_tp": "3",
    "cond_uv": ""
}
```

### Response Example
```json
{
    "ord_no": "0000138",
    "dmst_stex_tp": "KRX",
    "return_code": 0,
    "return_msg": "매도주문이 완료되었습니다."
}
```

---

## [usa06011] 미국주식 분 차트
- **메뉴 위치**: 미국주식 > 차트 > 미국주식 분 차트(usa06011)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/chart`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 분 차트 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | Y |  | NA: AMEX, ND: NASDAQ, NY: NYSE |
| Body | `stk_cd` | 종목코드 |  | N |  |  |
| Body | `strt_dt` | 시작일자 |  | N |  | YYYYMMDD |
| Body | `tic_scope` | XX분봉 |  | N |  |  |
| Body | `upd_stkpc_tp` | 수정주가구분 |  | N |  | 0:미적용, 1:적용 |
| Body | `exrt_appl_tp` | 환율적용구분 |  | N |  | 0:미적용, 1:적용 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- cur_prc` | 현재가(종가) |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- trde_qty` | 거래량 |  | N |  |  |
| Body | `- open_pric` | 시가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- high_pric` | 고가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- low_pric` | 저가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- cntr_tm` | 체결시간 |  | N |  | YYYYMMDDHHmmss |
| Body | `- bus_dt` | 영업일자 |  | N |  | YYYYMMDD |
| Body | `- upd_stkpc_tp` | 수정주가구분 |  | N |  |  |
| Body | `- upd_rt` | 수정비율 |  | N |  |  |

### Request Example
```json
{
    "stex_tp": "ND",
    "stk_cd": "NVDA",
    "strt_dt": "20260305",
    "tic_scope": "1",
    "upd_stkpc_tp": "0",
    "exrt_appl_tp": "1"
}
```

### Response Example
```json
{
    "result_list": [
        {
            "cur_prc": "201.3900",
            "trde_qty": "2",
            "open_pric": "201.3900",
            "high_pric": "201.3900",
            "low_pric": "201.3900",
            "cntr_tm": "20260624080800",
            "bus_dt": "20260624",
            "upd_stkpc_tp": "",
            "upd_rt": ""
        },
        {
            "cur_prc": "201.3700",
            "trde_qty": "1",
            "open_pric": "201.3700",
            "high_pric": "201.3700",
            "low_pric": "201.3700",
            "cntr_tm": "20260624080800",
            "bus_dt": "20260624",
            "upd_stkpc_tp": "",
            "upd_rt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [usa06012] 미국주식 일 차트
- **메뉴 위치**: 미국주식 > 차트 > 미국주식 일 차트(usa06012)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/chart`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 일 차트 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | Y |  | NA: AMEX, ND: NASDAQ, NY: NYSE |
| Body | `stk_cd` | 종목코드 |  | N |  |  |
| Body | `strt_dt` | 시작일자 |  | N |  | YYYYMMDD |
| Body | `upd_stkpc_tp` | 수정주가구분 |  | N |  | 0:미적용, 1:적용 |
| Body | `exrt_appl_tp` | 환율적용구분 |  | N |  | 0:미적용, 1:적용 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- cur_prc` | 현재가(종가) |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- pred_pre` | 전일대비 |  | N |  | 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- flu_rt` | 등락율 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- acc_trde_qty` | 누적거래량 |  | N |  |  |
| Body | `- acc_trde_prica` | 누적거래대금 |  | N |  |  |
| Body | `- open_pric` | 시가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- high_pric` | 고가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- low_pric` | 저가 |  | N |  | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- dt` | 일자 |  | N |  | YYYYMMDD |
| Body | `- upd_stkpc_tp` | 수정주가구분 |  | N |  |  |
| Body | `- upd_rt` | 수정비율 |  | N |  |  |

### Request Example
```json
{
    "stex_tp": "ND",
    "stk_cd": "NVDA",
    "strt_dt": "20260412",
    "upd_stkpc_tp": "1",
    "exrt_appl_tp": "0"
}
```

### Response Example
```json
{
    "result_list": [
        {
            "cur_prc": "201.3612",
            "pred_pre": "+1.3212",
            "flu_rt": "+0.66",
            "acc_trde_qty": "431663",
            "acc_trde_prica": "86910071",
            "open_pric": "200.0400",
            "high_pric": "200.0400",
            "low_pric": "200.0400",
            "dt": "20260624",
            "upd_stkpc_tp": "",
            "upd_rt": ""
        },
        {
            "cur_prc": "200.0400",
            "pred_pre": "-8.6100",
            "flu_rt": "-4.30",
            "acc_trde_qty": "153496196",
            "acc_trde_prica": "39496094121",
            "open_pric": "202.1700",
            "high_pric": "203.7700",
            "low_pric": "200.0000",
            "dt": "20260623",
            "upd_stkpc_tp": "",
            "upd_rt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [usa20100] 미국주식 현재가 상세(시세)
- **메뉴 위치**: 미국주식 > 시세 > 미국주식 현재가 상세(usa20100)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/mrkcond`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식의 현재가, 전일 종가 등의 종합 시세 정보를 단건 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, `usa20100` |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙여서 호출 |
| Body | `stex_tp` | 거래소구분 | String | Y | | NA: AMEX, ND: NASDAQ, NY: NYSE |
| Body | `stk_cd` | 종목코드 | String | Y | | 종목코드 (ex: NVDA, TQQQ) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, `usa20100` |
| Body | `base_close_pric` | 전일종가 | String/Float | N | | 전일종가 (단위: USD) |
| Body | `cur_prc` | 현재가 | String/Float | N | | 현재가 (단위: USD) |
| Body | `return_code` | 응답코드 | String/Int | Y | | 0: 정상 처리 |
| Body | `return_msg` | 응답메시지 | String | Y | | 오류 메시지 혹은 정상 처리 메시지 |

### Request Example
```json
{
    "stex_tp": "ND",
    "stk_cd": "NVDA"
}
```

### Response Example
```json
{
    "base_close_pric": "127.5000",
    "cur_prc": "130.2500",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [usa20280] 미국주식 조건검색 목록조회
- **메뉴 위치**: 미국주식 > 조건검색 > 미국주식 조건검색 목록조회(usa20280)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 조건검색은 영웅문Global에서 만드실 수 있습니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | TR명 |  | Y | 8 | GCNSRLST고정값 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 정상 : 0 |
| Body | `return_msg` | 결과메시지 |  | N |  | 정상인 경우는 메시지 없음 |
| Body | `trnm` | 서비스명 |  | N |  | GCNSRLT고정값 |
| Body | `data` | 조건검색식 목록 |  | N |  |  |
| Body | `- seq` | 조건검색식 일련번호 |  | N |  |  |
| Body | `- name` | 조건검색식 명 |  | N |  |  |

### Request Example
```json
{
    "trnm": "GCNSRLST"
}
```

### Response Example
```json
{
    "trnm": "GCNSRLST",
    "return_code": 0,
    "return_msg": "",
    "data": [
        ["0","조건1"],
        ["1","조건2"],
        ["2","조건3"],
        ["3","조건4"],
        ["4","조건5"],
    ]
}
```

---

## [usa21670] 미국주식 일별계좌수익률현황
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 일별계좌수익률현황(usa21670)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 일별 계좌 수익률 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `from` | from 일자 |  | Y |  | YYYYMMDD |
| Body | `to` | to 일자 |  | Y |  | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- base_dt` | 기준일 |  | N |  |  |
| Body | `- stk_evlta` | 주식평가금 |  | N |  |  |
| Body | `- pl_amt` | 손익금액 |  | N |  |  |
| Body | `- dvid_amt` | 배당금액 |  | N |  |  |
| Body | `- cmsn_tax` | 수수료+세금 |  | N |  |  |
| Body | `- acum_pl_amt` | 누적손익 |  | N |  |  |
| Body | `- pymn_amt` | 출금금액 |  | N |  |  |
| Body | `- dast` | 예탁자산 |  | N |  |  |
| Body | `- dly_amt` | 연체금액 |  | N |  |  |
| Body | `- sell_amt` | 매도금액 |  | N |  |  |
| Body | `- buy_amt` | 매수금액 |  | N |  |  |
| Body | `- prft_rt` | 수익률 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- frgn_stk_outq_amt` | 출고금액 |  | N |  |  |
| Body | `- frgn_stk_inq_amt` | 입고금액 |  | N |  |  |
| Body | `- ina_amt` | 입금금액 |  | N |  |  |
| Body | `- exrt` | 환율 |  | N |  |  |

### Request Example
```json
{
    "from": "20260501",
    "to": "20260511"
}
```

### Response Example
```json
{
    "result_list": [
        {
            "base_dt": "20260503",
            "stk_evlta": "165918511",
            "pl_amt": "165918511",
            "dvid_amt": "0",
            "cmsn_tax": "0",
            "acum_pl_amt": "165918511",
            "pymn_amt": "0",
            "dast": "23911983597",
            "dly_amt": "0",
            "sell_amt": "0",
            "buy_amt": "0",
            "prft_rt": "0.70",
            "frgn_stk_outq_amt": "0",
            "frgn_stk_inq_amt": "0",
            "ina_amt": "0",
            "exrt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [usa21680] 미국주식 월별계좌수익률현황
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 월별계좌수익률현황(usa21680)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 월별 계좌 수익률 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `from` | from 년월 |  | Y |  | YYYYMM |
| Body | `to` | to 년월 |  | Y |  | YYYYMM |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- base_dt` | 기준일 |  | N |  |  |
| Body | `- stk_evlta` | 주식평가금 |  | N |  |  |
| Body | `- pl_amt` | 손익금액 |  | N |  |  |
| Body | `- dvid_amt` | 배당금액 |  | N |  |  |
| Body | `- cmsn_tax` | 수수료+세금 |  | N |  |  |
| Body | `- acum_pl_amt` | 누적손익 |  | N |  |  |
| Body | `- pymn_amt` | 출금금액 |  | N |  |  |
| Body | `- dast` | 예탁자산 |  | N |  |  |
| Body | `- dly_amt` | 연체금액 |  | N |  |  |
| Body | `- sell_amt` | 매도금액 |  | N |  |  |
| Body | `- buy_amt` | 매수금액 |  | N |  |  |
| Body | `- prft_rt` | 수익률 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- frgn_stk_outq_amt` | 출고금액 |  | N |  |  |
| Body | `- frgn_stk_inq_amt` | 입고금액 |  | N |  |  |
| Body | `- ina_amt` | 입금금액 |  | N |  |  |
| Body | `- exrt` | 환율 |  | N |  |  |

### Request Example
```json
{
    "from": "202605",
    "to": "202605"
}
```

### Response Example
```json
{
    "result_list": [
        {
            "base_dt": "202605",
            "stk_evlta": "224548209",
            "pl_amt": "4141959526",
            "dvid_amt": "0",
            "cmsn_tax": "112762",
            "acum_pl_amt": "4141959526",
            "pymn_amt": "0",
            "dast": "27431091788",
            "dly_amt": "0",
            "sell_amt": "2926000000",
            "buy_amt": "27256614",
            "prft_rt": "17.36",
            "frgn_stk_outq_amt": "0",
            "frgn_stk_inq_amt": "0",
            "ina_amt": "0",
            "exrt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [usa21690] 미국주식 연도별계좌수익률현황
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 연도별계좌수익률현황(usa21690)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 연도별 계좌 수익률 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `from` | from 년도 |  | Y |  | YYYY |
| Body | `to` | to 년도 |  | Y |  | YYYY |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- base_dt` | 기준일 |  | N |  |  |
| Body | `- stk_evlta` | 주식평가금 |  | N |  |  |
| Body | `- pl_amt` | 손익금액 |  | N |  |  |
| Body | `- dvid_amt` | 배당금액 |  | N |  |  |
| Body | `- cmsn_tax` | 수수료+세금 |  | N |  |  |
| Body | `- acum_pl_amt` | 누적손익 |  | N |  |  |
| Body | `- pymn_amt` | 출금금액 |  | N |  |  |
| Body | `- dast` | 예탁자산 |  | N |  |  |
| Body | `- dly_amt` | 연체금액 |  | N |  |  |
| Body | `- sell_amt` | 매도금액 |  | N |  |  |
| Body | `- buy_amt` | 매수금액 |  | N |  |  |
| Body | `- prft_rt` | 수익률 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- frgn_stk_outq_amt` | 출고금액 |  | N |  |  |
| Body | `- frgn_stk_inq_amt` | 입고금액 |  | N |  |  |
| Body | `- ina_amt` | 입금금액 |  | N |  |  |
| Body | `- exrt` | 환율 |  | N |  |  |

### Request Example
```json
{
    "from": "2026",
    "to": "2026"
}
```

### Response Example
```json
{
    "result_list": [
        {
            "base_dt": "2026",
            "stk_evlta": "250117674",
            "pl_amt": "30391098826",
            "dvid_amt": "0",
            "cmsn_tax": "719910",
            "acum_pl_amt": "30391098826",
            "pymn_amt": "7617000",
            "dast": "27957204238",
            "dly_amt": "0",
            "sell_amt": "27347262123",
            "buy_amt": "234023274",
            "prft_rt": "0.00",
            "frgn_stk_outq_amt": "0",
            "frgn_stk_inq_amt": "0",
            "ina_amt": "0",
            "exrt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

---

## [ust20000] 미국주식 매수 주문
- **메뉴 위치**: 미국주식 > 주문 > 미국주식 매수 주문(ust20000)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/ordr`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 매수 주문을 요청합니다.
주문 TR의 경우 영웅문 Global [2000] 해외주식 주문 종합 화면에서 미국 주식 주문 유형별 유의사항을 확인 후 주문해주시기 바랍니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | Y |  | NA: AMEX, ND: NASDAQ, NY: NYSE |
| Body | `stk_cd` | 종목코드 |  | Y | 12 |  |
| Body | `ord_qty` | 주문수량 |  | Y | 12 |  |
| Body | `ord_uv` | 주문단가 |  | N | 12 | trde_tp가 00(지정가),30(LOC)...인 경우 필수 입력, 그 외 시장가 거래유형 설정 시 입력 값은 빈 값 처리 |
| Body | `trde_tp` | 해외매매구분 |  | Y | 2 | 00:지정가 03시장가 26:VWAP지정가 27:TWAP지정가 30:LOC 36:VWAP시장가 37:TWAP시장가 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `stk_nm` | 종목명 |  | N | 50 |  |
| Body | `ord_no` | 주문번호 |  | N | 9 | 취소 혹은 정정 주문 시 사용 |
| Body | `fc_entra` | 외화예수금 |  | N | 12 |  |
| Body | `tdy_rebuy_useda` | 금일재매수사용금액 |  | N | 12 |  |
| Body | `pred_rebuy_useda` | 전일재매수사용금액 |  | N | 12 |  |
| Body | `trst_prof_ch` | 사용증거금 |  | N | 12 |  |

### Request Example
```json
{
    "stex_tp": "ND",
    "stk_cd": "NVDA",
    "ord_qty": "10",
    "ord_uv": "213.04",
    "trde_tp": "00"
}
```

### Response Example
```json
{
    "acnt_nm": "000",
    "stk_nm": "엔비디아",
    "ord_no": "000000282",
    "fc_entra": "18042538.7700",
    "tdy_rebuy_useda": "195.7772",
    "pred_rebuy_useda": "365.0867",
    "trst_prof_ch": "444.1361",
    "return_code": 0,
    "return_msg": "미국 매수주문입력 완료되었습니다"
}
```

---

## [ust20001] 미국주식 매도 주문
- **메뉴 위치**: 미국주식 > 주문 > 미국주식 매도 주문(ust20001)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/ordr`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 매도 주문을 요청합니다.
주문 TR의 경우 영웅문 Global [2000] 해외주식 주문 종합 화면에서 미국 주식 주문 유형별 유의사항을 확인 후 주문해주시기 바랍니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stk_cd` | 종목코드 |  | Y | 12 |  |
| Body | `stex_tp` | 거래소구분 |  | Y |  | NA: AMEX, ND: NASDAQ, NY: NYSE |
| Body | `ord_qty` | 주문수량 |  | Y | 12 |  |
| Body | `ord_uv` | 주문단가 |  | N | 12 | trde_tp가 00(지정가),30(LOC)...인 경우 필수 입력, 그 외 시장가 거래유형 설정 시 입력 값은 빈 값 처리 |
| Body | `stop_pric` | STOP가격 |  | N | 12 | trde_tp가 34(STOP LIMIT) 또는 35(STOP)인 경우 필수 입력, 그 외 거래유형(지정가,시장가 등) 설정 시 입력 값은 무시되거나 빈 값처리. |
| Body | `trde_tp` | 매매구분 |  | Y | 2 | 00:지정가 03시장가 26:VWAP지정가 27:TWAP지정가 30:LOC 33:MOC 36:VWAP시장가 37:TWAP시장가 35:STOP 34:STOP LIMIT |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `stk_nm` | 종목명 |  | N | 50 |  |
| Body | `ord_no` | 주문번호 |  | N | 9 | 취소 혹은 정정 주문 시 사용 |
| Body | `poss_qty` | 보유수량 |  | N | 12 |  |
| Body | `tdy_resel_usedq` | 금일재매도사용수량 |  | N | 12 |  |
| Body | `pred_resel_usedq` | 전일재매도사용수량 |  | N | 12 |  |

### Request Example
```json
{
    "stk_cd": "NVDA",
    "stex_tp": "ND",
    "ord_qty": "10",
    "ord_uv": "210.05",
    "stop_pric": "",
    "trde_tp": "00"
}
```

### Response Example
```json
{
    "acnt_nm": "000",
    "stk_nm": "엔비디아",
    "ord_no": "000000283",
    "poss_qty": "000000000028",
    "tdy_resel_usedq": "000000000000",
    "pred_resel_usedq": "000000000000",
    "return_code": 0,
    "return_msg": "미국 매도주문 입력이 완료되었습니다."
}
```

---

## [ust21100] 미국주식 거래내역
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 거래내역(ust21100)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 거래내역 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `strt_dt` | 시작일자 |  | N | 8 | YYYYMMDD |
| Body | `end_dt` | 종료일자 |  | N | 8 | YYYYMMDD |
| Body | `tp` | 구분 |  | N | 1 | 0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,F:환전, M:입출금+환전(매체전용), G:환전매수, H:환전매도, I:환전정산입금, J:환전정산출금, 6:입금, 7:출금 8:배당금입금 K:환전+환전정산입출금 |
| Body | `stex_tp` | 거래소구분 |  | N | 2 | ND:NASDAQ,NY:NYSE,NA:AMEX |
| Body | `stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `krw_repl_skip_yn` | 원화대용입출금제외여부 |  | N | 1 | Y:제외,N:비제외 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `acnt_print` | 계좌번호 |  | N | 62 | 계좌번호 출력용 |
| Body | `sell_sum` | 매도합계 |  | N | 15 |  |
| Body | `buy_sum` | 매수합계 |  | N | 15 |  |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- deal_dt` | 거래일자 |  | N | 8 |  |
| Body | `- deal_kind_nm` | 거래종류명 |  | N | 20 |  |
| Body | `- rmrk_nm` | 적요명 |  | N | 60 |  |
| Body | `- deal_amt` | 거래금액 |  | N | 15 |  |
| Body | `- tax_tot_amt` | 소득/주민세 |  | N | 15 | 기존:세금합 |
| Body | `- exct_amt` | 정산금액 |  | N | 15 |  |
| Body | `- uncl_ocr` | 미수(원/주) |  | N | 30 |  |
| Body | `- fc_uncl_ocr` | 미수(외) |  | N | 15 |  |
| Body | `- entra_remn` | 예수금잔고 |  | N | 15 |  |
| Body | `- deal_no` | 거래번호 |  | N | 9 |  |
| Body | `- stk_nm` | 종목명 |  | N | 40 |  |
| Body | `- deal_qty` | 거래수량 |  | N | 30 |  |
| Body | `- fc_deal_tax` | 거래세(외) |  | N | 15 |  |
| Body | `- frgn_pay_txam` | 외국납부세액(외) |  | N | 15 |  |
| Body | `- rpym_sum` | 변제합 |  | N | 15 |  |
| Body | `- fc_rpym_sum` | 변제합(외) |  | N | 30 |  |
| Body | `- fc_entra` | 외화예수금잔고 |  | N | 15 |  |
| Body | `- mdia_nm` | 메체구분명 |  | N | 20 |  |
| Body | `- orig_deal_no` | 원거래번호 |  | N | 9 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- uv_exrt` | 거래단가/환율 |  | N | 20 |  |
| Body | `- fc_cmsn` | 수수료(외) |  | N | 15 |  |
| Body | `- fc_exct_amt` | 정산금액(외) |  | N | 15 |  |
| Body | `- dly_sum` | 연체합 |  | N | 15 |  |
| Body | `- fc_dly_sum` | 연체합(외) |  | N | 15 |  |
| Body | `- vlbl_nowrm` | 유가금잔 |  | N | 30 |  |
| Body | `- stex_nm` | 거래소구분명 |  | N | 20 |  |
| Body | `- fc_deal_amt` | 거래금액(외) |  | N | 15 |  |
| Body | `- proc_time` | 처리시간 |  | N | 111 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |

### Request Example
```json
{
    "strt_dt": "20260601",
    "end_dt": "20260613",
    "tp": "",
    "stex_tp": "",
    "stk_cd": "",
    "krw_repl_skip_yn": ""
}
```

### Response Example
```json
{
    "acnt_print": "0000-0000-10 [***]",
    "sell_sum": "2000000.00",
    "buy_sum": "19118.36",
    "result_list": [
        {
            "deal_dt": "20260511",
            "deal_kind_nm": "매매",
            "rmrk_nm": "매수",
            "deal_amt": "000000000000000",
            "tax_tot_amt": "000000000000000",
            "exct_amt": "000000000000000",
            "uncl_ocr": "0",
            "fc_uncl_ocr": "0.00",
            "entra_remn": "000000000000000",
            "deal_no": "000000001",
            "stk_nm": "뱅크오브아메리카",
            "deal_qty": "20",
            "fc_deal_tax": "0.00",
            "frgn_pay_txam": "0.00",
            "rpym_sum": "000000000000000",
            "fc_rpym_sum": "0.00",
            "fc_entra": "16085944.77",
            "mdia_nm": "영웅문Global",
            "orig_deal_no": "000000000",
            "stk_cd": "BAC",
            "uv_exrt": "54.1300",
            "fc_cmsn": "2.70",
            "fc_exct_amt": "1085.30",
            "dly_sum": "000000000000000",
            "fc_dly_sum": "0.00",
            "vlbl_nowrm": "20",
            "isin_code": "US0605051046",
            "stex_nm": "미국",
            "fc_deal_amt": "1082.60",
            "wrkr_id": "SY",
            "proc_brch": "영업부",
            "proc_time": "08:25:42",
            "crnc_code": "USD"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다"
}
```

---

## [ust21150] 미국주식 일별 주문체결내역
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 일별 주문체결내역(ust21150)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 일별 주문체결내역 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `ord_dt` | 주문일자 |  | N | 8 | 미입력시 오늘 날짜로 조회 |
| Body | `query_tp` | 조회구분 |  | Y | 1 | 1:주문순,2:주문역순,3:미체결주문순,4:미체결역순,5:체결주문순,6:체결역순 |
| Body | `slby_tp` | 매도수구분 |  | Y | 1 | 0:전체,1:매도,2:매수 |
| Body | `stex_tp` | 거래소구분 |  | N | 2 | ND:NASDAQ,NY:NYSE,NA:AMEX |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 미입력시 전체 |
| Body | `oppo_trde_tp` | 반대매매구분 |  | N | 1 | %:전체,0:일반,1:반대매매 |
| Body | `fr_ord_no` | 시작주문번호 |  | N | 9 |  |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- ord_no` | 주문번호 |  | N | 9 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- isin_code` | 국제표준코드 |  | N | 12 |  |
| Body | `- frgn_trde_tp` | 매매구분 |  | N | 40 |  |
| Body | `- ord_qty` | 주문수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- cntr_qty` | 체결수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- mdfy_qty` | 정정수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- cncl_qty` | 취소수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- frgn_msg_code` | 해외메세지코드 |  | N | 8 |  |
| Body | `- rsrv_tp` | 예약구분 |  | N | 12 |  |
| Body | `- oppo_trde_tp_nm` | 반대매매구분명 |  | N | 20 |  |
| Body | `- comm_ord_tp_nm` | 통신주문구분명 |  | N | 20 |  |
| Body | `- ord_time` | 주문시간 |  | N | 8 | HH:mm:ss |
| Body | `- crnc_nm` | 통화코드명 |  | N | 20 |  |
| Body | `- stex_nm` | 거래소코드명 |  | N | 20 |  |
| Body | `- frgn_stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- slby_tp_nm` | 매도매수구분명 |  | N | 4 |  |
| Body | `- ord_uv` | 주문단가 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- stop_pric` | STOP가격 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- cntr_uv` | 체결단가 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- mdfy_uv` | 정정단가 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- ord_remnq` | 주문잔량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- ord_stat_nm` | 주문상태명 |  | N | 25 |  |
| Body | `- text1` | 거부사유 |  | N | 80 |  |
| Body | `- inpt_chnl_tp` | 입력매체구분명 |  | N | 20 |  |
| Body | `- ord_resp_time` | 주문응답수신시간 |  | N | 8 | HH:mm:ss |
| Body | `- cntr_time` | 체결시간 |  | N | 8 |  |

### Request Example
```json
{
    "ord_dt": "",
    "query_tp": "1",
    "slby_tp": "0",
    "stex_tp": "",
    "stk_cd": "",
    "oppo_trde_tp": "",
    "fr_ord_no": ""
}
```

### Response Example
```json
{
    "result_lsit": [
        {
            "ord_no": "000000252",
            "crnc_code": "USD",
            "stk_cd": "NVDA",
            "isin_code": "US67066G1040",
            "frgn_trde_tp": "지정가",
            "ord_qty": "000000000001",
            "cntr_qty": "000000000001",
            "mdfy_qty": "000000000000",
            "cncl_qty": "000000000000",
            "frgn_msg_code": "",
            "rsrv_tp": "일반",
            "oppo_trde_tp_nm": "일반",
            "comm_ord_tp_nm": "영웅문Global",
            "ord_time": "21:04:41",
            "crnc_nm": "미국달러",
            "stex_nm": "미국",
            "frgn_stk_nm": "엔비디아",
            "slby_tp_nm": "매도",
            "ord_uv": "201.0200",
            "stop_pric": "0.0000",
            "cntr_uv": "201.3147",
            "mdfy_uv": "0.0000",
            "ord_remnq": "000000000000",
            "ord_stat_nm": "체결완료",
            "text1": "",
            "inpt_chnl_tp": "영웅문Global",
            "ord_resp_time": "21:04:41",
            "cntr_time": "21:04:41"
        },
    ],
    "return_code": 0,
    "return_msg": "계좌별 체결내역이 조회되었습니다."
}
```

---

## [ust21160] 미국주식 예수금 상세
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 예수금 상세(ust21160)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 예수금 상세 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `won_entr` | 원화 예수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `won_dfr_amt` | 미수금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `won_etc_loana` | 기타 대여금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `krw_ord_set_amt` | 해외원화주문설정금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `usd_exch_rate` | 매도환율(USD) |  | N | 12 | 세자릿수 콤마, 소수점 둘째 자리까지 포맷된 숫자 |
| Body | `d0_setl_dt` | D0 국내결제일자 |  | N | 8 | YYYYMMDD |
| Body | `d0_won_conv_alow_ch` | D0 원화환산추정인출가능금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d0_usd_fx_entr` | D0 외화예수금(USD) |  | N | 15 |  |
| Body | `d1_setl_dt` | D1 국내결제일자 |  | N | 8 |  |
| Body | `d1_won_conv_alow_ch` | D1 원화환산추정인출가능금 |  | N | 15 |  |
| Body | `d1_usd_fx_entr` | D1 외화예수금(USD) |  | N | 15 |  |
| Body | `d1_usd_exct_amt` | D1 해외정산금(USD) |  | N | 15 |  |
| Body | `d1_usd_buy_excta` | D1 해외매수정산금(USD) |  | N | 15 |  |
| Body | `d1_usd_sell_excta` | D1 해외매도정산금(USD) |  | N | 15 |  |
| Body | `d2_setl_dt` | D2 국내결제일자 |  | N | 8 | YYYYMMDD |
| Body | `d2_won_conv_alow_ch` | D2 원화환산추정인출가능금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d2_usd_fx_entr` | D2 외화예수금(USD) |  | N | 15 |  |
| Body | `d2_usd_exct_amt` | D2 해외정산금(USD) |  | N | 15 |  |
| Body | `d2_usd_buy_excta` | D2 해외매수정산금(USD) |  | N | 15 |  |
| Body | `d2_usd_sell_excta` | D2 해외매도정산금(USD) |  | N | 15 |  |
| Body | `d3_setl_dt` | D3 국내결제일자 |  | N | 8 | YYYYMMDD |
| Body | `d3_won_conv_alow_ch` | D3 원화환산추정인출가능금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d3_usd_fx_entr` | D3 외화예수금(USD) |  | N | 15 |  |
| Body | `d3_usd_exct_amt` | D3 해외정산금(USD) |  | N | 15 |  |
| Body | `d3_usd_buy_excta` | D3 해외매수정산금(USD) |  | N | 15 |  |
| Body | `d3_usd_sell_excta` | D3 해외매도정산금(USD) |  | N | 15 |  |
| Body | `d4_setl_dt` | D4 국내결제일자 |  | N | 8 | YYYYMMDD |
| Body | `d4_won_conv_alow_ch` | D4 원화환산추정인출가능금 |  | N | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| Body | `d4_usd_fx_entr` | D4 외화예수금(USD) |  | N | 15 |  |
| Body | `d4_usd_exct_amt` | D4 해외정산금(USD) |  | N | 15 |  |
| Body | `d4_usd_buy_excta` | D4 해외매수정산금(USD) |  | N | 15 |  |
| Body | `d4_usd_sell_excta` | D4 해외매도정산금(USD) |  | N | 15 |  |

### Request Example
```json
{}
```

### Response Example
```json
{
    "won_entr": "000000930965946",
    "won_dfr_amt": "000000000000000",
    "won_etc_loana": "000000000000000",
    "krw_ord_set_amt": "000000000000",
    "usd_exch_rate": "1,507.70",
    "d0_setl_dt": "20260626",
    "d0_won_conv_alow_ch": "000028131991593",
    "d0_usd_fx_entr": "18041599.000",
    "d1_setl_dt": "20260629",
    "d1_won_conv_alow_ch": "000028131991601",
    "d1_usd_fx_entr": "18041404.560",
    "d1_usd_exct_amt": "-194.440",
    "d1_usd_buy_excta": "194.440",
    "d1_usd_sell_excta": "0.000",
    "d2_setl_dt": "20260630",
    "d2_won_conv_alow_ch": "000028131991601",
    "d2_usd_fx_entr": "18041404.560",
    "d2_usd_exct_amt": "0.000",
    "d2_usd_buy_excta": "0.000",
    "d2_usd_sell_excta": "0.000",
    "d3_setl_dt": "20260701",
    "d3_won_conv_alow_ch": "000028131991601",
    "d3_usd_fx_entr": "18041404.560",
    "d3_usd_exct_amt": "0.000",
    "d3_usd_buy_excta": "0.000",
    "d3_usd_sell_excta": "0.000",
    "d4_setl_dt": "20260702",
    "d4_won_conv_alow_ch": "000028131991601",
    "d4_usd_fx_entr": "18041404.560",
    "d4_usd_exct_amt": "0.000",
    "d4_usd_buy_excta": "0.000",
    "d4_usd_sell_excta": "0.000",
    "return_code": 0,
    "return_msg": "해외증권 예수금 상세현황이 조회 되었습니다."
}
```

---

## [ust21510] 미국주식 당일 주문체결 확인
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 당일 주문체결 확인(ust21510)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 당일 주문체결 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `slby_tp` | 매도매수구분 |  | N | 1 | 0:전체,1:매도,2:매수 |
| Body | `stex_tp` | 거래소구분 |  | N | 2 | 종목코드 입력시 |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 미입력시 전체 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 조회결과리스트 |  | N |  |  |
| Body | `- ord_no` | 주문번호 |  | N | 9 |  |
| Body | `- orig_ord_no` | 원주문번호 |  | N | 9 |  |
| Body | `- stex_nm` | 거래소명 |  | N | 30 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- frgn_stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- frgn_trde_tp` | 매매구분 |  | N | 2 | 00:지정가,03:시장가,11:Enhanced Limit Order,12:Special Limit Order,30:Limit On Close,33:Market On Close,34:Stop Limit,35:Stop Market,36:VWAP,37:TWAP |
| Body | `- frgn_trde_nm` | 매매구분명 |  | N | 30 |  |
| Body | `- slby_tp` | 매도매수구분 |  | N | 1 | 1:매도,2:매수 |
| Body | `- slby_tp_nm` | 매도매수구분명 |  | N | 4 |  |
| Body | `- ord_qty` | 주문수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- ord_uv` | 주문단가 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- stop_pric` | STOP가격 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- cntr_qty` | 체결수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- cntr_uv` | 체결단가 |  | N | 12 | 단위: USD, 소수점 넷째 자리까지 포맷된 숫자 |
| Body | `- cnfm_qty` | 확인수량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- ord_remnq` | 주문잔량 |  | N | 12 | 단위: 1주, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `- ord_time` | 주문시간 |  | N | 8 | HH:mm:ss |
| Body | `- ord_resp_time` | 주문응답시간 |  | N | 8 | HH:mm:ss |
| Body | `- ord_stat` | 주문상태명 |  | N | 25 |  |
| Body | `- rsrv_tp` | 예약주문구분 |  | N | 12 | 0:일반, 1:예약 |
| Body | `- natn_nm` | 국가명 |  | N | 40 |  |
| Body | `- cntr_time` | 체결시간 |  | N | 8 |  |

### Request Example
```json
{
    "slby_tp": "0",
    "stex_tp": "",
    "stk_cd": ""
}
```

### Response Example
```json
{
    "result_lsit": [
        {
            "ord_no": "000000281",
            "orig_ord_no": "000000000",
            "stex_nm": "미국",
            "crnc_code": "USD",
            "stk_cd": "NVDA",
            "frgn_stk_nm": "엔비디아",
            "frgn_trde_tp": "00",
            "frgn_trde_nm": "지정가",
            "slby_tp": "2",
            "slby_tp_nm": "매수",
            "ord_qty": "000000000005",
            "ord_uv": "1.0000",
            "stop_pric": "0.0000",
            "cntr_qty": "000000000000",
            "cntr_uv": "0.0000",
            "cnfm_qty": "000000000000",
            "ord_remnq": "000000000005",
            "ord_time": "21:45:58",
            "ord_resp_time": "21:45:58",
            "ord_stat": "접수",
            "rsrv_tp": "일반",
            "natn_nm": "미국",
            "cntr_time": ""
        },
    ],
    "return_code": 0,
    "return_msg": "계좌별 체결내역이 조회되었습니다."
}
```

---

## [ust21620] 미국주식 당일매매정리
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 당일매매정리(ust21620)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 당일 매매 정리 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | N | 2 | NA :AMEX, ND :NASDAQ, NY:NYSE |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 기본값 전체 |
| Body | `fc_krw_tp` | 외화원화구분 |  | Y | 1 | 0:외화,1:원화 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- stex_nm` | 거래소코드명 |  | N | 20 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- slby_tp_nm` | 매도수구분명 |  | N | 40 | 매수인경우'+',매도인경우'-' |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- cntr_uv` | 체결단가 |  | N | 12 |  |
| Body | `- cntr_qty` | 체결수량 |  | N | 12 |  |
| Body | `- engg_amt` | 약정금액 |  | N | 15 |  |
| Body | `- cmsn` | 수수료 |  | N | 15 |  |
| Body | `- altx` | 제세금 |  | N | 15 |  |
| Body | `- exct_amt` | 정산금액 |  | N | 15 |  |
| Body | `- exch_rate` | 환율 |  | N | 12 |  |
| Body | `- natn_nm` | 국가명 |  | N | 40 |  |

### Request Example
```json
{
    "stex_tp": "",
    "stk_cd": "",
    "fc_krw_tp": "0"
}
```

### Response Example
```json
{
    "result_lsit": [
        {
            "stex_nm": "미국",
            "stk_cd": "NVDA",
            "stk_nm": "엔비디아",
            "slby_tp_nm": "-매도",
            "crnc_code": "USD",
            "cntr_uv": "201.3147",
            "cntr_qty": "000000000001",
            "engg_amt": "201.3147",
            "cmsn": "0.5033",
            "altx": "0.0042",
            "exct_amt": "200.8072",
            "exch_rate": "1520.80",
            "natn_nm": "미국"
        }
    ],
    "return_code": 0,
    "return_msg": "해외주식 당일 매매 정리 자료가 조회 되었습니다."
}
```

---

## [ust21630] 미국주식 당일 실현손익
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 당일 실현손익(ust21630)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 당일 실현손익 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | N |  | ND:NASDAQ,NY:NYSE,NA:AMEX |
| Body | `stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `fc_krw_tp` | 외화원화구분 |  | Y | 1 | 0:외화,1:원화 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `tot_tdy_pl_amt` | 총당일실현손익 |  | N | 15 |  |
| Body | `tot_tdy_pl_amt_krw` | 총당일실현손익(원) |  | N | 15 |  |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- stex_nm` | 거래소코드명 |  | N | 20 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- cntr_sellq` | 체결매도수량 |  | N | 20 |  |
| Body | `- avg_buy_uv` | 매입평균가 |  | N | 12 |  |
| Body | `- cntr_sella` | 체결매도가 |  | N | 20 |  |
| Body | `- tdy_pl_amt` | 당일실현손익 |  | N | 15 |  |
| Body | `- pl_rt` | 실현수익률 |  | N | 12 |  |
| Body | `- cmsn` | 수수료 |  | N | 15 |  |
| Body | `- altx` | 제세금 |  | N | 15 |  |
| Body | `- exch_rate` | 환율 |  | N | 12 |  |
| Body | `- natn_nm` | 국가명 |  | N | 40 |  |

### Request Example
```json
{
    "stex_tp": "",
    "stk_cd": "",
    "fc_krw_tp": ""
}
```

### Response Example
```json
{
    "tot_tdy_pl_amt": "0.0000",
    "tot_tdy_pl_amt_krw": "-00000000014432",
    "result_list": [
        {
            "stex_nm": "미국",
            "stk_cd": "NVDA",
            "stk_nm": "엔비디아",
            "crnc_code": "USD",
            "cntr_sellq": "00000000000000000001",
            "avg_buy_uv": "319562.0000",
            "cntr_sella": "306159.0000",
            "tdy_pl_amt": "-14432.0000",
            "pl_rt": "-4.51",
            "cmsn": "1022.0000",
            "altx": "6.0000",
            "exch_rate": "1520.80",
            "natn_nm": "미국"
        }
    ],
    "return_code": 0,
    "return_msg": "해외주식 당일 실현손익 상세내역 조회 되었습니다."
}
```

---

## [ust21640] 미국주식 일별 종목별 실현손익
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 일별 종목별 실현손익(ust21640)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 일별 종목별 실현손익 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | N |  | ND:NASDAQ,NY:NYSE,NA:AMEX |
| Body | `stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `cntr_dt` | 체결일자 |  | Y | 8 | YYYYMMDD |
| Body | `fc_krw_tp` | 외화원화구분 |  | Y | 1 | 0:외화,1:원화 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `tot_pl_amt` | 총실현손익 |  | N | 15 |  |
| Body | `tot_pl_amt_krw` | 총실현손익(원) |  | N | 15 |  |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- stex_nm` | 거래소코드명 |  | N | 20 |  |
| Body | `- stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- cntr_sellq` | 체결매도수량 |  | N | 20 |  |
| Body | `- avg_buy_uv` | 매입평균가 |  | N | 12 |  |
| Body | `- cntr_sella` | 체결매도가 |  | N | 20 |  |
| Body | `- pl_amt` | 실현손익 |  | N | 15 |  |
| Body | `- pl_rt` | 실현수익률 |  | N | 12 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- cmsn` | 수수료 |  | N | 15 |  |
| Body | `- altx` | 제세금 |  | N | 15 |  |
| Body | `- exch_rate` | 환율 |  | N | 12 |  |
| Body | `- natn_nm` | 국가명 |  | N | 40 |  |

### Request Example
```json
{
    "stex_tp": "",
    "stk_cd": "",
    "cntr_dt": "20260611",
    "fc_krw_tp": "0"
}
```

### Response Example
```json
{
    "tot_pl_amt": "-9.4902",
    "tot_pl_amt_krw": "-00000000014432",
    "result_list": [
        {
            "stex_nm": "미국",
            "stk_nm": "엔비디아",
            "crnc_code": "USD",
            "cntr_sellq": "00000000000000000001",
            "avg_buy_uv": "210.1282",
            "cntr_sella": "201.3147",
            "pl_amt": "-9.4902",
            "pl_rt": "-4.51",
            "stk_cd": "NVDA",
            "cmsn": "0.6725",
            "altx": "0.0042",
            "exch_rate": "1520.80",
            "natn_nm": "미국"
        }
    ],
    "return_code": 0,
    "return_msg": "해외주식 일별 종목별 실현손익내역 조회 되었습니다."
}
```

---

## [ust21650] 미국주식 기간별 수익률 현황
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 기간별 수익률 현황(ust21650)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 기간별 수익률 현황 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `fr_dt` | 조회시작일자 |  | N | 8 | YYYYMMDD |
| Body | `to_dt` | 조회종료일자 |  | N | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `fr_entr` | 기간초예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_dfr_amt` | 기간초현금미수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_etc_loana` | 기간초기타대여금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_fc_entr` | 기간초외화예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_fc_dfr_amt` | 기간초외화미수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_fc_etc_loana` | 기간초외화기타대여금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_frgn_stk_evltv` | 기간초해외증권평가금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fr_tot_evltv` | 기간초순자산액계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_entr` | 기간말예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_dfr_amt` | 기간말현금미수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_etc_loana` | 기간말기타대여금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_fc_entr` | 기간말외화예수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_fc_dfr_amt` | 기간말외화미수금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_fc_etc_loana` | 기간말외화기타대여금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_frgn_stk_evltv` | 기간말해외증권평가금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `to_tot_evltv` | 기간말순자산액계 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fc_rcpta` | 기간내총외화입금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `fc_payma` | 기간내총외화출금 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `chg_rcpta` | 기간내외화매도 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `chg_payma` | 기간내외화매수 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `frgn_stk_inqa` | 기간내해외증권입고 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `frgn_stk_outqa` | 기간내해외증권출고 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `invt_bsamt` | 투자원금평잔 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `evlt_profit` | 평가손익 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| Body | `profit_rate` | 수익율 |  | N | 12 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `io_bsamt` | 기간내총입출금고평잔 |  | N | 12 | 단위: 원, 좌측 0-padding 처리된 12자리 숫자 |
| Body | `tern_rt` | 회전율 |  | N | 12 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

### Request Example
```json
{
    "fr_dt": "20260501",
    "to_dt": "20260507"
}
```

### Response Example
```json
{
    "fr_entr": "000000000000",
    "fr_dfr_amt": "000000000000",
    "fr_etc_loana": "000000000000",
    "fr_fc_entr": "023746065086",
    "fr_fc_dfr_amt": "000000000000",
    "fr_fc_etc_loana": "000000000000",
    "fr_frgn_stk_evltv": "000165918511",
    "fr_tot_evltv": "023911983597",
    "to_entr": "000000000000",
    "to_dfr_amt": "000000000000",
    "to_etc_loana": "000000000000",
    "to_fc_entr": "023435585406",
    "to_fc_dfr_amt": "000000000000",
    "to_fc_etc_loana": "000000000000",
    "to_frgn_stk_evltv": "000174683157",
    "to_tot_evltv": "023610268563",
    "fc_rcpta": "000000000000",
    "fc_payma": "000000000000",
    "chg_rcpta": "000000000000",
    "chg_payma": "000000000000",
    "frgn_stk_inqa": "000000000000",
    "frgn_stk_outqa": "000000000000",
    "invt_bsamt": "023911983597",
    "evlt_profit": "-00301715035",
    "profit_rate": "-1.26",
    "io_bsamt": "000000000000",
    "tern_rt": "0.04",
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다.."
}
```

---

## [ust21660] 미국주식 일별 실현손익
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 일별 실현손익(ust21660)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 일별 실현손익 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `strt_dt` | 시작일자 |  | N | 8 | YYYYMMDD |
| Body | `end_dt` | 종료일자 |  | N | 8 | YYYYMMDD |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `tot_buy_amt` | 총매수금액 |  | N | 12 |  |
| Body | `tot_sell_amt` | 총매도금액 |  | N | 12 |  |
| Body | `tot_pl_amt` | 총실현손익금액 |  | N | 12 |  |
| Body | `tot_cmsn` | 수수료합 |  | N | 12 |  |
| Body | `tot_tax` | 세금합 |  | N | 12 |  |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- trde_dt` | 매매일자 |  | N | 8 |  |
| Body | `- buy_amt` | 매수금액 |  | N | 12 |  |
| Body | `- sell_amt` | 매도금액 |  | N | 12 |  |
| Body | `- pl_amt` | 실현손익금액 |  | N | 12 |  |
| Body | `- cmsn` | 수수료 |  | N | 12 |  |
| Body | `- tax` | 세금 |  | N | 12 |  |

### Request Example
```json
{
    "strt_dt": "20260601",
    "end_dt": "20260613"
}
```

### Response Example
```json
{
    "tot_buy_amt": "112804.0000",
    "tot_sell_amt": "16200000.0000",
    "tot_pl_amt": "16194319.3186",
    "tot_cmsn": "0.8630",
    "tot_tax": "333.7200",
    "result_lsit": [
        {
            "trde_dt": "20260407",
            "buy_amt": "112804.0000",
            "sell_amt": "16200000.0000",
            "pl_amt": "16194319.3186",
            "cmsn": "0.8630",
            "tax": "333.7200"
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---

## [ust31301] 환율 조회
- **메뉴 위치**: 미국주식 > 환전 > 환율 조회(ust31301)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/exchange`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: - 환전 적용 환율을 조회하는 tr입니다.
  다만 ust3102 (환전 신청)에서 환전 시, 환율 변동으로 인해 ust31301(환율조회)로 조회한 환율과 실제 환전 적용환율이 다를 수 있으며, 환전 후 취소 또는 변경 처리는 불가합니다.

- 환전 관련 유의사항은 영웅문 Global[3130] &#39;외화 환전 - 외화환전신청&#39; 화면의 유의사항을 확인하시기 바랍니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `exch_tp` | 환전구분 |  | Y | 1 | 1:원화(KRW)->달러(USD), 2:달러(USD)->원화(KRW) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `sell_aplc_exrt` | 매도적용환율 |  | N | 12 | 소수점 둘째 자리까지 포맷된 숫자 |
| Body | `buy_aplc_exrt` | 매수적용환율 |  | N | 12 | 소수점 둘째 자리까지 포맷된 숫자 |
| Body | `aplc_exrt` | 적용환율 |  | N | 12 | 실제 환전에 적용되는 환율입니다. <br>다만, 환전시점 시 환율 변동으로 인해 조회 환율과 적용 환율이 다를 수 있으며 환전 신청 전 꼭 환율을 확인해주시기 바랍니다 |
| Body | `exrt_tp_nm` | 환율구분명 |  | N | 40 |  |
| Body | `spcl_bf_exrt` | 우대율 적용 전 환율 |  | N | 12 | 환율 우대율을 적용하기 전 환율 입니다. 실제 환전은 aplc_exrt (적용환율)로 진행됩니다 |
| Body | `exrt_spcl_rt` | 환율우대율 |  | N | 12 |  |

### Request Example
```json
{
    "exch_tp": "1"
}
```

### Response Example
```json
{
    "sell_aplc_exrt": "0.00",
    "buy_aplc_exrt": "1533.20",
    "aplc_exrt": "1533.200000",
    "exrt_tp_nm": "고시환율",
    "spcl_bf_exrt": "1533.20",
    "exrt_spcl_rt": "0.00",
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---

## [00] 주문체결
- **메뉴 위치**: 국내주식 > 실시간시세 > 주문체결(00)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 실시간 항목 00(주문체결)은 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문 접수, 체결, 정정, 취소 등 매매가 발생할 경우 데이터가 수신됩니다. 

ACCESS TOKEN 발급과 상관없이 해당 종목의 체결내역을 보고싶으신 경우에 0B를 이용 부탁드립니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y | 10 | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y | 4 |  |
| Body | `refresh` | 기존등록유지여부 |  | Y | 1 | 등록(REG)시<br><br>0:기존유지안함 1:기존유지(Default)<br><br>0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N | 100 |  |
| Body | `- type` | 실시간 항목 |  | Y | 2 | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 9201` | 계좌번호 |  | N |  | 고유 계좌번호 10자리 |
| Body | `- - 9203` | 주문번호 |  | N |  | 주문번호 7자리 |
| Body | `- - 9205` | 관리자사번 |  | N |  |  |
| Body | `- - 9001` | 종목코드,업종코드 |  | N |  |  |
| Body | `- - 912` | 주문업무분류 |  | N |  |  |
| Body | `- - 913` | 주문상태 |  | N |  | 접수, 체결, 확인, 취소, 거부 |
| Body | `- - 302` | 종목명 |  | N |  |  |
| Body | `- - 900` | 주문수량 |  | N |  | 단위: 1주 |
| Body | `- - 901` | 주문가격 |  | N |  | 단위: 원 |
| Body | `- - 902` | 미체결수량 |  | N |  | 단위: 1주 |
| Body | `- - 903` | 체결누계금액 |  | N |  | 단위: 원 |
| Body | `- - 904` | 원주문번호 |  | N |  | 원 주문이 없는 경우 '0000000'으로 출력 |
| Body | `- - 905` | 주문구분 |  | N |  | "+/-", 매도, 매수, 매도정정, 매수정정, 매수취소, 매도취소<br><br><br>※ 영웅문4에서 적색으로 표기되어있으면 +가, 청색으로 표기되어있으면 -가 앞에 기재됩니다 |
| Body | `- - 906` | 매매구분 |  | N |  | 보통, 시장가, 조건부지정가, 최유리지정가, 최우선지정가, 보통(IOC), 시장가(IOC), 최유리(IOC), 보통(FOK), 시장가(FOK), 최유리(FOK), 스톰지정가, 중간가, 중간가(IOC), 중간가(FOK), 장전시간외, 장후시간외, 시간외대량, 시간외바스켓, 시간외자사주, 시간외단일가 |
| Body | `- - 907` | 매도수구분 |  | N |  | 1:매도, 2:매수 |
| Body | `- - 908` | 주문/체결시간 |  | N |  | HHmmss |
| Body | `- - 909` | 체결번호 |  | N |  |  |
| Body | `- - 910` | 체결가 |  | N |  |  |
| Body | `- - 911` | 체결량 |  | N |  |  |
| Body | `- - 10` | 현재가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 27` | (최우선)매도호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 28` | (최우선)매수호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 914` | 단위체결가 |  | N |  |  |
| Body | `- - 915` | 단위체결량 |  | N |  |  |
| Body | `- - 938` | 당일매매수수료 |  | N |  |  |
| Body | `- - 939` | 당일매매세금 |  | N |  |  |
| Body | `- - 919` | 거부사유 |  | N |  |  |
| Body | `- - 920` | 화면번호 |  | N |  | HTS화면번호 |
| Body | `- - 921` | 터미널번호 |  | N |  |  |
| Body | `- - 922` | 신용구분 |  | N |  | 실시간 체결용 |
| Body | `- - 923` | 대출일 |  | N |  | 실시간 체결용 |
| Body | `- - 10010` | 시간외단일가_현재가 |  | N |  |  |
| Body | `- - 2134` | 거래소구분 |  | N |  | 0:통합,1:KRX,2:NXT |
| Body | `- - 2135` | 거래소구분명 |  | N |  | 통합,KRX,NXT |
| Body | `- - 2136` | SOR여부 |  | N |  | Y,N |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": null,
    "- item": "",
    "- type": "00"
}
```

### Response Example
```json
#요청
{
    'trnm': 'REG',
    'return_code': 0,
    'return_msg': ''
}

#실시간 수신
{
    'data':[
        {
            'values': {
                '9201':'1111111111',
                '9203':'0000018',
                '9205':'',
                '9001':'005930',
                '912':'JJ',
                '913':'접수',
                '302':'삼성전자',
                '900':'1',
                '901':'0',
                '902':'1',
                '903':'0',
                '904':'0000000',
                '905':'+매수',
                '906':'시장가',
                '907':'2',
                '908':'094022',
                '909':'',
                '910':'',
                '911':'',
                '10':'+60700',
                '27':'+60700',
                '28':'-60000',
                '914':'',
                '915':'',
                '938':'0',
                '939':'0',
                '919':'0',
                '920':'',
                '921':'0701002',
                '922':'00',
                '923':'00000000',
                '10010':'',
                '2134':'1',
                '2135':'KRX',
                '2136':'Y'
            },
            'type':'00',
            'name':'주문체결',
            'item':'005930'
        }
    ],
    'trnm': 'REAL'
}
```

---

## [04] 잔고
- **메뉴 위치**: 국내주식 > 실시간시세 > 잔고(04)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 실시간 항목 04(잔고)는 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문 체결이 발생할 경우 데이터가 수신됩니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y | 10 | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y | 4 |  |
| Body | `refresh` | 기존등록유지여부 |  | Y | 1 | 등록(REG)시<br> <br>0:기존유지안함 1:기존유지(Default)<br><br>0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N | 104 |  |
| Body | `- type` | 실시간 항목 |  | Y | 2 | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 9201` | 계좌번호 |  | N |  | 고유 계좌번호 10자리 |
| Body | `- - 9001` | 종목코드,업종코드 |  | N |  |  |
| Body | `- - 917` | 신용구분 |  | N |  |  |
| Body | `- - 916` | 대출일 |  | N |  | YYYYMMDD |
| Body | `- - 302` | 종목명 |  | N |  |  |
| Body | `- - 10` | 현재가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 930` | 보유수량 |  | N |  | 단위: 1주 |
| Body | `- - 931` | 매입단가 |  | N |  | 단위: 원 |
| Body | `- - 932` | 총매입가(당일누적) |  | N |  | 단위: 원 |
| Body | `- - 933` | 주문가능수량 |  | N |  | 단위: 1주 |
| Body | `- - 945` | 당일순매수량 |  | N |  | 단위: 1주 |
| Body | `- - 946` | 매도/매수구분 |  | N |  | 계약,주 |
| Body | `- - 950` | 당일총매도손익 |  | N |  |  |
| Body | `- - 951` | Extra Item |  | N |  |  |
| Body | `- - 27` | (최우선)매도호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 28` | (최우선)매수호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 307` | 기준가 |  | N |  | 단위: 원 |
| Body | `- - 8019` | 손익률(실현손익) |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 957` | 신용금액 |  | N |  |  |
| Body | `- - 958` | 신용이자 |  | N |  |  |
| Body | `- - 918` | 만기일 |  | N |  | YYYYMMDD |
| Body | `- - 990` | 당일실현손익(유가) |  | N |  |  |
| Body | `- - 991` | 당일실현손익율(유가) |  | N |  |  |
| Body | `- - 992` | 당일실현손익(신용) |  | N |  |  |
| Body | `- - 993` | 당일실현손익율(신용) |  | N |  |  |
| Body | `- - 959` | 담보대출수량 |  | N |  |  |
| Body | `- - 924` | Extra Item |  | N |  |  |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": null,
    "- item": "",
    "- type": "04"
}
```

### Response Example
```json
#요청
{
    'trnm': 'REG',
    'return_code': 0,
    'return_msg': ''
}

#실시간 수신
{
    'data': [
        {
            'values': {
                '9201': '1111111111',
                '9001': '005930',
                '917': '00',
                '916': '00000000',
                '302': '삼성전자',
                '10': '-60150',
                '930': '102',
                '931': '154116',
                '932': '15719834',
                '933': '102',
                '945': '4',
                '946': '2',
                '950': '0',
                '951': '0',
                '27': '-60200',
                '28': '-60100',
                '307': '60300',
                '8019': '0.00',
                '957': '0',
                '958': '0',
                '918': '00000000',
                '990': '0',
                '991': '0.00',
                '992': '0',
                '993': '0.00',
                '959': '0',
                '924': '0'
            },
            'type': '04',
            'name': '현물잔고',
            'item': '005930'
        }
    ],
    'trnm': 'REAL'
}
```

---

## [0A] 주식기세
- **메뉴 위치**: 국내주식 > 실시간시세 > 주식기세(0A)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 특정 종목이 기세일때 발생하는 데이터로 시장에서 체결없이 현재가가 변경되는 대량매매나 거래소에서 종목 종가데이터 보정시 발생하는 실시간 입니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y | 10 | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y | 4 |  |
| Body | `refresh` | 기존등록유지여부 |  | Y | 1 | 등록(REG)시<br><br>0:기존유지안함 1:기존유지(Default)<br><br>0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N | 100 | 거래소별 종목코드, 업종코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| Body | `- type` | 실시간 항목 |  | Y | 2 | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지(등록,해지시에만 값 전송,데이터 실시간 수신시 미전송) |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 10` | 현재가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 11` | 전일대비 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 12` | 등락율 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 27` | (최우선)매도호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 28` | (최우선)매수호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 13` | 누적거래량 |  | N |  | 단위: 1주 |
| Body | `- - 14` | 누적거래대금 |  | N |  | 단위: 백만원 |
| Body | `- - 16` | 시가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 17` | 고가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 18` | 저가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 25` | 전일대비기호 |  | N |  | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| Body | `- - 26` | 전일거래량대비(계약,주) |  | N |  | 단위: 1주, 부호가 포함된 숫자 |
| Body | `- - 29` | 거래대금증감 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 30` | 전일거래량대비(비율) |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 31` | 거래회전율 |  | N |  | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 32` | 거래비용 |  | N |  |  |
| Body | `- - 311` | 시가총액(억) |  | N |  | 단위: 억원 |
| Body | `- - 567` | 상한가발생시간 |  | N |  | HHmmss |
| Body | `- - 568` | 하한가발생시간 |  | N |  | HHmmss |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": null,
    "- item": "005930",
    "- type": "0A"
}
```

### Response Example
```json
#요청
{
    'trnm': 'REG',
    'return_code': 0,
    'return_msg': ''
}

#실시간 수신
{
    'data': [
        {
            'values': {
                '10': '+86800',
                '11': '+19500',
                '12': '+28.97',
                '27': '+85200',
                '28': '+85100',
                '13': '367090',
                '14': '31642',
                '16': '+87400',
                '17': '+87400',
                '18': ' 67300',
                '25': '2',
                '26': '+131995',
                '29': '+15843118000',
                '30': '+156.15',
                '31': '0.01',
                '32': '157',
                '311': '5181771',
                '567': '154912',
                '568': '000000'
            },
            'type': '0A',
            'name': '주식기세',
            'item': '005930'
        }
    ],
    'trnm': 'REAL'
}
```

---

## [0B] 주식체결
- **메뉴 위치**: 국내주식 > 실시간시세 > 주식체결(0B)
- **HTTP Method**: `POST`
- **Request URL**: `/api/dostk/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 종목별 주식 체결 정보를 수신합니다.
※ item에 종목 코드를 설정해주세요.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y | 10 | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y | 4 |  |
| Body | `refresh` | 기존등록유지여부 |  | Y | 1 | 등록(REG)시<br>0:기존유지안함 1:기존유지(Default)<br> 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N | 100 | 거래소별 종목코드, 업종코드<br>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| Body | `- type` | 실시간 항목 |  | Y | 2 | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0B,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 20` | 체결시간 |  | N |  | HHmmss |
| Body | `- - 10` | 현재가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 11` | 전일대비 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 12` | 등락율 |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 27` | (최우선)매도호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 28` | (최우선)매수호가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 15` | 거래량 |  | N |  | +는 매수체결,-는 매도체결 |
| Body | `- - 13` | 누적거래량 |  | N |  | 단위: 1주 |
| Body | `- - 14` | 누적거래대금 |  | N |  | 단위: 백만원 |
| Body | `- - 16` | 시가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 17` | 고가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 18` | 저가 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 25` | 전일대비기호 |  | N |  | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| Body | `- - 26` | 전일거래량대비(계약,주) |  | N |  | 단위: 1주, 부호가 포함된 숫자 |
| Body | `- - 29` | 거래대금증감 |  | N |  | 단위: 원, 부호가 포함된 숫자 |
| Body | `- - 30` | 전일거래량대비(비율) |  | N |  | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 31` | 거래회전율 |  | N |  | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 32` | 거래비용 |  | N |  |  |
| Body | `- - 228` | 체결강도 |  | N |  | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| Body | `- - 311` | 시가총액(억) |  | N |  |  |
| Body | `- - 290` | 장구분 |  | N |  | 1: 장전 시간외 , 2: 장중 , 3: 장후 시간외 |
| Body | `- - 691` | K.O 접근도 |  | N |  |  |
| Body | `- - 567` | 상한가발생시간 |  | N |  | HHmmss |
| Body | `- - 568` | 하한가발생시간 |  | N |  | HHmmss |
| Body | `- - 851` | 전일 동시간 거래량 비율 |  | N |  |  |
| Body | `- - 1890` | 시가시간 |  | N |  |  |
| Body | `- - 1891` | 고가시간 |  | N |  |  |
| Body | `- - 1892` | 저가시간 |  | N |  |  |
| Body | `- - 1030` | 매도체결량 |  | N |  |  |
| Body | `- - 1031` | 매수체결량 |  | N |  |  |
| Body | `- - 1032` | 매수비율 |  | N |  |  |
| Body | `- - 1071` | 매도체결건수 |  | N |  |  |
| Body | `- - 1072` | 매수체결건수 |  | N |  |  |
| Body | `- - 1313` | 순간거래대금 |  | N |  |  |
| Body | `- - 1315` | 매도체결량_단건 |  | N |  |  |
| Body | `- - 1316` | 매수체결량_단건 |  | N |  |  |
| Body | `- - 1314` | 순매수체결량 |  | N |  |  |
| Body | `- - 1497` | CFD증거금 |  | N |  |  |
| Body | `- - 1498` | 유지증거금 |  | N |  |  |
| Body | `- - 620` | 당일거래평균가 |  | N |  |  |
| Body | `- - 732` | CFD거래비용 |  | N |  |  |
| Body | `- - 852` | 대주거래비용 |  | N |  |  |
| Body | `- - 9081` | 거래소구분 |  | N |  |  |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": null,
    "- item": "005930",
    "- type": "0B"
}
```

### Response Example
```json
#요청
{
    'trnm': 'REG',
    'return_code': 0,
    'return_msg': ''
}

#실시간 수신
{
    'trnm': 'REAL',
    'data': [
        {
            'type': '0B',
            'name': '주식체결',
            'item': '005930',
            'values': {
                '20': '165208',
                '10': '-20800',
                '11': '-50',
                '12': '-0.24',
                '27': '-20800',
                '28': '-20700',
                '15': '+82',
                '13': '30379732',
                '14': '632640',
                '16': '20850',
                '17': '+21150',
                '18': '-20450',
                '25': '5',
                '26': '-1057122',
                '29': '-22041267850',
                '30': '-96.64',
                '31': '36.67',
                '32': '44',
                '228': '98.92',
                '311': '17230',
                '290': '2',
                '691': '0',
                '567': '000000',
                '568': '000000',
                '851': '',
                '1890': '',
                '1891': '',
                '1892': '',
                '1030': '',
                '1031': '',
                '1032': '',
                '1071': '',
                '1072': '',
                '1313': '',
                '1315': '',
                '1316': '',
                '1314': '',
                '1497': '',
                '1498': '',
                '620': '',
                '732': '',
                '852': '',
                '9081': '1'
            }
        }
    ]
}
```

---

## [F4] 미국주식 실시간 주문 확인
- **메뉴 위치**: 미국주식 > 실시간시세 > 미국주식 실시간 주문 확인(F4)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 실시간 항목 F4(미국주식 실시간 주문 확인)은 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문이 발생할 경우 데이터가 수신됩니다

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y |  | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y |  |  |
| Body | `refresh` | 기존등록유지여부 |  | Y |  | 등록(REG)시<br><br>기존유지안함 1:기존유지(Default)<br><br> 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | Map구조 {종목코드, 거래소코드, 국가구분} ex) item: [{"jmcode":"NVDA", "stex_tp":"ND"}] |
| Body | `- type` | 실시간 항목 |  | Y |  | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- stexTp` | 거래소구분 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 9201` | 계좌번호 |  | N |  |  |
| Body | `- - 9203` | 주문번호 |  | N |  |  |
| Body | `- - 9001` | 종목,업종코드 |  | N |  |  |
| Body | `- - 905` | 주문구분 |  | N |  |  |
| Body | `- - 907` | 매도수구분 |  | N |  |  |
| Body | `- - 904` | 원주문번호 |  | N |  |  |
| Body | `- - 900` | 주문수량 |  | N |  |  |
| Body | `- - 901` | 주문가격 |  | N |  |  |
| Body | `- - 906` | 매매구분 |  | N |  |  |
| Body | `- - 913` | 주문상태 |  | N |  |  |
| Body | `- - 908` | 주문/체결시간 |  | N |  |  |
| Body | `- - 50810` | 주문STOP가격 |  | N |  |  |
| Body | `- - 8043` | 통화코드 |  | N |  |  |
| Body | `- - 50841` | 예약구분 |  | N |  |  |
| Body | `- - 55190` | (재무)국가코드 사용 |  | N |  |  |
| Body | `- - 1091` | 국가명 |  | N |  |  |
| Body | `- - 50072` | 매도수구분명 |  | N |  |  |
| Body | `- - 302` | 종목명 |  | N |  |  |
| Body | `- - 50073` | 매매구분명 |  | N |  |  |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": "",
    "- item": "[{\"jmcode\":\"NVDA\",\"stex_tp\":\"ND\"}]",
    "- type": "F4"
}
```

### Response Example
```json
{
    "data": [
        {
            "values": {
                "302": "엔비디아",
                "900": "1",
                "901": "198.4200",
                "904": "000000000",
                "905": "10",
                "906": "00",
                "907": "02",
                "908": "105247",
                "913": "주문전송",
                "1091": "미국",
                "8043": "USD",
                "8046": "000030",
                "9001": "NVDA",
                "9201": "8985024710",
                "9203": "000000027",
                "50072": "매수",
                "50073": "지정가",
                "50810": "000000000000",
                "50841": "0",
                "55190": "001"
            },
            "type": "F4",
            "name": "해외주식주문",
            "item": "NVDA"
        }
    ],
    "trnm": "REAL"
}
```

---

## [F5] 미국주식 실시간 체결
- **메뉴 위치**: 미국주식 > 실시간시세 > 미국주식 실시간 체결(F5)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 실시간 항목 F5(미국주식 실시간 주문 체결)은 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문 접수, 체결 등 매매가 발생할 경우 데이터가 수신됩니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y |  | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y |  |  |
| Body | `refresh` | 기존등록유지여부 |  | Y |  | 등록(REG)시<br><br>기존유지안함 1:기존유지(Default)<br><br> 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | Map구조 {종목코드, 거래소코드, 국가구분} ex) item: [{"jmcode":"NVDA", "stex_tp":"ND"}] |
| Body | `- type` | 실시간 항목 |  | Y |  | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 1091` | 국가명 |  | N |  |  |
| Body | `- - 8046` | 거래소코드 |  | N |  |  |
| Body | `- - 9001` | 종목코드 |  | N |  |  |
| Body | `- - 302` | 종목명 |  | N |  |  |
| Body | `- - 904` | 원주문번호 |  | N |  |  |
| Body | `- - 9203` | 주문번호 |  | N |  |  |
| Body | `- - 905` | 주문구분 |  | N |  |  |
| Body | `- - 907` | 매도수구분 |  | N |  |  |
| Body | `- - 908` | 주문/체결시간 |  | N |  |  |
| Body | `- - 913` | 주문상태 |  | N |  |  |
| Body | `- - 900` | 주문수량 |  | N |  |  |
| Body | `- - 901` | 주문가격 |  | N |  |  |
| Body | `- - 902` | 미체결수량 |  | N |  |  |
| Body | `- - 909` | 체결번호 |  | N |  |  |
| Body | `- - 910` | 체결가 |  | N |  |  |
| Body | `- - 911` | 체결량 |  | N |  |  |
| Body | `- - 930` | 보유수량 |  | N |  |  |
| Body | `- - 931` | 매입단가 |  | N |  |  |
| Body | `- - 934` | 당일매도수량 사용 |  | N |  |  |
| Body | `- - 936` | 당일매수수량 사용 |  | N |  |  |
| Body | `- - 8004` | 전일매도수량 |  | N |  |  |
| Body | `- - 8005` | 전일매수수량 |  | N |  |  |
| Body | `- - 8018` | 손익금액 |  | N |  |  |
| Body | `- - 8019` | 손익율 |  | N |  |  |
| Body | `- - 8043` | 통화코드 |  | N |  |  |
| Body | `- - 8075` | 세금 사용 |  | N |  |  |
| Body | `- - 9201` | 계좌번호 |  | N |  |  |
| Body | `- - 13006` | 수수료 사용 |  | N |  |  |
| Body | `- - 50072` | 매도수구분명 |  | N |  |  |
| Body | `- - 50073` | 매매구분명 |  | N |  |  |
| Body | `- - 50724` | 실현손익매입금 사용 |  | N |  |  |
| Body | `- - 50725` | 환전실현손익매입금액 사용 |  | N |  |  |
| Body | `- - 50810` | 주문STOP가격 |  | N |  |  |
| Body | `- - 50841` | 예약구분 |  | N |  |  |
| Body | `- - 50844` | 환전실현손익금액 사용 |  | N |  |  |
| Body | `- - 55190` | (재무)국가코드 사용 |  | N |  |  |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": "",
    "- item": "[{\"jmcode\":\"NVDA\",\"stex_tp\":\"ND\"}]",
    "- type": "F5"
}
```

### Response Example
```json
{
    "data": [
        {
            "values": {
                "302": "엔비디아",
                "900": "1",
                "901": "0000198.4200",
                "902": "1",
                "904": "000000000",
                "905": "25",
                "907": "02",
                "908": "105247",
                "909": "000000000",
                "910": "000000000000",
                "911": "0",
                "913": "접수",
                "930": "54",
                "931": "0000185.0305",
                "934": "0",
                "936": "0",
                "1091": "미국",
                "8004": "0",
                "8005": "0",
                "8018": "0.0000",
                "8019": "0.0000",
                "8043": "USD",
                "8046": "000030",
                "8075": "000000000000",
                "9001": "NVDA",
                "9201": "8985024710",
                "9203": "000000027",
                "13006": "000000000000",
                "50072": "매수",
                "50073": "지정가",
                "50724": "000000000000",
                "50725": "000000000000",
                "50810": "0000000.0000",
                "50841": "0",
                "50844": "000000000000000",
                "55190": "001"
            },
            "type": "F5",
            "name": "해외주식체결",
            "item": "NVDA"
        }
    ],
    "trnm": "REAL"
}
```

---

## [FE] 미국주식 실시간 체결가
- **메뉴 위치**: 미국주식 > 실시간시세 > 미국주식 실시간 체결가(FE)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/websocket`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: - 미국주식 종목의 현재 체결가를 확인하는 API입니다.

- 미국주식 시세의 경우 개인 고객 대상으로 별도 신청 없이 나스닥 토탈뷰(실시간 시세)를 무료로 제공하고 있습니다.

- 유료 시세 서비스를 이용하시더라도 REST API의 경우 무료 시세로만 제공하고 있습니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `trnm` | 서비스명 |  | Y |  | REG : 등록 , REMOVE : 해지 |
| Body | `grp_no` | 그룹번호 |  | Y |  |  |
| Body | `refresh` | 기존등록유지여부 |  | Y |  | 등록(REG)시<br><br>기존유지안함 1:기존유지(Default)<br><br> 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지<br><br>해지(REMOVE)시 값 불필요 |
| Body | `data` | 실시간 등록 리스트 |  |  |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | Map구조 {종목코드, 거래소코드, 국가구분} ex) item: [{"jmcode":"NVDA", "stex_tp":"ND"}] |
| Body | `- type` | 실시간 항목 |  | Y |  | TR 명(0A,0B....) |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `return_code` | 결과코드 |  | N |  | 통신결과에대한 코드<br>(등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시 미전송) |
| Body | `return_msg` | 결과메시지 |  | N |  | 통신결과에대한메시지 |
| Body | `trnm` | 서비스명 |  | N |  | 등록,해지요청시 요청값 반환 , 실시간수신시 REAL 반환 |
| Body | `data` | 실시간 등록리스트 |  | N |  |  |
| Body | `- type` | 실시간항목 |  | N |  | TR 명(0A,0B....) |
| Body | `- name` | 실시간 항목명 |  | N |  |  |
| Body | `- item` | 실시간 등록 요소 |  | N |  | 종목코드 |
| Body | `- values` | 실시간 값 리스트 |  | N |  |  |
| Body | `- - 10` | 현재가 |  | N |  |  |
| Body | `- - 11` | 전일대비 |  | N |  |  |
| Body | `- - 12` | 등락율 |  | N |  |  |
| Body | `- - 13` | 누적거래량 |  | N |  |  |
| Body | `- - 14` | 누적거래대금 |  | N |  |  |
| Body | `- - 15` | 체결량 |  | N |  |  |
| Body | `- - 16` | 시가 |  | N |  |  |
| Body | `- - 17` | 고가 |  | N |  |  |
| Body | `- - 18` | 저가 |  | N |  |  |
| Body | `- - 20` | 시간 |  | N |  |  |
| Body | `- - 22` | 체결일자 |  | N |  |  |
| Body | `- - 25` | 전일대비기호 |  | N |  |  |
| Body | `- - 27` | (최우선)매도호가 |  | N |  |  |
| Body | `- - 28` | (최우선)매수호가 |  | N |  |  |
| Body | `- - 30` | 전일거래량대비(비율) |  | N |  |  |
| Body | `- - 228` | 체결강도 |  | N |  |  |
| Body | `- - 290` | 장구분 |  | N |  |  |
| Body | `- - 51020` | 현지 체결시간 |  | N |  |  |

### Request Example
```json
{
    "trnm": "REG",
    "grp_no": "1",
    "refresh": "1",
    "data": "",
    "- item": "[{\"jmcode\":\"NVDA\",\"stex_tp\":\"ND\"}]",
    "- type": "FE"
}
```

### Response Example
```json
{
    "data": [
        {
            "values": {
                "10": "+198.5000",
                "11": "+3.5300",
                "12": "+1.81",
                "13": "166476665",
                "14": "36384473.963000",
                "15": "+15",
                "16": "+197.2400",
                "17": "+200.6300",
                "18": "+195.1100",
                "20": "215300",
                "22": "20260630",
                "25": "2",
                "27": "+198.5400",
                "28": "+198.4800",
                "30": "+11.85",
                "228": "500.00",
                "290": "4",
                "51020": "215300"
            },
            "type": "FE",
            "name": "미국체결",
            "item": "NVDA",
            "stexTp": "ND"
        }
    ],
    "trnm": "REAL"
}
```

---

## [ust21070] 미국주식 원장잔고확인
- **메뉴 위치**: 미국주식 > 계좌 > 미국주식 원장잔고확인(ust21070)
- **HTTP Method**: `POST`
- **Request URL**: `/api/us/acnt`
- **Content-Type**: `application/json;charset=UTF-8`
- **개요**: 미국주식 원장 잔고 정보를 조회합니다.

### Request Parameters
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `authorization` | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 <br> 예) Bearer Egicyx... |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| Body | `stex_tp` | 거래소구분 |  | N | 2 | ND:NASDAQ,NY:NYSE,NA:AMEX |
| Body | `stk_cd` | 종목코드 |  | N | 12 | 미입력시 전체 |

### Response Fields
| 구분 | Element | 한글명 | Type | 필수여부 | 길이 | 설명 |
| --- | --- | --- | --- | --- | --- | --- |
| Header | `api-id` | TR명 | String | Y | 10 | 7자리 TR코드, ex) ka00001 |
| Header | `cont-yn` | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| Header | `next-key` | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| Body | `crnc_code` | 통화코드 |  | N | 3 | USD |
| Body | `tot_evlt_amt` | 총평가금액 |  | N | 15 |  |
| Body | `tot_prch_amt` | 총매입금액 |  | N | 15 |  |
| Body | `tot_pl_amt` | 총손익금액 |  | N | 15 |  |
| Body | `tot_pl_rt` | 총수익율 |  | N | 8 |  |
| Body | `tdy_book_amt` | 당일실현손익매입금액 |  | N | 15 |  |
| Body | `tdy_pl_amt` | 당일실현손익 |  | N | 15 |  |
| Body | `tdy_pl_rt` | 당일실현손익율(%) |  | N | 8 |  |
| Body | `tot_evlt_amt_krw` | 총평가금액(원) |  | N | 15 |  |
| Body | `tot_prch_amt_krw` | 총매입금액(원) |  | N | 15 |  |
| Body | `tot_pl_amt_krw` | 총손익금액(원) |  | N | 15 |  |
| Body | `tdy_book_amt_krw` | 당일실현손익매입금액(원) |  | N | 15 |  |
| Body | `tdy_pl_amt_krw` | 당일실현손익(원) |  | N | 15 |  |
| Body | `result_list` | 결과리스트 |  | N |  |  |
| Body | `- stex_nm` | 거래소명 |  | N | 30 |  |
| Body | `- crnc_code` | 통화코드 |  | N | 3 |  |
| Body | `- stk_cd` | 종목코드 |  | N | 12 |  |
| Body | `- frgn_stk_nm` | 종목명 |  | N | 50 |  |
| Body | `- qty` | 결제기준수량 |  | N | 12 |  |
| Body | `- poss_qty` | 보유수량 |  | N | 12 |  |
| Body | `- sell_alowq` | 매도가능수량 |  | N | 12 |  |
| Body | `- pred_cntr_sellq` | 전일매도수량 |  | N | 12 |  |
| Body | `- pred_cntr_buyq` | 전일매수수량 |  | N | 12 |  |
| Body | `- tdy_cntr_sellq` | 금일매도수량 |  | N | 12 |  |
| Body | `- tdy_cntr_buyq` | 금일매수수량 |  | N | 12 |  |
| Body | `- frgn_stk_book_uv` | 매입단가 |  | N | 12 |  |
| Body | `- now_pric` | 현재가 |  | N | 12 |  |
| Body | `- evlt_amt` | 평가금액 |  | N | 12 |  |
| Body | `- pl_amt` | 손익금액 |  | N | 12 |  |
| Body | `- pl_rt` | 손익율(%) |  | N | 8 |  |
| Body | `- evlt_amt_krw` | 평가금액(원) |  | N | 12 |  |
| Body | `- pl_amt_krw` | 손익금액(원) |  | N | 12 |  |
| Body | `- natn_nm` | 국가명 |  | N | 40 |  |
| Body | `- exch_rate` | 환율 |  | N | 12 |  |
| Body | `- frgn_stk_book_uv_krw` | 매입단가(원) |  | N | 12 |  |
| Body | `- now_pric_krw` | 현재가(원) |  | N | 12 |  |
| Body | `- frgn_stk_book_amt` | 매입금액 |  | N | 12 |  |
| Body | `- frgn_stk_book_amt_krw` | 매입금액(원) |  | N | 12 |  |

### Request Example
```json
{
    "stex_tp": "",
    "stk_cd": ""
}
```

### Response Example
```json
{
    "stex_tp": "000030",
    "crnc_code": "USD",
    "tot_evlt_amt": "156464.6701",
    "tot_prch_amt": "157279.9717",
    "tot_pl_amt": "-1599.6616",
    "tot_pl_rt": "-1.01",
    "tdy_book_amt": "0.0000",
    "tdy_pl_amt": "0.0000",
    "tdy_pl_rt": "0.00",
    "tot_evlt_amt_krw": "000000238530390",
    "tot_prch_amt_krw": "000000239773317",
    "tot_pl_amt_krw": "-00000002438684",
    "tdy_book_amt_krw": "000000000000000",
    "tdy_pl_amt_krw": "000000000000000",
    "result_list": [
        {
            "stex_nm": "미국",
            "crnc_code": "USD",
            "stk_cd": "AAPL",
            "frgn_stk_nm": "애플",
            "qty": "000000000395",
            "poss_qty": "000000000395",
            "sell_alowq": "000000000395",
            "pred_cntr_sellq": "000000000000",
            "pred_cntr_buyq": "000000000000",
            "tdy_cntr_sellq": "000000000000",
            "tdy_cntr_buyq": "000000000000",
            "frgn_stk_book_uv": "282.1603",
            "now_pric": "275.2400",
            "evlt_amt": "108719.8000",
            "pl_amt": "-3283.9512",
            "pl_rt": "-2.94",
            "evlt_amt_krw": "000165743335",
            "pl_amt_krw": "-00005006383",
            "natn_nm": "미국",
            "exch_rate": "1524.50",
            "frgn_stk_book_uv_krw": "000000430153",
            "now_pric_krw": "000000419603",
            "frgn_stk_book_amt": "111453.3212",
            "frgn_stk_book_amt_krw": "000169910588"
        }
    ],
    "return_code": 0,
    "return_msg": "계좌잔고내역이 조회되었습니다."
}
```

---
