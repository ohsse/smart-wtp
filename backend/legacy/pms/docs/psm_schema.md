# Mapper 기반 DB 스키마 추정서

## 목적
- 실제 MariaDB DDL에 접근할 수 없는 상태에서 `src/main/resources/mapper` 의 SQL만으로 테이블 구조를 유추한 문서입니다.
- 확정 스키마가 아니라, 서비스 코드와 조인 조건을 근거로 한 운영 추정치입니다.

## 분석 기준
- 근거 소스
  - `src/main/resources/mapper/*.xml`
  - `src/main/java/com/wapplab/pms/repository/*.java`
  - `src/test/java/com/wapplab/pms/repository/*Test.java`
- 신뢰도 기준
  - 높음: `INSERT`, `UPDATE`, `ON DUPLICATE KEY`, 반복 조인으로 구조가 비교적 명확함
  - 중간: 조회 컬럼은 충분하지만 PK/FK가 직접 드러나지 않음
  - 낮음: 단일 조회만 있고 의미를 단정하기 어려움

## 핵심 관계 요약
- `TB_PUMP_INF` 가 설비 기준정보의 중심 테이블입니다.
- `TB_PUMP_INF.MOTOR_ID` 는 `TB_AI_DIAG_MOTOR.MOTOR_ID`, `TB_AI_DIAG_PUMP.PUMP_ID` 와 연결됩니다.
- `TB_PUMP_INF.PUMP_SCADA_ID` 는 `TB_PUMP_SCADA.PUMP_SCADA_ID`, `TB_DIAG_MOTOR_PUMP.PUMP_SCADA_ID`, `TB_DIAG_MOTOR_PUMP_WINDING.PUMP_SCADA_ID`, `TB_JSON.PUMP_SCADA_ID` 와 연결됩니다.
- 시계열 데이터는 대부분 `ACQ_DATE` 기준이며, 복합 키 후보는 `장비 식별자 + ACQ_DATE` 패턴입니다.

## 1. 설비 / 기준정보

### `TB_PUMP_INF`
- 역할: 펌프/모터 설비 마스터
- 주요 컬럼: `GRP_IDX`, `GRP_NM`, `PUMP_IDX`, `PUMP_NM`, `MOTOR_ID`, `PUMP_SCADA_ID`, `CENTER_ID`, `SENSOR_COUNT`
- 태그 매핑 컬럼: `MOTOR_NDE_AMP_TAG`, `MOTOR_DE_AMP_TAG`, `PUMP_NDE_AMP_TAG`, `PUMP_DE_AMP_TAG`, `MOTOR_ALARM_TAG`, `PUMP_ALARM_TAG`, `EQ_ON_TAG`, `FREQUENCY_TAG`, `FLOW_RATE_TAG`, `PRESSURE_TAG`, `R_TEMP_TAG`, `S_TEMP_TAG`, `T_TEMP_TAG`, `BRG_MOTOR_DE_TEMP_TAG`, `BRG_MOTOR_NDE_TEMP_TAG`, `BRG_PUMP_DE_TEMP_TAG`, `BRG_PUMP_NDE_TEMP_TAG`, `DISCHARGE_PRESSURE_TAG`, `SUCTION_PRESSURE_TAG`
- PK 후보: `MOTOR_ID` 또는 `PUMP_SCADA_ID`
- 특징: 거의 모든 조회의 조인 기준점
- 신뢰도: 높음

### `TB_CHANNEL`
- 역할: 모터별 채널 정의
- 주요 컬럼: `MOTOR_ID`, `CHANNEL_ID`, `CHANNEL_NM`, `CHANNEL_NO`
- PK 후보: `MOTOR_ID + CHANNEL_ID`
- FK 후보: `MOTOR_ID -> TB_PUMP_INF.MOTOR_ID`
- 신뢰도: 중간

### `TB_SENSOR_INF`
- 역할: 알람 타입 메타정보
- 주요 컬럼: `SENSOR_TYPE`, `SENSOR_NAME`, `SENSOR_DECS`
- 조인 키: `SENSOR_NAME = alarm_type`
- 신뢰도: 중간

### `TB_GRAPH_THRESHOLD`
- 역할: 그래프 임계치 설정
- 주요 컬럼: `EQ_TYPE`, `GRAPH_TYPE`, `TH_VALUE`
- PK 후보: `EQ_TYPE + GRAPH_TYPE`
- 신뢰도: 낮음

