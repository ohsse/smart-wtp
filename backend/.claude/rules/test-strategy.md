# 테스트 전략

스마트정수장 백엔드의 3계층 테스트 분리 원칙과 도메인 시나리오 기반 테스트 가이드.

---

## 참조 문서 관계

| 문서 | 이 문서와의 관계 |
|------|----------------|
| [`db-patterns.md §1`](db-patterns.md) | 시계열 파티션 생성 규칙 — 픽스처 구성에 필수 (§4) |
| [`domain-glossary.md §4·§5`](domain-glossary.md) | 운전 모드·알람 4단계 — 도메인 시나리오 기준 (§5) |
| `api/src/test/java/` | 현재 단위 테스트 스타일 참고 (§1) |

---

## 테스트 3계층 원칙

```
단위 테스트 (Unit)       ← 현재 표준, 빠름, Mock 허용
통합 테스트 (Integration) ← DB·컨텍스트 슬라이스, TestContainers 필요 시 추가
E2E 테스트               ← 전체 스택, 최소화
```

---

## 1. 단위 테스트

현재 프로젝트의 표준 스타일. 외부 의존성은 Mockito로 격리한다.

### 기본 구성

```java
@ExtendWith(MockitoExtension.class)
class PumpServiceTest {

    @Mock PumpRepository pumpRepository;
    @InjectMocks PumpService pumpService;

    @Test
    void 펌프_조합이_없으면_예외를_던진다() {
        given(pumpRepository.findById(any())).willReturn(Optional.empty());

        assertThatThrownBy(() -> pumpService.findPump("P-001"))
            .isInstanceOf(RestApiException.class);
    }
}
```

### 적용 대상

| 대상 | 핵심 검증 항목 |
|------|--------------|
| Service 로직 | 비즈니스 규칙, 예외 발생 조건, 상태 전이 |
| 도메인 엔티티 | `create()`·`changeInfo()` 정적 팩토리 및 변경 메서드 |
| 유효성 검사 컴포넌트 | Validator, 인터록 검사 로직 |
| 값 계산 로직 | 절감량 계산, 알람 임계값 비교 |

### 의존성 (현재 표준)

```groovy
testImplementation 'org.junit.jupiter:junit-jupiter'
testImplementation 'org.mockito:mockito-core:5.20.0'
testImplementation 'org.assertj:assertj-core:3.27.4'
```

---

## 2. 통합 테스트

DB·Spring 컨텍스트를 실제로 올려 Repository와 쿼리를 검증한다.

### 슬라이스별 어노테이션

| 슬라이스 | 어노테이션 | 용도 |
|---------|-----------|------|
| JPA Repository | `@DataJpaTest` | 엔티티 CRUD, Querydsl 조회 |
| Web/Controller | `@WebMvcTest` | 요청 파라미터 바인딩, 응답 형식 |
| 전체 컨텍스트 | `@SpringBootTest` | 서비스 통합, 인증 필터 |

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)  // 실제 DB 사용 시
class PumpRepositoryTest {

    @Autowired PumpRepository pumpRepository;

    @Test
    void 유량_범위로_펌프를_조회한다() { ... }
}
```

### TestContainers 도입 기준

실제 PostgreSQL이 필요한 경우(파티션·JSONB·플 함수 검증)에만 TestContainers를 도입한다.

```groovy
// build.gradle — 도입 시 추가
testImplementation 'org.testcontainers:postgresql:1.20.4'
testImplementation 'org.testcontainers:junit-jupiter:1.20.4'
```

```java
@Testcontainers
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class RawDataRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void registerProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
    }
}
```

> TestContainers 없이 H2로 대체 가능한 경우 H2를 우선 사용한다. 시계열 파티션·BRIN 인덱스처럼 PostgreSQL 전용 DDL이 필요할 때만 TestContainers를 사용한다.

---

## 3. E2E 테스트

전체 Spring 컨텍스트 + 실제 DB로 API 골든 패스를 검증한다. 분량을 최소화하고 핵심 흐름만 포함한다.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
class PumpControlApiE2ETest {

    @Container
    static PostgreSQLContainer<?> postgres = ...;

    @Autowired TestRestTemplate restTemplate;

    @Test
    void 펌프_제어_명령_API_골든패스() {
        // given: 초기 데이터 적재
        // when: POST /api/pumps/{id}/control
        // then: 200 OK + 제어 이벤트 기록 확인
    }
}
```

E2E 테스트는 CI에서 별도 태스크(`./gradlew.bat :api:test -Pe2e`)로 분리하여 실행 시간을 관리한다.

---

## 4. 시계열 픽스처 전략

### 파티션 생성 규칙

`db-patterns.md §1`의 월 RANGE 파티션 규칙을 테스트 픽스처에도 그대로 적용한다.
파티션 없이 INSERT 시 실패하므로 픽스처 SQL에서 파티션을 먼저 생성해야 한다.

