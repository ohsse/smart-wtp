# EMS 스키마 분석 보고서

> 분석 대상: `ems_schema.md`
> 분석 일자: 2026-04-09
> 총 테이블 수: 95개

---

## 목차

1. [도메인 영역 분류](#1-도메인-영역-분류)
2. [핵심 용어 및 약어 정리](#2-핵심-용어-및-약어-정리)
3. [시계열 데이터 계층 구조](#3-시계열-데이터-계층-구조)
4. [전체 테이블 목록](#4-전체-테이블-목록)
5. [주요 테이블 상세](#5-주요-테이블-상세)
6. [테이블 간 참조 관계](#6-테이블-간-참조-관계)
7. [데이터 파티셔닝 전략](#7-데이터-파티셔닝-전략)

---

## 1. 도메인 영역 분류

| 도메인                   | 테이블 수 | 주요 테이블                                               |
| ------------------------ | --------- | --------------------------------------------------------- |
| **펌프 운영 시스템**     | 15개      | TB_CTR_PRF_PUMPMST_INF, TB_PUMP_COMBINATION, TB_PUMP_CAL  |
| **데이터 수집/로깅**     | 14개      | TB_RAWDATA, TB_RAWDATA_HOUR, TB_RAWDATA_DAY               |
| **전력 에너지 관리**     | 7개       | TB_PEAK_TAG_INF, TB_PEAK_PWR_PRDCT_RST, TB_PEAK_SCHDL_RST |
| **요금제 및 비용 분석**  | 6개       | TB_RT_RATE_INF, TB_RT_RATE_RST, TB_BASE_SAVINGS_TARGET    |
| **물리 인프라 구조**     | 10개      | TB_TNK_GRP_INF, TB_ZONE, TB_FAC, TB_TAGINFO               |
| **관망 해석 시뮬레이션** | 8개       | TB_FP_VAL, TB_FR_VAL, TB_EPA_PUMP_FLOW                    |
| **제어 및 모니터링**     | 7개       | TB_HMI_CTR_TAG, TB_EMS_ALR, TB_PTR_STRTG_INF              |
| **성능 곡선 분석**       | 3개       | TB_PRF_PRFRM_RST, TB_PRF_INVRT_RST, TB_PRF_PUMPYN_RST     |

### 도메인 상세 설명

#### I. 펌프 운영 시스템 (Pump Control System)

펌프의 마스터 정보, 최적 제어 결과, 운전 조합 및 상수를 관리한다.

- TB_CTR_PRF_PUMPMST_INF — 펌프 마스터 (성능곡선 태그)
- TB_CTR_PUMPYN_RST — 최적 펌프제어 펌프 결과
- TB_CTR_PUMPYN_INQUIRY — 최적 펌프제어 펌프 결과 조회
- TB_CTR_PUMP_REQ_OPT — 펌프 동작 선행조건
- TB_CTR_PUMP_OPT_LOG — 부분 AI 운전 이력 정보
- TB_CTR_OPT_RST — 최적 펌프제어 지역 결과
- TB_CTR_OPT_RST2 — 최적 펌프제어 지역 결과(2)
- TB_PUMP_COMBINATION — 펌프 운전 조합
- TB_PUMP_COMBINATION_INF — 펌프 운전조합 정의
- TB_PUMP_CAL — 펌프 가동조건 조합식 상수
- TB_PUMP_COMB_POWER — 펌프 조합 전력
- TB_PUMP_CTR_RTM — 펌프 제어 작동 시간
- TB_AI_MODE_RST — AI 모드 결과
- TB_PTR_CTR_INF — 최적 펌프 운영 태그 정의
- TB_PTR_STRTG_INF — 펌프 제어 전략 정보

#### II. 데이터 수집 및 로깅 (Data Collection & Logging)

SCADA에서 수집된 원시 데이터를 시간 단위별로 집계하여 저장한다.

- TB_RAWDATA — 분단위 SCADA 태그 데이터 (파티션)
- TB_RAWDATA_15MIN — 15분단위 SCADA 태그 데이터 (파티션)
- TB_RAWDATA_HOUR — 1시간단위 SCADA 태그 데이터 (파티션)
- TB_RAWDATA_HOUR_INGRT — 1시간단위 적산 SCADA 태그 데이터 (파티션)
- TB_RAWDATA_DAY — 1일단위 SCADA 태그 합계 데이터
- TB_RAWDATA_DAY_INGRT — 1일단위 적산 SCADA 태그 데이터
- TB_RAWDATA_MONTH — 1개월단위 SCADA 태그 합계 데이터
- TB_RAWDATA_MONTH_INGRT — 1개월단위 적산 SCADA 태그 데이터
- TB_RAWDATA_PMB_HOUR — 펌프 가동상태(PMB) 태그 전용
- TB_HMI_CTR_LOG — 펌프 실시간 자동 제어 태그 로그
- TB_PTR_CTR_ANLY_RST — 펌프 실시간 제어 분석 결과
- TB_PTR_ORC_RST — 펌프 성능 곡선 계수 (파티션)
- TB_LOG_TABLE — EMS 로그 테이블
- TB_MNL_CHN_LOG — 증감 및 감소 운영 결과 로그

#### III. 전력 에너지 관리 (Energy Management)

전력 피크 예측, 전력 생산 스케줄, 발생 전력 결과를 관리한다.

- TB_PEAK_TAG_INF — 피크 제어 태그 정보
- TB_PEAK_PWR_PRDCT_RST — 전력 예측 결과
- TB_PEAK_PRDCT_RST — 피크시간대 결과
- TB_PEAK_LOG — 전력피크 로그
- TB_PEAK_GNRTD_RST — 발생 전력 결과
- TB_PEAK_SCHDL_RST — 전력생산설비 스케줄 결과
- TB_PEAK_PRTCP_INF — 전력수요거래 참여 결과 (미사용)

#### IV. 요금제 및 비용 분석 (Rate & Cost Analysis)

최적 요금제 산출, 절감 목표 설정 및 결과를 관리한다.

- TB_RT_RATE_INF — 요금제 정보
- TB_RT_RATE_RST — 최적요금제 결과
- TB_RT_POWER_RST — 요금적용 전력 결과
- TB_RT_MSTR_INF — 요금제 코드 정보
- TB_RT_JOB_INF — 작업 정보
- TB_BASE_SAVINGS_TARGET — 전력 절감 목표
- TB_RST_SAVINGS_TARGET — 전력 절감 결과
- TB_GOALSETTING — 월간 전력사용 목표량

#### V. 물리 인프라 구조 (Infrastructure)

정수장, 시설, 설비, 배수지, 네트워크 노드/링크 구조를 정의한다.

- TB_ZONE — 시설 정보
- TB_FAC — 설비 정보
- TB_TAGINFO — 정수장 시설 및 설비 태그 정의
- TB_TNK_GRP_INF — 배수지 그룹 정보
- TB_CTR_TNK_INF — 배수지 및 분기 태그 정의
- TB_CTR_TNK_RST — 배수지 및 분기 결과
- TB_NODE_TAG — 노드 태그
- TB_LINK_GRP — 링크 그룹
- TB_WPP_TAG_CODE — 데이터 태그 정의
- TB_WPP_TAG_INF — Kafka Consumer 사용 태그 정의

#### VI. 관망 해석 시뮬레이션 (Network Analysis)

EPANET 기반 관망 분석 및 유압/유속 시뮬레이션 결과를 저장한다.

- TB_FP_VAL — 유압값
- TB_FP_SI_VAL — 유압값 (시뮬레이션)
- TB_FR_VAL — 유속값
- TB_FR_SI_VAL — 유속값 (시뮬레이션)
- TB_EPA_PUMP_FLOW — 관망분석 펌프 설정 및 유량 범위
- TB_EPA_SIM_RESV_FLOW — 관망해석 유량 설정
- TB_EPA_TAG_INFO — EPA 관망 분석 태그 정보
- TB_TOT_ALG — 통합 알고리즘
- TB_TOT_GRP — 통합 그룹

#### VII. 제어 및 모니터링 (Control & Monitoring)

HMI 태그, 알람, 실시간 반자동 제어를 관리한다.

- TB_HMI_CTR_TAG — HMI 제어 태그
- TB_HMI_ALR_TAG — HMI 알람 태그
- TB_HMI_TRNSP_TAG — HMI 전송 태그
- TB_PTR_HALF_CTR_TAG — 펌프 실시간 반자동 제어 태그
- TB_EMS_ALR — 알람 발생 정보
- TB_PEAK_RT_TAG_INF — 알고리즘 사용 태그 정보
- TB_PEAK_RT_TAGHRR_INF — 태그 계층 정보

#### VIII. 성능 곡선 분석 (Performance Curve)

펌프 및 인버터 펌프의 성능 곡선 데이터를 저장한다.

- TB_PRF_PRFRM_RST — 펌프 성능 곡선
- TB_PRF_INVRT_RST — 인버터 펌프 성능 곡선
- TB_PRF_PUMPYN_RST — 최적 펌프제어 펌프 결과

---

## 2. 핵심 용어 및 약어 정리

### 2.1 시스템/솔루션 약어

| 약어      | 풀네임                                   | 설명                           |
| --------- | ---------------------------------------- | ------------------------------ |
| **EMS**   | Energy Management System                 | 에너지 관리 시스템 (본 시스템) |
| **SCADA** | Supervisory Control And Data Acquisition | 현장 계측 데이터 수집 시스템   |
| **HMI**   | Human Machine Interface                  | 운전원 조작 화면               |
| **EPA**   | EPANET                                   | 관망 수리 해석 엔진            |
| **WPP**   | Water Purification Plant                 | 정수장                         |
| **AI**    | Artificial Intelligence                  | AI 기반 최적 제어              |

### 2.2 설비/위치 식별 코드

| 컬럼명        | 의미             | 데이터 타입                   |
| ------------- | ---------------- | ----------------------------- |
| `WPP_CODE`    | 정수장 코드      | varchar(7)                    |
| `ZONE_CODE`   | 시설 코드        | —                             |
| `FAC_CODE`    | 설비 코드        | —                             |
| `PUMP_GRP`    | 펌프 그룹 번호   | int(11)                       |
| `PUMP_IDX`    | 펌프 인덱스      | int                           |
| `PUMP_TYP`    | 펌프 유형        | int (1: 일반, 2: 인버터)      |
| `TNK_GRP_IDX` | 탱크 그룹 인덱스 | —                             |
| `TNK_IDX`     | 탱크 인덱스      | —                             |
| `TNK_TYP`     | 탱크 유형        | int(1) (1: 배수지, 2: 정수지) |
| `VLV_IDX`     | 밸브 인덱스      | —                             |
| `NODE_ID`     | 노드 ID          | —                             |
| `LINK_ID`     | 링크 ID          | —                             |

### 2.3 SCADA 태그 분류 체계

| 태그 접미사 | 측정 물리량                         | 단위 예시 |
| ----------- | ----------------------------------- | --------- |
| `PWI_TAG`   | 전력 순시 (Power Instantaneous)     | kW        |
| `PWQ_TAG`   | 전력 적산 (Power Quantity)          | kWh       |
| `FRI_TAG`   | 유량 순시 (Flow Rate Instantaneous) | m³/h      |
| `PRI_S_TAG` | 흡입압력 (Suction Pressure)         | m         |
| `PRI_D_TAG` | 토출압력 (Discharge Pressure)       | m         |
| `PRI_T_TAG` | 전체압력 (Total Pressure)           | m         |
| `TEI_TAG`   | 수온 (Temperature)                  | °C        |
| `LEI_TAG`   | 수위 (Level)                        | m         |
| `PMB_TAG`   | 펌프 작동 여부 (Pump Motor Bit)     | ON/OFF    |
| `CTI_TAG`   | 주파수 순시 (Current/Frequency)     | Hz        |
| `SPI_TAG`   | 속도 (Speed)                        | Hz        |

### 2.4 컬럼명 명명 규칙

#### 접미사 패턴

| 패턴     | 의미                       | 예시             |
| -------- | -------------------------- | ---------------- |
| `_RST`   | Result (결과)              | CTR_OPT_RST      |
| `_INF`   | Information (정보)         | CTR_TNK_INF      |
| `_TYP`   | Type (유형)                | PUMP_TYP         |
| `_YN`    | Yes/No 여부 (1/0 또는 Y/N) | PUMP_YN, USE_YN  |
| `_CD`    | Code (코드)                | WPP_CODE         |
| `_IDX`   | Index (인덱스)             | PUMP_IDX         |
| `_GRP`   | Group (그룹)               | PUMP_GRP         |
| `_NM`    | Name (이름)                | PUMP_NM          |
| `_TAG`   | SCADA 태그명               | PWI_TAG          |
| `_PRDCT` | Prediction (예측값)        | PRDCT_MEAN       |
| `_LIM`   | Limit (제한값)             | LWL_LIM, HWL_LIM |
| `_VAL`   | Value (값)                 | FC_VAL           |
| `_UNIT`  | Unit (단위)                | PWI_UNIT         |
| `_FEE`   | Fee (요금)                 | BASE_FEE         |
| `_PWR`   | Power (전력량)             | TOT_PWR          |

#### 접두사 패턴

| 패턴     | 의미              | 예시       |
| -------- | ----------------- | ---------- |
| `RGSTR_` | 등록 (Register)   | RGSTR_TIME |
| `UPDT_`  | 업데이트          | UPDT_TIME  |
| `ANLY_`  | 분석 (Analyze)    | ANLY_TIME  |
| `PRDCT_` | 예측 (Prediction) | PRDCT_TIME |
| `CNFRM_` | 확인 (Confirm)    | CNFRM_TIME |

### 2.5 물리량 약어

| 약어      | 물리량                | 단위     |
| --------- | --------------------- | -------- |
| `FLW`     | Flow (유량)           | m³/h     |
| `PRI`     | Pressure (압력/양정)  | m        |
| `PWR`     | Power (전력)          | kW / kWh |
| `FREQ`    | Frequency (주파수)    | Hz       |
| `TE`      | Temperature (수온)    | °C       |
| `LEI`     | Level (수위)          | m        |
| `HH_LOSS` | Head Loss (수두 손실) | m        |
| `FP`      | Fluid Pressure (유압) | —        |
| `FR`      | Flow Rate (유속)      | m/s      |
| `DUTY_H`  | 정격 양정             | m        |
| `DUTY_Q`  | 정격 유량             | m³/h     |

### 2.6 요금제 부하 시간대 구분

| 코드 접두사 | 시간대                     | 예시 컬럼          |
| ----------- | -------------------------- | ------------------ |
| `L_`        | 경부하 (Light load)        | L_PWR, L_ELCTR_FEE |
| `M_`        | 중간부하 (Medium load)     | M_PWR, M_ELCTR_FEE |
| `H_`        | 최대부하 (Heavy/Peak load) | H_PWR, H_ELCTR_FEE |

### 2.7 상태/플래그 코드값

| 컬럼       | 값    | 의미         |
| ---------- | ----- | ------------ |
| `PUMP_TYP` | 1     | 일반 펌프    |
| `PUMP_TYP` | 2     | 인버터 펌프  |
| `TNK_TYP`  | 1     | 배수지       |
| `TNK_TYP`  | 2     | 정수지       |
| `USE_YN`   | Y / 1 | 사용 중      |
| `USE_YN`   | N / 0 | 미사용       |
| `FLAG`     | 0     | Kafka 미전송 |
| `FLAG`     | 1     | 전송 대상    |
| `FLAG`     | 2     | 확인 완료    |
| `PEAK_YN`  | Y     | 피크 발생    |
| `PEAK_YN`  | N     | 피크 미발생  |

### 2.8 시간 단위 구분자

| 접미사   | 의미                    |
| -------- | ----------------------- |
| `_15MIN` | 15분 단위 집계          |
| `_HOUR`  | 1시간 단위 집계         |
| `_DAY`   | 1일 단위 집계           |
| `_MONTH` | 1개월 단위 집계         |
| `_INGRT` | 적산 (누적 합산) 데이터 |
| `_PMB`   | 펌프 가동 상태 전용     |

---

## 3. 시계열 데이터 계층 구조

```
SCADA 원시 데이터
│
├── TB_RAWDATA              (1분 단위, 월별 파티션: 2021-08 ~ 2030-12)
│     └── TS + TAGNAME + VALUE + QUALITY
│
├── TB_RAWDATA_15MIN        (15분 단위, 월별 파티션)
│
├── TB_RAWDATA_HOUR         (1시간 단위, 월별 파티션)
├── TB_RAWDATA_HOUR_INGRT   (1시간 적산, 월별 파티션)
│
├── TB_RAWDATA_DAY          (1일 단위, 연도별 파티션: 2023~2026)
├── TB_RAWDATA_DAY_INGRT    (1일 적산, 연도별 파티션)
│
├── TB_RAWDATA_MONTH        (1개월 단위, 연도별 파티션)
├── TB_RAWDATA_MONTH_INGRT  (1개월 적산, 연도별 파티션)
│
└── TB_RAWDATA_PMB_HOUR     (펌프 ON/OFF 전용, 시간 단위)
```

> **적산(INGRT)**: 순시값의 누적 합산. 전력량(kWh), 유량(m³) 등 누적 측정값에 사용.

---

## 4. 전체 테이블 목록

| #   | 테이블명                    | 설명                             | 비고                |
| --- | --------------------------- | -------------------------------- | ------------------- |
| 1   | TB_AI_MODE_RST              | AI 모드 결과                     |                     |
| 2   | TB_AVL_GRP                  | 사용가능 그룹                    |                     |
| 3   | TB_BASE_SAVINGS_TARGET      | 전력 절감 목표                   |                     |
| 4   | TB_BASE_SAVING_CHART        | 일별 전력 절감량                 |                     |
| 5   | TB_CTR_OPT_RST              | 최적 펌프제어 지역 결과          |                     |
| 6   | TB_CTR_OPT_RST2             | 최적 펌프제어 지역 결과(2)       |                     |
| 7   | TB_CTR_PRF_PUMPMST_INF      | 펌프 마스터 (성능곡선 태그)      |                     |
| 8   | TB_CTR_PUMPYN_INQUIRY       | 최적 펌프제어 펌프 결과 조회     |                     |
| 9   | TB_CTR_PUMPYN_RST           | 최적 펌프제어 펌프 결과          |                     |
| 10  | TB_CTR_PUMP_OPT_LOG         | 부분 AI 운전 이력 정보           |                     |
| 11  | TB_CTR_PUMP_REQ_OPT         | 펌프 동작 선행조건               |                     |
| 12  | TB_CTR_TNK_INF              | 배수지 및 분기 태그 정의         |                     |
| 13  | TB_CTR_TNK_INF_1119         | 배수지 및 분기 태그 정의         | 백업                |
| 14  | TB_CTR_TNK_RST              | 배수지 및 분기 결과              |                     |
| 15  | TB_EMS_ALR                  | 알람 발생 정보                   |                     |
| 16  | TB_EPA_PUMP_FLOW            | 관망분석 펌프 설정 및 유량 범위  |                     |
| 17  | TB_EPA_SIM_RESV_FLOW        | 관망해석 유량 설정               |                     |
| 18  | TB_EPA_TAG_INFO             | EPA 관망 분석 태그 정보          |                     |
| 19  | TB_FAC                      | 설비 정보                        |                     |
| 20  | TB_FAC_OLD                  | 설비 정보 (구)                   | 구버전              |
| 21  | TB_FP_SI_VAL                | 유압값 (시뮬레이션)              |                     |
| 22  | TB_FP_VAL                   | 유압값                           |                     |
| 23  | TB_FR_SI_VAL                | 유속값 (시뮬레이션)              |                     |
| 24  | TB_FR_VAL                   | 유속값                           |                     |
| 25  | TB_GOALSETTING              | 월간 전력사용 목표량             |                     |
| 26  | TB_HMI_ALR_TAG              | HMI 알람 태그                    |                     |
| 27  | TB_HMI_CTR_LOG              | 펌프 실시간 자동 제어 태그 로그  |                     |
| 28  | TB_HMI_CTR_TAG              | HMI 제어 태그                    |                     |
| 29  | TB_HMI_TRNSP_TAG            | HMI 전송 태그                    |                     |
| 30  | TB_LINK_GRP                 | 링크 그룹                        |                     |
| 31  | TB_LOG_TABLE                | EMS 로그 테이블                  |                     |
| 32  | TB_MERGE                    | —                                | 사용 여부 검토 필요 |
| 33  | TB_MNL_CHN_LOG              | 증감 및 감소 운영 결과 로그      |                     |
| 34  | TB_MONTHLY_PEAK             | 월별 최대 피크값 요약            |                     |
| 35  | TB_NODE_TAG                 | 노드 태그                        |                     |
| 36  | TB_NODE_TAG_11190           | 노드 태그                        | 백업                |
| 37  | TB_OPER_INF                 | 운영 정보                        |                     |
| 38  | TB_PEAK_GNRTD_RST           | 발생 전력 결과                   |                     |
| 39  | TB_PEAK_LOG                 | 전력피크 로그                    |                     |
| 40  | TB_PEAK_PRDCT_RST           | 피크시간대 결과                  |                     |
| 41  | TB_PEAK_PRTCP_INF           | 전력수요거래 참여 결과           | 미사용              |
| 42  | TB_PEAK_PWR_PRDCT_RST       | 전력 예측 결과                   |                     |
| 43  | TB_PEAK_RT_TAGHRR_INF       | 태그 계층 정보                   |                     |
| 44  | TB_PEAK_RT_TAG_INF          | 알고리즘 사용 태그 정보          |                     |
| 45  | TB_PEAK_SCHDL_RST           | 전력생산설비 스케줄 결과         |                     |
| 46  | TB_PEAK_TAG_INF             | 피크 제어 태그 정보              |                     |
| 47  | TB_PEAK_TAG_INF_GM_250725   | 피크 제어 태그 정보 (GM)         | 백업                |
| 48  | TB_PEAK_TAG_INF_HP_250725   | 피크 제어 태그 정보 (HP)         | 백업                |
| 49  | TB_PRF_INVRT_RST            | 인버터 펌프 성능 곡선            |                     |
| 50  | TB_PRF_PRFRM_RST            | 펌프 성능 곡선                   |                     |
| 51  | TB_PRF_PUMPYN_RST           | 최적 펌프제어 펌프 결과          |                     |
| 52  | TB_PRODUCER_DATA            | —                                | 미사용              |
| 53  | TB_PTR_CTR_ANLY_RST         | 펌프 실시간 제어 분석 결과       |                     |
| 54  | TB_PTR_CTR_INF              | 최적 펌프 운영 태그 정의         |                     |
| 55  | TB_PTR_HALF_CTR_TAG         | 펌프 실시간 반자동 제어 태그     |                     |
| 56  | TB_PTR_ORC_RST              | 펌프 성능 곡선 계수              | 파티션              |
| 57  | TB_PTR_STRTG_INF            | 펌프 제어 전략 정보              |                     |
| 58  | TB_PUMP_CAL                 | 펌프 가동조건 조합식 상수        |                     |
| 59  | TB_PUMP_CAL_0718            | 펌프 가동조건 조합식 상수        | 백업                |
| 60  | TB_PUMP_CAL_20250418        | 펌프 가동조건 조합식 상수        | 백업                |
| 61  | TB_PUMP_CAL_20250528        | 펌프 가동조건 조합식 상수        | 백업                |
| 62  | TB_PUMP_CAL_250718          | 펌프 가동조건 조합식 상수        | 백업                |
| 63  | TB_PUMP_CAL_250812          | 펌프 가동조건 조합식 상수        | 백업                |
| 64  | TB_PUMP_CAL_260324          | 펌프 가동조건 조합식 상수        | 백업                |
| 65  | TB_PUMP_CAL_BACKUP          | 펌프 가동조건 조합식 상수        | 백업                |
| 66  | TB_PUMP_CAL_OLD             | 펌프 가동조건 조합식 상수 (구)   | 구버전              |
| 67  | TB_PUMP_COMBINATION         | 펌프 운전 조합                   |                     |
| 68  | TB_PUMP_COMBINATION_INF     | 펌프 운전조합 정의               |                     |
| 69  | TB_PUMP_COMBINATION_INF_OLD | 펌프 운전조합 정의 (구)          | 구버전              |
| 70  | TB_PUMP_COMBINATION_OLD     | 펌프 운전 조합 (구)              | 구버전              |
| 71  | TB_PUMP_COMB_POWER          | 펌프 조합 전력                   |                     |
| 72  | TB_PUMP_CTR_RTM             | 펌프 제어 작동 시간              |                     |
| 73  | TB_RAWDATA                  | 분단위 SCADA 태그 데이터         | 파티션              |
| 74  | TB_RAWDATA_15MIN            | 15분단위 SCADA 태그 데이터       | 파티션              |
| 75  | TB_RAWDATA_DAY              | 1일단위 SCADA 태그 합계 데이터   |                     |
| 76  | TB_RAWDATA_DAY_INGRT        | 1일단위 적산 SCADA 태그 데이터   |                     |
| 77  | TB_RAWDATA_HOUR             | 1시간단위 SCADA 태그 데이터      | 파티션              |
| 78  | TB_RAWDATA_HOUR_INGRT       | 1시간단위 적산 SCADA 태그 데이터 | 파티션              |
| 79  | TB_RAWDATA_MONTH            | 1개월단위 SCADA 태그 합계 데이터 |                     |
| 80  | TB_RAWDATA_MONTH_INGRT      | 1개월단위 적산 SCADA 태그 데이터 |                     |
| 81  | TB_RAWDATA_PMB_HOUR         | 펌프 가동상태(PMB) 태그 전용     |                     |
| 82  | TB_RST_SAVINGS_TARGET       | 전력 절감 결과                   |                     |
| 83  | TB_RT_JOB_INF               | 작업 정보                        |                     |
| 84  | TB_RT_MSTR_INF              | 요금제 코드 정보                 |                     |
| 85  | TB_RT_POWER_RST             | 요금적용 전력 결과               |                     |
| 86  | TB_RT_RATE_INF              | 요금제 정보                      |                     |
| 87  | TB_RT_RATE_RST              | 최적요금제 결과                  |                     |
| 88  | TB_TAGINFO                  | 정수장 시설 및 설비 태그 정의    |                     |
| 89  | TB_TAG_UNIT_INFO            | 태그 단위 정의                   |                     |
| 90  | TB_TNK_GRP_INF              | 배수지 그룹 정보                 |                     |
| 91  | TB_TOT_ALG                  | 통합 알고리즘                    |                     |
| 92  | TB_TOT_GRP                  | 통합 그룹                        |                     |
| 93  | TB_WPP_TAG_CODE             | 데이터 태그 정의                 |                     |
| 94  | TB_WPP_TAG_INF              | Kafka Consumer 사용 태그 정의    |                     |
| 95  | TB_ZONE                     | 시설 정보                        |                     |

---

## 5. 주요 테이블 상세

### TB_CTR_PRF_PUMPMST_INF — 펌프 마스터

| 컬럼명         | 타입         | 설명                   |
| -------------- | ------------ | ---------------------- |
| `WPP_CODE`     | varchar(7)   | 정수장 코드 (PK)       |
| `PUMP_IDX`     | int          | 펌프 인덱스 (PK)       |
| `PUMP_GRP`     | int          | 펌프 그룹 (PK)         |
| `PUMP_GRP_IDX` | int          | 펌프 그룹 내 순서 (PK) |
| `PUMP_TYP`     | int          | 펌프 유형 (PK)         |
| `PUMP_NM`      | varchar(100) | 펌프 이름              |
| `PUMP_CTR_TYP` | char(1)      | 펌프 제어 유형         |
| `DUTY_H`       | float        | 정격 양정              |
| `DUTY_Q`       | float        | 정격 유량              |
| `PRRT_TYP`     | varchar(9)   | 우선순위 유형          |
| `PRRT_RNK`     | int(10)      | 우선순위 순위          |
| `PWI_TAG`      | varchar      | 전력 순시 태그         |
| `PWQ_TAG`      | varchar      | 전력 적산 태그         |
| `FRI_TAG`      | varchar      | 유량 태그              |
| `PMB_TAG`      | varchar      | 펌프 작동 여부 태그    |
| `PRI_S_TAG`    | varchar      | 흡입압력 태그          |
| `PRI_D_TAG`    | varchar      | 토출압력 태그          |
| `TEI_TAG`      | varchar      | 수온 태그              |

### TB_RAWDATA — 분단위 SCADA 원시 데이터

| 컬럼명    | 타입        | 설명           |
| --------- | ----------- | -------------- |
| `TS`      | timestamp   | 측정 시각 (PK) |
| `TAGNAME` | varchar(45) | 태그명 (PK)    |
| `VALUE`   | —           | 측정값         |
| `QUALITY` | —           | 데이터 품질    |
| `SERVER`  | —           | 수집 서버      |

### TB_TNK_GRP_INF — 배수지 그룹

| 컬럼명        | 타입         | 설명                             |
| ------------- | ------------ | -------------------------------- |
| `TNK_GRP_IDX` | —            | 탱크 그룹 인덱스 (PK)            |
| `TNK_IDX`     | —            | 탱크 인덱스 (PK)                 |
| `VLV_IDX`     | —            | 밸브 인덱스 (PK)                 |
| `IN_FLW_IDX`  | —            | 유입 유량 인덱스 (PK)            |
| `OUT_FLW_IDX` | —            | 유출 유량 인덱스 (PK)            |
| `TNK_GRP_NM`  | varchar(200) | 탱크 그룹 이름                   |
| `TNK_NM`      | varchar(100) | 탱크 이름                        |
| `TNK_TYP`     | int(1)       | 탱크 유형 (1: 배수지, 2: 정수지) |
| `PUMP_GRP`    | int(11)      | 연결 펌프 그룹                   |
| `LEI_TAG`     | varchar(30)  | 수위 태그                        |
| `IN_FLW_TAG`  | varchar(30)  | 유입 유량 태그                   |
| `OUT_FLW_TAG` | varchar(30)  | 유출 유량 태그                   |
| `DMD_PRI`     | float        | 최소 요구 관압                   |
| `LWL_LIM`     | float        | 최저 수위 제한                   |
| `HWL_LIM`     | float        | 최고 수위 제한                   |
| `VLM`         | float        | 탱크 용적                        |

### TB_RT_RATE_RST — 최적 요금제 결과

| 컬럼명          | 타입    | 설명                  |
| --------------- | ------- | --------------------- |
| `ANLY_DATE`     | —       | 분석 일자 (PK)        |
| `DATA_BS_YMNTH` | —       | 데이터 기준 연월 (PK) |
| `RATE_IDX`      | —       | 요금제 인덱스 (PK)    |
| `TOT_PWR`       | int(11) | 전체 전력량           |
| `TOT_FEE`       | int(11) | 전체 요금             |
| `BASE_FEE`      | int(11) | 기본 요금             |
| `L_PWR`         | —       | 경부하 전력량         |
| `M_PWR`         | —       | 중간부하 전력량       |
| `H_PWR`         | —       | 최대부하 전력량       |
| `L_ELCTR_FEE`   | —       | 경부하 전기요금       |
| `M_ELCTR_FEE`   | —       | 중간부하 전기요금     |
| `H_ELCTR_FEE`   | —       | 최대부하 전기요금     |

### TB_PUMP_CAL — 펌프 운전 조건 상수

| 컬럼명           | 타입        | 설명             |
| ---------------- | ----------- | ---------------- |
| `PUMP_GRP`       | int(11)     | 펌프 그룹        |
| `C_IDX`          | int(11)     | 조합 인덱스      |
| `PUMP_COMB`      | varchar(30) | 펌프 조합        |
| `FC_VAL`         | double      | 유량 상수        |
| `FC_MIN_VAL`     | double      | 최소 유량        |
| `FC_MAX_VAL`     | double      | 최대 유량        |
| `P_ADD_VAL`      | double      | 압력 추가값      |
| `P_MUL_VAL`      | double      | 압력 배율        |
| `P_SQRT_MUL_VAL` | double      | 압력 제곱근 배율 |

---

## 6. 테이블 간 참조 관계

### 전체 데이터 흐름

```
[정수장 마스터]
TB_ZONE ──→ TB_FAC ──→ TB_TAGINFO
                              │
                              ▼
                        TB_RAWDATA (원시 데이터)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        TB_RAWDATA_HOUR  TB_RAWDATA_DAY  TB_RAWDATA_MONTH

[펌프 제어 흐름]
TB_CTR_PRF_PUMPMST_INF (마스터)
        │
        ├──→ TB_CTR_PUMPYN_RST (제어 결과)
        │         └──→ TB_CTR_PUMP_OPT_LOG
        │
        └──→ TB_PUMP_COMBINATION_INF
                   └──→ TB_PUMP_CAL (운전 상수)

[전력 관리 흐름]
TB_PEAK_TAG_INF
        │
        ├──→ TB_PEAK_PWR_PRDCT_RST (전력 예측)
        └──→ TB_PEAK_SCHDL_RST (스케줄)

[요금제 분석 흐름]
TB_RT_MSTR_INF ──→ TB_RT_RATE_RST ←── TB_RT_RATE_INF
                         │
                         └──→ TB_RT_POWER_RST

[배수지 흐름]
TB_TNK_GRP_INF ──→ TB_CTR_TNK_INF ──→ TB_CTR_TNK_RST
```

### 주요 참조 키

| 부모 테이블             | 자식 테이블           | 참조 키                      |
| ----------------------- | --------------------- | ---------------------------- |
| TB_CTR_PRF_PUMPMST_INF  | TB_CTR_PUMPYN_RST     | WPP_CODE, PUMP_GRP, PUMP_IDX |
| TB_CTR_PRF_PUMPMST_INF  | TB_CTR_PUMPYN_INQUIRY | WPP_CODE, PUMP_GRP, PUMP_IDX |
| TB_PUMP_COMBINATION_INF | TB_PUMP_CAL           | PUMP_GRP                     |
| TB_RT_MSTR_INF          | TB_RT_RATE_RST        | RATE_IDX                     |
| TB_CTR_TNK_INF          | TB_CTR_TNK_RST        | DSTRB_ID                     |
| TB_TAGINFO              | TB_RAWDATA            | TAGNAME                      |
| TB_ZONE                 | TB_TAGINFO            | ZONE_CODE                    |
| TB_FAC                  | TB_TAGINFO            | FAC_CODE                     |
| TB_CTR_PUMPYN_RST       | TB_CTR_OPT_RST        | OPT_IDX, PUMP_GRP, PUMP_IDX  |
| TB_PEAK_PRDCT_RST       | TB_PEAK_PWR_PRDCT_RST | ANLY_TIME                    |

---

## 7. 데이터 파티셔닝 전략

### 월별 파티션 테이블 (2021-08 ~ 2030-12)

수집 빈도가 높은 분/시간 단위 데이터에 적용.

| 테이블명              | 수집 주기      |
| --------------------- | -------------- |
| TB_RAWDATA            | 1분            |
| TB_RAWDATA_15MIN      | 15분           |
| TB_RAWDATA_HOUR       | 1시간          |
| TB_RAWDATA_HOUR_INGRT | 1시간 (적산)   |
| TB_PTR_ORC_RST        | 성능 곡선 계수 |

### 연도별 파티션 테이블 (2023 ~ 2026)

일/월 단위 집계 데이터에 적용.

| 테이블명               | 수집 주기    |
| ---------------------- | ------------ |
| TB_RAWDATA_DAY         | 1일          |
| TB_RAWDATA_DAY_INGRT   | 1일 (적산)   |
| TB_RAWDATA_MONTH       | 1개월        |
| TB_RAWDATA_MONTH_INGRT | 1개월 (적산) |

> 모든 파티션 테이블은 `p_future (MAXVALUE)` 파티션을 포함하여 향후 데이터를 수용한다.

---

## 요약

이 스키마는 **수도 시설(정수장)의 에너지 최적화 관리 시스템(EMS)**의 데이터베이스로, 다음 업무 흐름을 통합한다:

```
SCADA 데이터 수집
    → 펌프 최적 제어 (AI 기반)
    → 전력 피크 예측 및 대응
    → 요금제 최적화 분석
    → 절감 성과 측정
    → 관망 수리 해석 시뮬레이션
```
