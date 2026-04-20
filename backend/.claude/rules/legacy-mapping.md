# 레거시 EMS/PMS → 신규 분류 체계 매핑

스마트정수장 레거시 EMS·PMS DB 스키마를 신규 6축 suffix 체계로 전환할 때의
분류 기준, 판정 지침, 매핑 seed, 안티패턴 해소 가이드를 기술한다.

> **필수 참조 의무**: 신규 엔티티·테이블 설계 또는 마이그레이션 작성 전 반드시 이 문서를 먼저 읽는다.
> PLAN 문서에 도메인 모델·DB 설계 변경이 수반되면 §3 매핑표에 해당 행을 추가 또는 확인한다.
>
> **참고**: 이 문서의 섹션 번호(§1~§7)는 PLAN2 계획안 섹션 번호보다 1씩 앞당겨진다. (PLAN2 §1 목적이 이 문서의 서문으로 통합됨)

---

## 참조 문서 관계

| 문서 | 이 문서와의 관계 |
|------|----------------|
| [`dev/plan.md`](../commands/dev/plan.md) | PLAN 작성 전 "도메인/DB 전문가 사전 검토" 항목에서 참조 |
| [`dev/review.md`](../commands/dev/review.md) | "레거시 동등성" 체크리스트의 기준 문서 (line 45) |
| [`agents/wtp-domain-expert.md`](../agents/wtp-domain-expert.md) | §3 매핑표 미수록 도메인 점검 항목 입력 근거 |
| [`agents/wtp-dba-reviewer.md`](../agents/wtp-dba-reviewer.md) | 파티셔닝·인덱스 설계 검토 시 §3 신규 테이블명 참조 |
| [`domain-glossary.md`](domain-glossary.md) | 도메인 용어·약어의 원천 (전 섹션) |
| [`db-patterns.md`](db-patterns.md) | 파티션(§1)·인덱스(§2)·보존 기간(§6) 정책 참조 원천 |
| 레거시 EMS 스키마 | [`../../legacy/ems/docs/ems_schema.md`](../../legacy/ems/docs/ems_schema.md) |
| 레거시 EMS 분석 | [`../../legacy/ems/docs/ems_schema_analysis.md`](../../legacy/ems/docs/ems_schema_analysis.md) |
| 레거시 PMS 스키마 | [`../../legacy/pms/docs/psm_schema.md`](../../legacy/pms/docs/psm_schema.md) |

---

## 1. 분류 6축 해석 기준

`naming.md` 의 m/l/d/h/c/p suffix 에 정수장 비즈니스 의미 해석을 부여한다.

| suffix | 본질 | 변경 빈도 | 데이터 수명 | 정수장 대표 예 |
|--------|------|-----------|-------------|----------------|
| `_m` 마스터 | **물리 설비·시설·조직 실체** | 드묾 (분기·년) | 영구 (논리 삭제만) | `pump_m`, `zone_m`, `wpp_m` |
| `_p` 명세/정의 | **운전 규칙·임계값·태그 매핑·조합 정의 등 설정값** | 월·분기 튜닝 | 영구 (버전 관리) | `alarm_rule_p`, `pump_comb_p`, `tag_role_p` |
| `_d` 상세 | **마스터의 1:N 구성요소** (채널·항목·상·그룹 등 수직화) | 마스터와 함께 | 마스터와 함께 | `pump_comb_d`, `equipment_channel_d` |
| `_l` 내역 | **조회·집계 리포트용 요약 저장** (일·월·기간 집계) | 스케줄러 생성 | `db-patterns.md §6` | `monthly_peak_l`, `saving_result_l` |
| `_h` 이력 | **시계열·이벤트·감사 로그** | 초~분 단위 생성 | 파티션 DROP | `rawdata_h`, `alarm_h`, `diag_h` |
| `_c` 코드 | **공통 코드·enum 정적 테이블** | 매우 드묾 | 영구 | `alarm_severity_c`, `unit_c` |

### 충돌 시 판정 규칙 3가지

```
규칙 1. 컬럼에 "설정·정의·매핑 파라미터"가 포함되면 _m 이 아니라 _p 로 분리한다.
         (변경 빈도가 다르고 이력 추적 범위도 다르기 때문)

규칙 2. "1 row = 1 시점 이벤트/측정" 이면 _h 로 분류한다.
         원시·집계·파티션 주기 차이는 테이블 이름 접두어(rawdata_1m_h, rawdata_d_h 등)로 구분한다.

규칙 3. 1:N 차원(채널, 항목, 상(R/S/T), 그룹)을 컬럼으로 가로 펼친 경우 _d 로 수직화한다.
         같은 접두어를 갖는 컬럼이 3개 이상이면 분리 대상으로 검토한다.
```

