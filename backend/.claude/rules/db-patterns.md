# DB 운영 패턴

스마트정수장 PostgreSQL 데이터베이스 설계·운영 기준. 시계열 파티셔닝, 인덱스 원칙,
스키마 무중단 변경, 트랜잭션 격리, 슬로우 쿼리 분석, 데이터 보존 정책을 기술한다.

---

## 1. 시계열 파티셔닝

### 기준
- SCADA 수집 데이터, 진단 결과, 알람 이력 등 시계열 테이블은 **월 단위 RANGE 파티셔닝**을 적용한다.
- 파티션 키: `acq_dtm` (수집 일시) 또는 `rgstr_dtm` (등록 일시)

### 파티션 생성 패턴 (PostgreSQL)

```sql
-- 파티션 테이블 생성
CREATE TABLE rawdata_m (
    acq_dtm     TIMESTAMP NOT NULL,
    tag_nm      VARCHAR(50) NOT NULL,
    tag_val     NUMERIC(15,4),
    quality     SMALLINT
) PARTITION BY RANGE (acq_dtm);

-- 월별 파티션 (최소 6개월 선행 생성)
CREATE TABLE rawdata_m_202601 PARTITION OF rawdata_m
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE rawdata_m_202602 PARTITION OF rawdata_m
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

### 운영 원칙
- 파티션은 **운영 기간보다 최소 6개월 앞서** 생성해야 한다. 파티션이 없으면 INSERT 실패.
- 오래된 파티션 삭제: `DROP TABLE rawdata_m_202001;` — 즉시 완료, VACUUM 불필요.
- 파티션 범위에 걸친 쿼리는 파티션 프루닝이 작동하도록 `acq_dtm` 조건을 반드시 포함한다.

---

## 2. 인덱스 원칙

### 인덱스 종류별 사용 기준

| 인덱스 | 사용 시점 | 예시 컬럼 |
|--------|----------|----------|
| B-Tree (기본) | 등가·범위 조건, 정렬이 필요한 컬럼 | `pump_id`, `alarm_tp`, `rgstr_dtm` |
| 복합 인덱스 | 두 개 이상 컬럼이 동시에 조건에 사용될 때 | `(pump_id, acq_dtm)` |
| BRIN | 삽입 순서와 물리 순서가 일치하는 대용량 시계열 | `acq_dtm` (시계열 파티션) |
| GIN | JSONB 필드 전체 키 검색 | `tag_meta`, `diag_rslt` |

### 복합 인덱스 컬럼 순서 규칙
1. **등가 조건(=) 컬럼 먼저**, 범위 조건(BETWEEN, >=, <=) 컬럼 뒤에 배치
2. **카디널리티 높은 컬럼 먼저** (pump_id > alarm_tp)
3. 정렬 컬럼은 마지막에 배치

```sql
-- 올바른 예: pump_id(등가) → acq_dtm(범위·정렬)
CREATE INDEX idx_rawdata_pump_time ON rawdata_m (pump_id, acq_dtm DESC);

-- 잘못된 예: 범위 조건 컬럼이 앞에 오면 나머지 컬럼 인덱스 미사용
CREATE INDEX idx_bad ON rawdata_m (acq_dtm, pump_id);
```

### BRIN 적용 기준
- 1분 이하 간격으로 삽입되는 시계열 파티션에 적용
- B-Tree 대비 크기 1/100, 쓰기 오버헤드 최소화

```sql
CREATE INDEX idx_rawdata_brin ON rawdata_m USING BRIN (acq_dtm);
```

### 인덱스 생성 원칙
- 무중단 생성: `CREATE INDEX CONCURRENTLY` 사용
- 주 서비스 시간 외(00:00~06:00) 실행 권장
- 불필요한 인덱스는 즉시 삭제 (`DROP INDEX CONCURRENTLY`)

---

## 3. 스키마 무중단 변경 원칙

### NOT NULL 컬럼 추가 3단계

기존 테이블에 NOT NULL 컬럼을 추가할 때는 **3단계 마이그레이션**을 반드시 따른다.

```sql
-- 1단계: NULL 허용으로 컬럼 추가 (즉시 완료, 락 없음)
ALTER TABLE pump_m ADD COLUMN alarm_lvl SMALLINT;

-- 2단계: 기존 행 백필 (배치 단위로 분할하여 실행)
UPDATE pump_m SET alarm_lvl = 0 WHERE alarm_lvl IS NULL AND id BETWEEN 1 AND 10000;
-- ... 반복

