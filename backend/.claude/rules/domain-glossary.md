# 스마트정수장 도메인 용어 사전

레거시 EMS·PMS 산출물(KWS-GS-SC-AN04/AN05/DG01, ems_schema.md, psm_schema.md)을 기반으로 추출한 정수장 핵심 용어 목록.
엔티티·컬럼·필드 명명 전 반드시 참조한다. 신규 용어를 도입할 경우 이 목록에 먼저 추가한다.

---

## 1. 시스템 약어

| 약어 | 풀네임 | 설명 |
|------|--------|------|
| WTP / WPP | Water (Treatment / Purification) Plant | 정수장 |
| EMS | Energy Management System | 에너지 관리 시스템 |
| PMS | Predictive Maintenance System | 예측 유지보수 시스템 |
| SCADA | Supervisory Control And Data Acquisition | 현장 계측 데이터 수집·감시 시스템 |
| HMI | Human Machine Interface | 운전원 조작 화면 |
| EPA | EPANET | 관망 수리 해석 엔진 |
| AI | Artificial Intelligence | AI 기반 최적 제어 |

---

## 2. 시설·설비 용어

| 한국어 용어 | 영문명 | DB 약어 | 단위 | 설명 |
|-------------|--------|---------|------|------|
| 정수장 | Water Purification Plant | WPP | — | 원수를 정수하여 배급수하는 시설 전체 |
| 시설 | Facility | FAC | — | 정수장 내 물리적 구조물 단위 |
| 설비 | Equipment | EQ | — | 시설 내 개별 기계·전기 장치 |
| 구역 | Zone | ZONE | — | 정수장 내 수리·운전 구역 구분 |
| 펌프 | Pump | PUMP | — | 정수·송수·배수 목적 유체 이송 장치 |
| 모터 | Motor | MOTOR | — | 펌프를 구동하는 전동기 |
| 인버터 | Inverter | INVRT | Hz | 모터 회전수(주파수)를 가변 제어하는 장치 |
| 펌프 그룹 | Pump Group | PUMP_GRP | — | 동일 목적·구역의 펌프 묶음 단위 |
| 배수지 | Reservoir | RESV | m | 정수된 물을 저장하는 탱크(TNK_TYP=1) |
| 정수지 | Clearwell | CLRW | m | 처리 완료 후 대기하는 저류조(TNK_TYP=2) |
| 밸브 | Valve | VLV | — | 관로 흐름 제어 장치 |
| 노드 | Node | NODE | — | 관망 해석에서 연결점 |
| 링크 | Link | LINK | — | 관망 해석에서 연결 구간 |
| 채널 | Channel | CHN | — | 진동 센서 측정 채널 (모터/펌프 DE·NDE 구분) |
| DE | Drive End | DE | — | 모터·펌프의 구동 측 베어링 위치 |
| NDE | Non-Drive End | NDE | — | 모터·펌프의 비구동 측 베어링 위치 |

---

## 3. 측정값·물리량 용어

| 한국어 용어 | 영문명 | DB 약어 / 컬럼 패턴 | 단위 | 설명 |
|-------------|--------|---------------------|------|------|
| 유량 순시 | Flow Rate (Inst.) | FRI / FLW | m³/h | 순간 유량 |
| 유량 적산 | Flow (Cumulative) | FRQ | m³ | 누적 유량 |
| 유속 | Flow Velocity | FR | m/s | 관내 유체 속도 |
| 흡입압력 | Suction Pressure | PRI_S | m | 펌프 흡입 측 압력 |
| 토출압력 | Discharge Pressure | PRI_D | m | 펌프 토출 측 압력 |
| 전체압력 (양정) | Total Head | PRI_T | m | 흡입+토출 합산 압력 |
| 관압 | Pipe Pressure | TUBE_PRSR | m | 배관 내 수압 |
| 수위 | Water Level | LEI | m | 저류조·배수지 수위 |
| 수온 | Water Temperature | TEI | °C | 원수·처리수 온도 |
| 전력 순시 | Power (Inst.) | PWI | kW | 순간 전력 소비량 |
| 전력 적산 | Energy | PWQ | kWh | 누적 전력량 |
| 주파수 | Frequency | FREQ / CTI | Hz | 인버터 출력 주파수(=회전수 제어 값) |
| 진동 (RMS) | Vibration RMS | RMS | mm/s | 베어링·모터 진동 실효값 |
| 베어링 온도 | Bearing Temperature | BRG_TEMP | °C | 베어링 과열 진단 기준값 |
| 권선 온도 | Winding Temperature | WINDING_TEMP | °C | 모터 권선(R/S/T) 온도 |
| 정격 양정 | Duty Head | DUTY_H | m | 설계 기준 토출 양정 |
| 정격 유량 | Duty Flow | DUTY_Q | m³/h | 설계 기준 운전 유량 |
| 유압 | Fluid Pressure | FP | m | EPANET 관망 해석 유압값 |