### `TB_AL_SETTING`
- 역할: 진단 파라미터 설정값
- 주요 컬럼: `GRP_ID`, `MOTOR_ID`, `EQ_TYPE`, `CHANNEL_NM`, `PARM_NM`, `PARM_VALUE`
- PK 후보: `GRP_ID + MOTOR_ID + EQ_TYPE + CHANNEL_NM + PARM_NM`
- 특징: `updateSettingParm` 에서 사실상 복합 키로 사용
- 신뢰도: 높음

## 2. 원천 수집 / SCADA / 진동 데이터

### `TB_PUMP_SCADA`
- 역할: SCADA 시계열 적재 테이블
- 주요 컬럼: `PUMP_SCADA_ID`, `CENTER_ID`, `ACQ_DATE`, `EQ_ON`, `FREQUENCY`, `FLOW_RATE`, `PRESSURE`, `R_TEMP`, `S_TEMP`, `T_TEMP`, `BRG_MOTOR_DE_TEMP`, `BRG_MOTOR_NDE_TEMP`, `BRG_PUMP_DE_TEMP`, `BRG_PUMP_NDE_TEMP`, `DISCHARGE_PRESSURE`, `SUCTION_PRESSURE`, `PROC_STAT`
- PK/Unique 후보: `PUMP_SCADA_ID + CENTER_ID + ACQ_DATE`
- 근거: `insertRawData` 의 `ON DUPLICATE KEY UPDATE`, `insertScadaDto`
- 신뢰도: 높음

### `TB_MOTOR`
- 역할: 원시 진동 데이터 적재 테이블
- 주요 컬럼: `MOTOR_ID`, `EQUIPMENT_ID`, `CENTER_ID`, `CHANNEL_ID`, `ACQ_DATE`, `DATA_ARRAY`
- PK 후보: `MOTOR_ID + CHANNEL_ID + ACQ_DATE`
- 특징: 이름은 일반적이지만 실제로는 파형 원본 저장소에 가까움
- 신뢰도: 높음

### `TB_RMS`
- 역할: 채널별 RMS 이력
- 주요 컬럼: `MOTOR_ID`, `CHANNEL_ID`, `RMS`, `ACQ_DATE`
- PK 후보: `MOTOR_ID + CHANNEL_ID + ACQ_DATE`
- 신뢰도: 중간

### `TB_TIMEWAVE`
- 역할: 시점별 Time Wave 저장
- 주요 컬럼: `MOTOR_ID`, `CHANNEL_ID`, `ACQ_DATE`, `DATA_ARRAY`
- PK 후보: `MOTOR_ID + CHANNEL_ID + ACQ_DATE`
- 신뢰도: 중간

### `TB_SPECTRUM`
- 역할: 시점별 Spectrum 저장
- 주요 컬럼: `MOTOR_ID`, `CHANNEL_ID`, `ACQ_DATE`, `DATA_ARRAY`
- PK 후보: `MOTOR_ID + CHANNEL_ID + ACQ_DATE`
- 신뢰도: 중간

### `TB_FREQ`
- 역할: 스펙트럼 주파수 상세값 저장
- 주요 컬럼: `MOTOR_ID`, `CHANNEL_ID`, `ACQ_DATE`, `FREQ_TYPE`, `FREQ_VALUE`
- PK 후보: `MOTOR_ID + CHANNEL_ID + ACQ_DATE + FREQ_TYPE`
- 신뢰도: 중간

### `TB_JSON`
- 역할: 분포도 차트용 JSON 캐시
- 주요 컬럼: `PUMP_SCADA_ID`, `ACQ_DATE`, `JSON_DATA`
- 조회 방식: `PUMP_SCADA_ID` 기준 최신 1건
- 신뢰도: 낮음

### `TB_DSTRB`
- 역할: 분포도 수치 데이터
- 주요 컬럼: `DSTRB_IDX`, `PUMP_IDX`, `DSTRB_NAME`, `DSTRB_ORDER_NUMBER`, `DSTRB_VALUE`, `REG_DATE`
- PK 후보: `DSTRB_IDX`
- 조회 조건: `PUMP_IDX`, 최근 1주
- 신뢰도: 중간

## 3. 진단 결과 / 알람

### `TB_AI_DIAG_MOTOR`
- 역할: AI 기반 모터 진단 결과 시계열
- 주요 컬럼: `MOTOR_ID`, `ACQ_DATE`, `DE_RMS_AMP`, `NDE_RMS_AMP`, `MISALIGNMENT_AMP`, `UNBALANCE_AMP`, `ROTOR_AMP`, `DE_AMP`, `NDE_AMP`
- 알람 컬럼: `UNBALANCE_ALARM`, `MISALIGNMENT_ALARM`, `ROTOR_ALARM`, `DE_BPFO_ALARM`, `DE_BPFI_ALARM`, `DE_BSF_ALARM`, `DE_FTF_ALARM`, `NDE_BPFO_ALARM`, `NDE_BPFI_ALARM`, `NDE_BSF_ALARM`, `NDE_FTF_ALARM`, `DE_RMS_ALARM`, `NDE_RMS_ALARM`
- PK 후보: `MOTOR_ID + ACQ_DATE`
- 신뢰도: 높음