```sql
-- 테스트용 파티션 생성 (2개월치만 생성)
CREATE TABLE IF NOT EXISTS rawdata_1m_h_202601
    PARTITION OF rawdata_1m_h
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE IF NOT EXISTS rawdata_1m_h_202602
    PARTITION OF rawdata_1m_h
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

### 데이터 분량 기준

| 목적 | 파티션 수 | 행 수 |
|------|----------|------|
| 단순 CRUD 검증 | 1개 | 10~50행 |
| 파티션 프루닝 검증 | 2~3개 | 각 50~100행 |
| 성능 기준선 | 1개 | 최대 1,000행 |

> 테스트 DB에 수만 건을 넣으면 CI 시간이 급증한다. 최소 데이터로 동작을 검증한다.

### 픽스처 빌더 패턴

```java
public class RawDataFixture {
    public static RawData create(String pumpId, LocalDateTime acqDtm, double tagVal) {
        return RawData.builder()
            .pumpId(pumpId)
            .acqDtm(acqDtm)
            .tagVal(tagVal)
            .quality(QualityCode.GOOD)
            .build();
    }

    public static List<RawData> createRange(
            String pumpId, LocalDateTime from, int minutes, int count) {
        return IntStream.range(0, count)
            .mapToObj(i -> create(pumpId, from.plusMinutes((long) i * minutes), 100.0))
            .toList();
    }
}
```

---

## 5. 도메인 시나리오 테스트

정수장 핵심 비즈니스 규칙을 시나리오 단위로 검증한다.

### 5-1. 알람 4단계 전이

`domain-glossary.md §5` 기준 0 → 1(주의) → 2(경보) → 3(위험/TRIP) 전이를 검증.

```java
@Test
void 진동값이_주의_임계값을_초과하면_알람_1단계가_발생한다() {
    // given: caution_thr = 5.0 mm/s 설정
    AlarmRule rule = AlarmRuleFixture.create(5.0, 8.0, 12.0);

    // when: RMS 6.5 mm/s 입력
    AlarmResult result = alarmEvaluator.evaluate(rule, 6.5);

    // then: severity = 1 (주의)
    assertThat(result.getSeverityCd()).isEqualTo(1);
}

@Test
void 위험_임계값_초과_시_즉시_TRIP_단계가_된다() { ... }

@Test
void 복귀_조건을_만족하면_정상_단계로_내려간다() { ... }
```

### 5-2. 인터록 조건 미충족 시 기동 차단

```java
@Test
void 흡입압력이_최저값_미만이면_기동_명령이_차단된다() {
    // given: 인터록 규칙 — 흡입압력 >= 0.3m 필요
    // when: 현재 흡입압력 = 0.1m 상태에서 기동 명령
    // then: RestApiException (INTERLOCK_VIOLATION)
}

@Test
void 모든_선행조건을_만족하면_기동_명령이_허용된다() { ... }
```

### 5-3. 운전 모드 전환

`domain-glossary.md §4` 기준 `AI_MODE=0(수동)`, `AI_MODE=1(AI자동)`, `AI_MODE=2(반자동)` 전환 검증.

```java
@Test
void AI자동_모드에서는_수동_주파수_입력이_거부된다() {
    // given: AI_MODE = 1 (AI 자동)
    // when: 운전원이 직접 주파수 입력
    // then: RestApiException (MANUAL_INPUT_DENIED_IN_AUTO_MODE)
}

@Test
void 수동_모드_전환_시_진행중인_AI_제어_명령이_취소된다() { ... }

@Test
void 반자동_모드에서는_펌프_조합_선택만_허용된다() { ... }
```

---

## 6. 테스트 디렉토리·네이밍

### 현재 구조 (유지)

```
{모듈}/src/test/java/
└── com/mo/smartwtp/
    └── {도메인}/
        └── {대상클래스}Test.java
```

### 통합 테스트 도입 시 소스셋 분리

TestContainers가 필요한 통합 테스트가 10개를 초과하면 별도 소스셋으로 분리하여 CI 단계를 구분한다.

```groovy
// build.gradle — 필요 시 추가
sourceSets {
    integrationTest {
        java.srcDir 'src/integration-test/java'
        resources.srcDir 'src/integration-test/resources'
        compileClasspath += sourceSets.main.output + configurations.testRuntimeClasspath
        runtimeClasspath += output + compileClasspath
    }
}

task integrationTest(type: Test) {
    testClassesDirs = sourceSets.integrationTest.output.classesDirs
    classpath = sourceSets.integrationTest.runtimeClasspath
    useJUnitPlatform()
}
```

### 테스트 클래스 네이밍

| 분류 | 패턴 | 예시 |
|------|------|------|
| 단위 테스트 | `{대상클래스}Test` | `PumpServiceTest` |
| Repository 통합 | `{대상클래스}RepositoryTest` | `PumpRepositoryTest` |
| Controller 슬라이스 | `{대상클래스}ControllerTest` | `PumpControllerTest` |
| 도메인 시나리오 | `{도메인}{시나리오}ScenarioTest` | `AlarmEscalationScenarioTest` |
| E2E | `{기능}E2ETest` | `PumpControlApiE2ETest` |