---

## 4. 운전 모드

| 한국어 용어 | 영문명 | 코드 / 값 | 설명 |
|-------------|--------|----------|------|
| AI 자동 운전 | AI Auto Mode | AI_MODE=1 | AI가 펌프 조합·주파수를 자동 결정·제어 |
| 반자동 운전 | Semi-Auto Mode | AI_MODE=2 | 운전원이 조합을 선택하고 주파수는 AI가 결정 |
| 수동 운전 | Manual Mode | AI_MODE=0 | 운전원이 모든 값을 직접 입력 |
| 인터록 | Interlock | — | 안전 조건 미충족 시 기동·변경을 자동 차단하는 보호 로직 |
| 가동 | Run / On | PMB=1 / EQ_ON=1 | 설비 운전 중 상태 |
| 정지 | Stop / Off | PMB=0 / EQ_ON=0 | 설비 정지 상태 |
| 증감운전 | Flow Control | FLOW_CTR=Y | 유량 부족·초과 시 추가 기동 또는 감속 운전 |
| 선행조건 | Pre-condition | REQ_TAG | 기동 전 만족해야 할 안전·운전 조건 |

---

## 5. 알람 4단계

PMS 및 EMS 공통으로 4단계 심각도를 사용한다.

| 단계 | 한국어 | 영문 | 코드 값 | 대응 행동 |
|------|--------|------|---------|----------|
| 0 | 정상 | Normal | 0 | 정상 운전 |
| 1 | 주의 | Caution | 1 | 모니터링 강화 |
| 2 | 경보 | Alert / Warning | 2 | 운전원 확인 필요 |
| 3 | 위험 / TRIP | Danger / Trip | 3 | 즉시 정지 또는 격리 |

> 진단 알람 컬럼명 패턴: `{항목}_ALARM` (예: `UNBALANCE_ALARM`, `DE_RMS_ALARM`)
> 알람 로그 테이블: EMS → `TB_EMS_ALR`, PMS → `TB_PMS_ALR`

---

## 6. 데이터 수집·시계열 패턴

| 한국어 용어 | 영문명 | 약어 | 설명 |
|-------------|--------|------|------|
| 태그 | Tag | TAG | SCADA에서 각 측정점에 붙인 식별자 |
| 원시 데이터 | Raw Data | RAWDATA | SCADA에서 수집된 미가공 시계열 값 |
| 순시값 | Instantaneous Value | I / INS | 특정 시점의 측정값 |
| 적산값 | Cumulative Value | INGRT | 누적 합산값 (전력량, 유량 등) |
| 집계 단위 | Aggregation | — | 1분·15분·1시간·1일·1개월 단위 |
| 품질 코드 | Quality | QUALITY | SCADA 데이터 품질 플래그 (Good/Bad) |
| 결측 | Missing | — | 센서 장애·통신 오류 시 값 누락 상태 |
| 이상치 | Anomaly / Outlier | — | 정상 범위를 벗어난 측정값 |

---

## 7. 에너지·요금 용어