---

## 2. 레거시 suffix ↔ 신규 suffix 판정 지침

고정 1:1 치환표가 아닌 "1차 권고 + 판정 조건" 형식. 반드시 컬럼 구성을 함께 확인한다.

| 레거시 suffix | 1차 권고 | 판정 조건 (이 경우 변경) |
|--------------|----------|--------------------------|
| `_INF` | `_m` 후보 | `*_tag`, `*_thr`, `*_rnk`, `*_typ` 컬럼이 3개 이상이면 → `_p` 로 분리 |
| `_RST` / `_DIAG_*` | `_h` | 일·월 요약 집계이면 → `_l` / 최신 1건만 유효한 상태 스냅샷이면 → `_p` 검토 |
| `_LOG` / `_ALR` | `_h` | 임계값 정의 성격이면 → `_p` / 정의와 이력이 혼재하면 분해 |
| `_TAG` | `_p` 후보 | 단순 코드·enum 이면 → `_c` / 태그 실체(단위·품질 기본값)이면 → `_m` |
| `_VAL` | `_h` | 시뮬레이션 기준값(설정)이면 → `_p` |
| `_GRP` | `_m` 또는 `_d` | 그룹 자체 실체 → `_m` / 마스터의 그룹 구성원 목록 → `_d` |
| `_HOUR / _DAY / _MONTH / _INGRT` | `_h` | 집계 리포트 전용이면 → `_l` |
| 접미 없음 (PMS) | **개별 판정** | 시계열 → `_h` / 진단 임계치 → `_p` / 설비 실체 → `_m` |
| `_OLD / _BACKUP / _날짜 / _지자체코드` | **이관 금지** | 별도 슬러그에서 아카이브 스키마 격리 |

---

## 3. 도메인별 매핑표 seed

핵심 도메인 seed (초기 13행). 전수 매핑은 각 도메인 구현 PR 에서 본 표에 행을 추가하여 확장한다.