### `TB_AI_DIAG_PUMP`
- 역할: AI 기반 펌프 진단 결과 시계열
- 주요 컬럼: `PUMP_ID`, `ACQ_DATE`, `DE_RMS_AMP`, `NDE_RMS_AMP`, `DE_AMP`, `NDE_AMP`, `CAVITATION_AMP`, `IMPELLER_AMP`
- 알람 컬럼: `IMPELLER_ALARM`, `CAVITATION_ALARM`, `DE_BPFO_ALARM`, `DE_BPFI_ALARM`, `DE_BSF_ALARM`, `DE_FTF_ALARM`, `NDE_BPFO_ALARM`, `NDE_BPFI_ALARM`, `NDE_BSF_ALARM`, `NDE_FTF_ALARM`, `DE_RMS_ALARM`, `NDE_RMS_ALARM`
- PK 후보: `PUMP_ID + ACQ_DATE`
- 주의: `PUMP_ID` 가 별도 펌프 ID라기보다 `TB_PUMP_INF.MOTOR_ID` 에 매핑되는 구조로 보임
- 신뢰도: 높음

### `TB_DIAG_MOTOR_PUMP`
- 역할: 온도 진단 결과 요약
- 주요 컬럼: `PUMP_SCADA_ID`, `CENTER_ID`, `ACQ_DATE`, `M_DE_BEARING_TEMP`, `M_NDE_BEARING_TEMP`, `P_DE_BEARING_TEMP`, `P_NDE_BEARING_TEMP`, `M_DE_BEARING_TEMP_FAULT`, `M_NDE_BEARING_TEMP_FAULT`, `P_DE_BEARING_TEMP_FAULT`, `P_NDE_BEARING_TEMP_FAULT`
- PK 후보: `PUMP_SCADA_ID + CENTER_ID + ACQ_DATE`
- 신뢰도: 중간

### `TB_DIAG_MOTOR_PUMP_WINDING`
- 역할: 권선 온도 진단 결과
- 주요 컬럼: `PUMP_SCADA_ID`, `CENTER_ID`, `ACQ_DATE`, `WINDING_TEMPR`, `WINDING_TEMPS`, `WINDING_TEMPT`, `WINDING_TEMPR_FAULT`, `WINDING_TEMPS_FAULT`, `WINDING_TEMPT_FAULT`
- PK 후보: `PUMP_SCADA_ID + CENTER_ID + ACQ_DATE`
- 신뢰도: 중간

### `TB_PMS_ALR`
- 역할: 운영 알람 로그
- 주요 컬럼: `ALR_TIME`, `FAC_NAME`, `FAC_INFO`, `DIAG_STUS`, `FLAG`
- 의미 추정: `FLAG` 는 `1=Alert`, `2=TRIP`
- PK 후보: 불명확, 최소 `ALR_TIME` 포함
- 신뢰도: 중간

## 사용 방법
- 신규 API 분석 시 먼저 `TB_PUMP_INF` 를 기준으로 설비 식별자를 찾습니다.
- 시계열 원천 데이터는 `TB_PUMP_SCADA`, `TB_MOTOR`, `TB_RMS`, `TB_TIMEWAVE`, `TB_SPECTRUM`, `TB_FREQ` 순으로 봅니다.
- 진단/알람 화면은 `TB_AI_DIAG_MOTOR`, `TB_AI_DIAG_PUMP`, `TB_DIAG_MOTOR_PUMP`, `TB_DIAG_MOTOR_PUMP_WINDING`, `TB_PMS_ALR` 를 우선 확인하면 됩니다.

## 주의사항 / 한계
- 실제 DDL, 인덱스, 제약조건을 확인하지 못했으므로 PK/FK는 모두 추정입니다.
- 일부 XML 주석과 alias 는 인코딩이 깨져 있으므로 해석 근거로 쓰지 않았습니다.
- `TB_AI_DIAG_PUMP.PUMP_ID` 처럼 이름과 실제 연결 대상이 다를 수 있으므로, 테이블명보다 조인 조건을 우선 신뢰해야 합니다.