-- 3단계: NOT NULL 제약 추가 (PostgreSQL 12+: CHECK 제약으로 검증 후 NOT NULL 전환)
ALTER TABLE pump_m ALTER COLUMN alarm_lvl SET NOT NULL;
```

> **⚠️ 절대 금지**: `ALTER TABLE ... ADD COLUMN col NOT NULL DEFAULT val` — 대용량 테이블에서 전체 락 발생.

### 컬럼 이름 변경
```sql
-- 무중단: 새 이름으로 컬럼 추가 → 양방향 동기 → 구 컬럼 제거
ALTER TABLE pump_m ADD COLUMN new_col_nm VARCHAR(100);
-- 애플리케이션 배포 후 구 컬럼 제거
ALTER TABLE pump_m DROP COLUMN old_col_nm;
```

### 인덱스 추가·변경
```sql
-- 항상 CONCURRENTLY 사용 (락 없이 생성)
CREATE INDEX CONCURRENTLY idx_pump_m_grp ON pump_m (pump_grp_id);
```

---

## 4. 트랜잭션 격리 기준

### 기본 정책
- Spring의 기본 격리 수준인 **READ_COMMITTED** 사용 (PostgreSQL 기본값과 일치).
- 집계·통계 쿼리처럼 팬텀 읽기가 문제 될 경우에만 **REPEATABLE_READ** 로컬 설정.

```java
// 일반 서비스: ReadOnly + READ_COMMITTED (기본)
@Transactional(readOnly = true)
public List<RawDataDto> findRawData(RawDataSearchDto dto) { ... }

// 집계 서비스: REPEATABLE_READ 필요 시
@Transactional(isolation = Isolation.REPEATABLE_READ, readOnly = true)
public EnergyStatDto calcEnergyStat(LocalDate from, LocalDate to) { ... }
```

### 주의 사항
- 시계열 대용량 조회는 **페이지네이션** 또는 **커서 기반** 분할 조회를 사용한다.
- SERIALIZABLE은 성능 저하가 크므로 배치 정산 등 명확한 필요성이 없으면 사용하지 않는다.
- 장시간 트랜잭션은 `VACUUM` 지연 및 테이블 팽창을 유발하므로 최소 범위로 유지한다.

---

## 5. p6spy 슬로우 쿼리 활용

### 슬로우 쿼리 임계값
- `p6spy` 설정(`common/src/main/resources-env/*/spy.properties`)에서 `executionThreshold` 값(기본 500ms) 이상 걸리는 쿼리는 로그에 기록된다.

### 분석 절차
1. 로컬·스테이징 환경에서 슬로우 쿼리 로그 확인
2. `EXPLAIN (ANALYZE, BUFFERS)` 실행하여 실행 계획 확인
3. Seq Scan → 인덱스 추가 검토 / Nested Loop 과다 → 조인 조건 재검토
4. 수정 후 재실행하여 비교

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM rawdata_m
WHERE pump_id = 'P-001' AND acq_dtm BETWEEN '2026-01-01' AND '2026-02-01';
```

### N+1 방지 원칙
- 연관 엔티티 조회는 `JOIN FETCH` 또는 `@EntityGraph` 사용
- 루프 내 개별 조회 금지: 배치 조회(`IN` 절) 또는 `@BatchSize`로 대체

---

## 6. 데이터 보존 기간 정책

| 데이터 종류 | 보존 기간 | 삭제 방식 |
|-------------|----------|----------|
| SCADA 원시 데이터 (1분) | 13개월 (롤링) | 파티션 DROP |
| SCADA 15분 집계 | 3년 | 파티션 DROP |
| SCADA 시간·일·월 집계 | 10년 | 파티션 DROP |
| 진단 결과 (모터·펌프) | 5년 | 파티션 DROP 또는 DELETE |
| 알람 이력 | 5년 | 파티션 DROP 또는 DELETE |
| 제어 로그 | 2년 | DELETE + VACUUM |
| 마스터 데이터 | 영구 보존 | 삭제 불가 (논리 삭제만 허용) |

> 파티션 DROP은 스케줄러(`SchedulerService`)에서 자정에 자동 실행한다.
> 삭제 정책 변경 시 PLAN 문서의 `## DB 설계 변경` 섹션에 반드시 명시한다.