| 도메인 | 레거시 테이블 | 레거시 역할 요약 | 신규 테이블(안) | 신규 suffix | 비고 |
|--------|--------------|-----------------|----------------|-------------|------|
| 펌프 실체 | `TB_CTR_PRF_PUMPMST_INF`, `TB_PUMP_INF` | 설비 실체 + SCADA 태그 매핑(20+ 컬럼) + 제어 전략·우선순위 혼재 | `pump_m` + `pump_tag_p` + `pump_oper_p` | m + p | 안티패턴 A 해소 |
| 펌프 조합 | `TB_PUMP_COMBINATION_INF`, `TB_PUMP_COMBINATION` | 조합 규칙(헤더) + 구성 펌프(1:N) | `pump_comb_p` + `pump_comb_d` | p + d | 헤더/상세 수직화 |
| 펌프 조합 계수·전력 | `TB_PUMP_CAL`, `TB_PUMP_COMB_POWER` | 유량·압력 계수 명세 + 조합별 전력 실적 | `pump_comb_cal_p` + `pump_comb_pwr_l` | p + l | 정의 vs 실적 분리 |
| 펌프 인터록·선행조건 | `TB_CTR_PUMP_REQ_OPT` | 펌프 기동 전 만족해야 할 태그 조건·선행조건 규칙 (`REQ_TAG`, `REQ_CTR_TAG`, `REQ_CTR_STOP_TAG`) | `pump_interlock_p` | p | `pump_oper_p` 와 독립 분리. 인터록 규칙 변경은 운전 전략과 다른 승인 흐름 |
| 알람 | `TB_EMS_ALR`, `TB_PMS_ALR`, `TB_AL_SETTING`, `TB_GRAPH_THRESHOLD` | 발생 이력 + 임계값 정의 + 진단 결과 판정 컬럼 혼재 | `alarm_rule_p` + `alarm_h` (진단 판정 컬럼은 `diag_h` 잔류) | p + h | 안티패턴 B 해소. `alarm_h` 파티션 키: `rgstr_dtm` (월 RANGE 필수) |
| 태그 | `TB_WPP_TAG_INF`, `TB_PEAK_TAG_INF`, `TB_HMI_*_TAG`, `TB_WPP_TAG_CODE`, `TB_TAG_UNIT_INFO` | 용도별(수집/피크/HMI) 파편화, 태그 속성 중복 보유 | `tag_m` + `tag_role_p` + `tag_kind_c` + `tag_unit_c` | m + p + c + c | `TB_WPP_TAG_CODE` → `tag_kind_c`, `TB_TAG_UNIT_INFO` → `tag_unit_c`. 안티패턴 C 해소 |
| SCADA 원시 수집 | `TB_RAWDATA`, `TB_RAWDATA_15MIN`, `TB_RAWDATA_HOUR`, `TB_RAWDATA_DAY`, `TB_RAWDATA_MONTH` | 원시 + 집계 주기별 파티션 시계열 | `rawdata_1m_h`, `rawdata_15m_h`, `rawdata_1h_h`, `rawdata_1d_h`, `rawdata_1mo_h` | h | 월 RANGE 파티션 필수 (`db-patterns.md §1`) |
| SCADA 집계 리포트 | `TB_MONTHLY_PEAK` | 월별 최대 피크 요약 (조회 전용) | `monthly_peak_l` | l | 조회 리포트 |
| AI 진단 결과 | `TB_AI_DIAG_MOTOR`, `TB_AI_DIAG_PUMP`, `TB_DIAG_MOTOR_PUMP`, `TB_DIAG_MOTOR_PUMP_WINDING` | AI 진단 시계열 (10+ 알람 판정 컬럼) | `diag_motor_h`, `diag_pump_h` (알람 발생 이벤트는 `alarm_h` 로 파생) | h | `acq_dtm` 파티션 키 (월 RANGE 필수). 알람 판정 컬럼은 h 내 컬럼, 발생 이벤트 → `alarm_h` |
| 진동 원시·채널 | `TB_MOTOR`, `TB_RMS`, `TB_TIMEWAVE`, `TB_SPECTRUM`, `TB_FREQ`, `TB_CHANNEL` | 원시 시계열 + 채널 구성(1:N) 혼재 | `equipment_channel_d` + `vibration_rms_h`, `timewave_h`, `spectrum_h`, `freq_h` | d + h | 채널 구성 수직화 (안티패턴 C). 시계열 4종 모두 `acq_dtm` 파티션 키 (월 RANGE 필수) |
| 요금제 | `TB_RT_RATE_INF`, `TB_RT_MSTR_INF`, `TB_RT_RATE_RST` | 요금제 정의 + 계산 결과 | `rate_plan_p` + `rate_calc_l` | p + l | 정의 vs 결과 분리 |
| 절감 목표·실적 | `TB_BASE_SAVINGS_TARGET`, `TB_RST_SAVINGS_TARGET`, `TB_BASE_SAVING_CHART` | 목표(정의) + 실적(집계) | `saving_target_p` + `saving_result_l` | p + l | |
| 관망(EPA) | `TB_FP_VAL`, `TB_FR_VAL`, `TB_EPA_PUMP_FLOW`, `TB_NODE_TAG`, `TB_LINK_GRP` | 시뮬 결과 + 관망 토폴로지 정의 | `epa_node_m` + `epa_link_m` + `epa_flow_h` | m + h | 네트워크 실체 vs 수리 해석 이력 |

---

## 4. 안티패턴 해소 가이드

레거시 조사에서 반복 발견된 3가지 패턴과 신규 프로젝트 해소 방법.

### A. `_INF` 위장 마스터

**증상**: 한 테이블에 설비 실체 컬럼 + SCADA 태그 매핑 컬럼 + 운전 전략·우선순위 컬럼 공존.
대표 사례: `TB_CTR_PRF_PUMPMST_INF`(`ems_schema.md:215`) — `DUTY_H / DUTY_Q` (실체)
+ `PWI_TAG / PMB_TAG` 20여 개 (태그 매핑) + `PRRT_TYP / PRRT_RNK / USER_RNK` (운전 전략).

**검사 기준**: 테이블 컬럼 중 `*_tag`, `*_thr`, `*_rnk`, `*_typ` 패턴이 3개 이상이면 분리 대상.

**해소 안**:
```
{domain}_m        — pump_id, pump_nm, duty_h, duty_q (물리 실체, 거의 불변)
{domain}_tag_p    — pump_id + 각 SCADA 태그 매핑 컬럼 (현장 튜닝 가능)
{domain}_oper_p   — pump_id + 우선순위, 제어 전략 코드, AI 태그 등 (운전 정책)
```

> 이유: 설비 교체·SCADA 리네이밍·운전 전략 변경은 각자 다른 변경 주기와 감사 이력을 가진다.

---

### B. "알람 3중 의미" 혼재

**증상**: "알람"이라는 단어가 세 층위에 모두 사용됨.
1. 임계값 정의 — `TB_AL_SETTING`, `TB_GRAPH_THRESHOLD`
2. 진단 결과 판정 컬럼 — `TB_AI_DIAG_MOTOR.UNBALANCE_ALARM`, `DE_RMS_ALARM` 등 10+ 컬럼
3. 발생 이벤트 이력 — `TB_EMS_ALR`, `TB_PMS_ALR`, `TB_HMI_ALR_TAG`