| 한국어 용어 | 영문명 | DB 약어 | 단위 | 설명 |
|-------------|--------|---------|------|------|
| 피크 전력 | Peak Power | PEAK_PWR | kW | 최대 수요 전력 |
| 절감량 | Savings | SAVINGS | kWh / 원 | 기준 대비 에너지·비용 절감량 |
| 경부하 | Light Load | L_ | — | 전력 요금 경부하 시간대 |
| 중간부하 | Medium Load | M_ | — | 전력 요금 중간부하 시간대 |
| 최대부하 | Peak Load (Heavy) | H_ | — | 전력 요금 최대부하 시간대 |
| 기본요금 | Demand Charge | BASE_FEE | 원 | 계약전력 기준 고정 요금 |
| 전력량요금 | Energy Charge | ELCTR_FEE | 원 | 사용 전력량 기준 변동 요금 |

---

## 8. 진단·유지보수 용어 (PMS)

| 한국어 용어 | 영문명 | DB 약어 | 설명 |
|-------------|--------|---------|------|
| 불평형 | Unbalance | UNBALANCE | 회전체 질량 불균형으로 발생하는 진동 |
| 정렬 불량 | Misalignment | MISALIGNMENT | 샤프트·커플링 정렬 오차로 발생하는 진동 |
| 로터 결함 | Rotor Fault | ROTOR | 로터 바·슬롯 손상 관련 진동 |
| 캐비테이션 | Cavitation | CAVITATION | 펌프 흡입 측 기포 발생으로 인한 손상 |
| 임펠러 결함 | Impeller Fault | IMPELLER | 임펠러 마모·파손 관련 진동 |
| BPFO | Ball Pass Frequency Outer | BPFO | 외륜 결함 주파수 |
| BPFI | Ball Pass Frequency Inner | BPFI | 내륜 결함 주파수 |
| BSF | Ball Spin Frequency | BSF | 볼 스핀 결함 주파수 |
| FTF | Fundamental Train Frequency | FTF | 케이지 결함 주파수 |
| TimeWave | Time Waveform | TIMEWAVE | 진동 시간 파형 원본 데이터 |
| Spectrum | Frequency Spectrum | SPECTRUM | 진동 주파수 스펙트럼 데이터 |

---

## 9. DB 컬럼명 명명 패턴

### 접미사

| 패턴 | 의미 | 예시 |
|------|------|------|
| `_id` | Primary Key / 식별자 | `pump_id`, `motor_id` |
| `_nm` | Name (이름) | `pump_nm`, `grp_nm` |
| `_tp` | Type (유형 코드) | `pump_tp`, `alarm_tp` |
| `_yn` | Yes/No 여부 | `use_yn`, `run_yn` |
| `_cd` | Code | `wpp_cd`, `zone_cd` |
| `_idx` | Index (순번) | `pump_idx`, `grp_idx` |
| `_grp` | Group (그룹) | `pump_grp` |
| `_tag` | SCADA 태그명 | `pwi_tag`, `fri_tag` |
| `_val` | Value (측정값) | `flow_val`, `prs_val` |
| `_lmt` | Limit (임계값) | `hi_lmt`, `lo_lmt` |
| `_prdct` | Prediction (예측값) | `pwr_prdct` |
| `_rslt` | Result (결과) | `diag_rslt` |
| `_unit` | Unit (단위) | `pwr_unit` |
| `_pw` | Password (비밀번호) | `user_pw` |
| `_dtm` | Datetime (일시) | `rgstr_dtm`, `updt_dtm` |
| `_dt` | Date (날짜) | `acq_dt` |

### 접두사

| 패턴 | 의미 | 예시 |
|------|------|------|
| `rgstr_` | 등록 | `rgstr_dtm` |
| `updt_` | 수정 | `updt_dtm` |
| `acq_` | 수집 (Acquisition) | `acq_dtm` |
| `anly_` | 분석 | `anly_dtm` |
| `prdct_` | 예측 | `prdct_dtm` |