**해소 안**:
```
alarm_rule_p   — (equipment_tp, alarm_item_cd, caution_thr, alert_thr, danger_thr,
                   hysteresis): 설비유형·항목별 알람 4단계(1=주의/2=경보/3=위험) 임계값 각각 독립 컬럼.
                   severity_cd 는 alarm_h(발생 이벤트)에서 관리
diag_h         — AI 진단 시계열 + 판정 결과 컬럼(*_alarm) 잔류
alarm_h        — (equipment_id, alarm_item_cd, severity_cd, occurred_at,
                   acknowledged_at, value): 발생 이벤트 로그 (diag_h 에서 파생 삽입)
```

> 알람 정의·진단 결과·발생 이벤트는 화면 권한·조회 패턴·보존 기간이 모두 다르다.

---

### C. "초광역 와이드 테이블"

**증상**: 1:N 차원(채널, 권선 상, 그룹 구분)을 한 행에 가로 컬럼으로 평면화.
대표 사례: `TB_PUMP_INF`(`psm_schema.md:25`) —
`MOTOR_NDE_AMP_TAG / MOTOR_DE_AMP_TAG / R_TEMP_TAG / S_TEMP_TAG / T_TEMP_TAG /
BRG_MOTOR_DE_TEMP_TAG / BRG_MOTOR_NDE_TEMP_TAG` 등 20+ 컬럼.

**검사 기준**: 같은 접두어를 갖는 컬럼 3개 이상 OR 항목·채널별 컬럼 10개 이상.

**해소 안**:
```
equipment_channel_d — (equipment_id, channel_role=DE|NDE|R|S|T,
                        channel_kind=AMP|TEMP, tag_id)
```

> 신규 모델·센서 추가 시 DDL ALTER TABLE 없이 행 삽입만으로 확장 가능.

---

## 5. KWS-GS-*-AN04 추적표 갱신 절차

**원칙**: 레거시 요구사항추적표 xlsx 는 원본 보존, 코드베이스 내 추적은 이 문서 §3 매핑표로 관리.

**의무 사항**:
1. 신규 엔티티·API 를 PLAN 문서에 기재할 때, §3 매핑표에 해당 레거시 테이블이 없으면
   **매핑표 추가 행을 PLAN 문서 내 "도메인 모델" 섹션에 함께 기재** 후 별도 PR 에서 이 문서에 반영
2. `wtp-domain-expert` 가 PLAN 리뷰 시 §3 미수록 레거시 테이블 → 매핑표 추가 요구를 체크
3. 기능 누락 검증은 §6 동등성 체크리스트 참조

---

## 6. 동등성 검증 체크리스트

신규 도메인 엔티티 PR 에서 레거시 대비 기능 누락을 방지하기 위한 항목:

```
[ ] 레거시 PK 보존: 자연키는 신규에서도 UNIQUE 제약으로 유지 또는 surrogate + UNIQUE
[ ] 일시 컬럼 정규화: 레거시 *_TIME / *_DTM / *_DATE → rgstr_dtm / updt_dtm / acq_dtm 중 하나
    (db-patterns.md §1 파티션 키 규칙 준수)
[ ] 알람 4단계: domain-glossary.md §5 의 0~3 값이 severity_cd / *_lvl 컬럼으로 보존
[ ] 보존 기간: db-patterns.md §6 정책이 신규 파티션 계획에 반영됨
    (SCADA 원시 13개월 / 알람 5년 / 제어 2년 / 마스터 영구 등)
[ ] 화면 전용 조회: 레거시 MyBatis 쿼리가 반환하던 컬럼 셋을 신규에서도 제공 가능
[ ] 인터록 선행조건: TB_CTR_PUMP_REQ_OPT 인터록 규칙이 pump_interlock_p 로 보존 (§3 매핑표 참조)
[ ] HMI 제어 로그: TB_HMI_CTR_LOG 제어 이력이 신규 ctrl_log_h 또는 상응 _h 테이블로 대응됨
    (db-patterns.md §6 제어 로그 2년 보존)
```

---

## 7. 매핑표 갱신 룰

1. 신규 엔티티/테이블 PR 은 §3 매핑표에 해당 행이 **존재하거나 추가** 되어야 merge 가능
   (`dev/review.md` "레거시 동등성" 체크리스트 항목으로 반영)
2. 매핑표 행 수정·추가는 단일 섹션 변경 PR 로 독립 처리 가능
3. 백업·사이트 스냅샷 테이블(`_OLD / _BACKUP / _날짜` 등)은 이 문서에 기재하지 않으며
   별도 슬러그에서 아카이브 스키마 정책으로 처리
