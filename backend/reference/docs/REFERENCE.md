# 프로젝트 레퍼런스 가이드

> **프로젝트명**: simulation (온라인 상수관망 의사결정 시뮬레이션)
> **개발사**: HSCMT
> **작성일**: 2026-04-08

---

## 목차

1. [기술 스택](#1-기술-스택)
2. [멀티모듈 구조](#2-멀티모듈-구조)
3. [패키지 구조 컨벤션](#3-패키지-구조-컨벤션)
4. [코드 컨벤션](#4-코드-컨벤션)
5. [주요 아키텍처 패턴](#5-주요-아키텍처-패턴)
6. [설정 관리](#6-설정-관리)
7. [네이밍 규칙](#7-네이밍-규칙)
8. [빌드 설정](#8-빌드-설정)

---

## 1. 기술 스택

| 분류 | 기술 |
|---|---|
| **언어** | Java 21 |
| **프레임워크** | Spring Boot 3.4.4 |
| **빌드 도구** | Gradle (Groovy DSL) + Spring Dependency Management 1.1.7 |
| **ORM** | Spring Data JPA, Hibernate 6, QueryDSL 5.0.0 (Jakarta) |
| **MyBatis** | mybatis-spring-boot-starter 3.0.3 (batch 모듈 전용) |
| **주 데이터베이스** | PostgreSQL |
| **보조 데이터베이스** | Tibero 6 (waternet 시스템 연동, Oracle 호환) |
| **커넥션 풀** | HikariCP |
| **SQL 로깅** | P6Spy |
| **캐시** | Spring Cache + Caffeine |
| **배치** | Spring Batch + Quartz Scheduler (JDBC 잡 스토어) |
| **API 문서** | SpringDoc OpenAPI (Swagger UI) 2.8.0 |
| **인증/JWT** | jjwt 0.12.6, Auth0 java-jwt 4.4.0 |
| **GIS/공간정보** | GeoTools 33.0, JTS 1.19.0, Proj4J, jts2geojson |
| **파일 처리** | Apache POI 5.3.0 (Excel), OpenCSV 5.9 |
| **외부 프로세스** | zt-exec 1.12 (Python/Anaconda 실행) |
| **시스템 모니터링** | OSHI 6.4.0, Spring Boot Actuator |
| **서비스 간 통신** | Spring WebFlux (WebClient) |
| **기타** | Lombok, UUID Creator (v7) |

---

## 2. 멀티모듈 구조

```
simulation/
  common/    -- 공유 라이브러리 (엔티티, DTO, 이벤트, 유틸리티)
  api/       -- REST API 서버 (port: 8080 / prod: 60083)
  batch/     -- 배치 처리 서버 (port: 8081 / prod: 60084)
  doc/ddl/   -- PostgreSQL DDL 스크립트 (24개 테이블 정의)
  libs/      -- 벤더 JAR (tibero6-jdbc.jar, GeoTools 의존성)
```

### common 모듈
`java-library` 플러그인 사용. `api`, `batch` 모듈이 의존하는 공유 라이브러리.

주요 내용:
- **도메인 엔티티** (22개): User, Library, Dataset, Program, Dashboard, Layer, VirtualEnvironment, Group 등
- **DTO / 이벤트 / 열거형 / 예외 / 유틸리티**
- **공통 인프라**: JWT, 캐시, 비동기 설정, P6Spy 포매터, CORS 필터

### api 모듈
Spring Boot Web 애플리케이션. 15개 Controller, 도메인별 Service/Repository 구성.

주요 도메인: `dashboard`, `dataset`, `group`, `layer`, `library`, `program`, `user`, `venv` (simulation 영역) + `lws`, `tag`, `wro` (waternet 영역)

### batch 모듈
Spring Boot + Spring Batch + Quartz 조합. JPA와 MyBatis를 함께 사용.

주요 도메인: `collect`, `dataset`, `layer`, `partition`, `program`, `schedule`, `tag`

---

## 3. 패키지 구조 컨벤션

**도메인 기반(feature-based) 패키지 구성**을 채택한다. 기술 계층(controller/service/repository)이 최상위가 아닌, 비즈니스 도메인이 최상위 패키지가 된다.

```
com.hscmt
  common/                     -- 공통 인프라 (양 모듈 공유)
    aop/                      -- 역할 검사 AOP
    cache/                    -- Caffeine 캐시 설정 & 상수
    config/                   -- AsyncConfig, JacksonConfig
    controller/               -- CommonController (베이스 컨트롤러)
    domain/                   -- BaseEntity, DomainEventEntity
    dto/                      -- BaseDto, FileInfoDto, FromToSearchDto
    enumeration/              -- 전체 열거형 (DatasetType, AuthCd, YesOrNo 등)
    event/                    -- AbstractDomainEventPublisher, DomainEventHolder
    exception/                -- RestApiException, ErrorCode 인터페이스, 에러코드 열거형
    jwt/                      -- JwtToken, TokenState
    p6spy/                    -- SQL 로깅 포매터
    props/                    -- DataSourceProps, JpaProps
    response/                 -- ResponseObject, CommandResult, SseEvent
    swagger/                  -- SwaggerConfig
    util/                     -- 유틸리티 클래스들
    web/                      -- CorsFilter
  simulation/
    {도메인명}/               -- 도메인별 패키지 (아래 구조 반복)
      controller/
      service/
      repository/
        impl/                 -- QueryDSL 커스텀 구현체
    common/                   -- 시뮬레이션 전용 공통 (JPA 설정, JWT, Batch 클라이언트, 커스텀 어노테이션)
  waternet/                   -- 보조 데이터소스 도메인
    {도메인명}/
```

---

## 4. 코드 컨벤션

### 4.1 Entity 패턴

```java
@Entity
@Table(name = "ds_m")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)   // JPA 요건, 외부 직접 생성 차단
@AllArgsConstructor(access = AccessLevel.PRIVATE)    // 모든 필드 생성자 제한
public class Dataset extends DomainEventEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "ds_id")
    private String dsId;

    @Column(name = "ds_nm")
    private String dsNm;

    // 생성 팩토리 메서드 (UpsertDto 기반)
    public static Dataset create(DatasetUpsertDto dto) {
        return new Dataset(null, dto.getDsNm(), ...);
    }

    // 상태 변경 메서드 (setter 대신 명시적 메서드)
    public void changeInfo(DatasetUpsertDto dto) {
        if (dto.getDsNm() != null) this.dsNm = dto.getDsNm();
        // null-check 가드 후 필드 변경
    }
}
```

**핵심 규칙**:
- `@Getter`만 사용, `@Setter` 사용 금지
- 상태 변경은 `changeXxx(UpsertDto)` 메서드로
- PK는 `@GeneratedValue(strategy = GenerationType.UUID)`
- `BaseEntity` 또는 `DomainEventEntity`를 상속

### 4.2 DTO 패턴

```java
// 응답/조회 DTO
@Data
@NoArgsConstructor
@Schema(description = "데이터셋 DTO")
public class DatasetDto extends BaseDto {
    @Schema(description = "데이터셋 ID")
    private String dsId;

    // QueryDSL 프로젝션 필드 정의
    public static List<Expression<?>> projectionFields(QDataset q) {
        return List.of(q.dsId, q.dsNm, ...);
    }
}

// 생성/수정 요청 DTO
@Data
@NoArgsConstructor
public class DatasetUpsertDto {
    private String dsNm;
    // ...
}

// 검색 조건 DTO
@Data
@NoArgsConstructor
public class DatasetSearchDto extends FromToSearchDto {
    private String dsNm;
    // ...
}
```

**네이밍 규칙**:
- `XxxDto` — 응답/조회
- `XxxUpsertDto` — 생성/수정 요청
- `XxxSearchDto` — 검색 조건

**다형성 JSON**: 상속 계층이 있는 DTO는 `@JsonTypeInfo` + `@JsonSubTypes` 사용

```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "dsTypeCd")
@JsonSubTypes({
    @JsonSubTypes.Type(value = MeasureDatasetDto.class, name = "MEASURE"),
    @JsonSubTypes.Type(value = PipeNetworkDatasetDto.class, name = "PIPE_NETWORK")
})
public abstract class DatasetDto extends BaseDto { ... }
```

### 4.3 Repository 패턴 (3계층)

```java
// 1. Spring Data JPA 인터페이스 (커스텀 리포지토리 다중 상속)
public interface DatasetRepository
    extends JpaRepository<Dataset, String>, DatasetCustomRepository { }

// 2. 커스텀 쿼리 인터페이스
public interface DatasetCustomRepository {
    List<DatasetDto> findList(DatasetSearchDto searchDto);
}

// 3. QueryDSL 구현체
@Repository
@RequiredArgsConstructor
public class DatasetCustomRepositoryImpl implements DatasetCustomRepository {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<DatasetDto> findList(DatasetSearchDto searchDto) {
        return queryFactory
            .select(QProjectionUtil.toQBean(DatasetDto.class,
                DatasetDto.projectionFields(QDataset.dataset)))
            .from(QDataset.dataset)
            .where(/* 동적 조건 */)
            .fetch();
    }
}
```

### 4.4 Service 패턴

```java
@Service
@RequiredArgsConstructor
@Slf4j
@SimulationTx(readOnly = true)   // 클래스 레벨: 기본 읽기 전용 트랜잭션
public class DatasetService {

    private final DatasetRepository datasetRepository;
    private final DatasetEventPublisher datasetEventPublisher;

    public DatasetDto getDataset(String dsId) {
        // 읽기 트랜잭션 (클래스 레벨 적용)
    }

    @SimulationTx   // 메서드 레벨: 쓰기 트랜잭션으로 오버라이드
    public void createDataset(DatasetUpsertDto dto) {
        Dataset dataset = Dataset.create(dto);
        datasetEventPublisher.saveAndPublish(dataset, new DatasetUpsertedEvent(...));
    }
}
```

**핵심 규칙**:
- 서비스 인터페이스 없음, 구체 클래스만 사용
- `@RequiredArgsConstructor`로 생성자 주입
- 클래스 레벨 `@SimulationTx(readOnly = true)`, 쓰기 메서드에 `@SimulationTx` 오버라이드
- 이벤트 발행은 `EventPublisher` 컴포넌트에 위임
- 유효성 검사는 `Validator` 컴포넌트로 분리

### 4.5 Controller 패턴

```java
@RestController
@RequiredArgsConstructor
@RequestMapping("/simulation/dataset")
@Tag(name = "03. 데이터셋 관리")
public class DatasetController extends CommonController {

    private final DatasetService datasetService;

    @GetMapping("/{dsId}")
    @Operation(summary = "데이터셋 단건 조회")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "성공")
    })
    public ResponseEntity<ResponseObject<DatasetDto>> getDataset(
            @PathVariable String dsId) {
        return getResponseEntity(datasetService.getDataset(dsId));
    }

    @PostMapping
    @UserRoleCheckRequired          // 역할 검사 (NORMAL 권한 차단)
    @Operation(summary = "데이터셋 등록")
    public ResponseEntity<ResponseObject<Void>> createDataset(
            @RequestBody DatasetUpsertDto dto) {
        datasetService.createDataset(dto);
        return getResponseEntity();
    }
}
```

**핵심 규칙**:
- `CommonController` 상속 필수 (응답 래핑 헬퍼 제공)
- 반환 타입은 항상 `ResponseEntity<ResponseObject<T>>`
- Swagger `@Tag`, `@Operation`, `@ApiResponses` 필수 작성
- JWT 인증 불필요 엔드포인트: `@UncheckedJwtToken` 적용
- 쓰기 엔드포인트: `@UserRoleCheckRequired` 적용

---

## 5. 주요 아키텍처 패턴

### 5.1 다중 데이터소스 (Multi-DataSource)

두 개의 독립적인 데이터소스를 운용한다. 

| 항목 | simulation (주) | waternet (보조) |
|---|---|---|
| DB | PostgreSQL | Tibero 6 (Oracle 호환) |
| 역할 | 애플리케이션 주 데이터 | 외부 waternet 시스템 연동 |
| DDL 전략 | update (local/dev) / none (prod) | none (항상) |
| JPA 설정 | `SimulationJpaConfig` | `WaternetJpaConfig` |
| 스캔 패키지 | `com.hscmt.simulation` | `com.hscmt.waternet` |

각 데이터소스는 독립적인 `EntityManagerFactory`, `TransactionManager`, `DataSource`를 가진다. `DataSourceAutoConfiguration`은 비활성화(`@SpringBootApplication` exclude) 후 수동 설정.

### 5.2 커스텀 트랜잭션 어노테이션

`@Transactional`을 직접 사용하지 않고 커스텀 메타 어노테이션을 사용한다.

```java
// 정의 (api/batch 모듈 각각)
@Transactional(value = "simulationTransactionManager")
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface SimulationTx {
    boolean readOnly() default false;
    Propagation propagation() default Propagation.REQUIRED;
}

// 사용
@SimulationTx(readOnly = true)   // 읽기
@SimulationTx                    // 쓰기 (readOnly = false 기본값)
@WaternetTx(readOnly = true)     // waternet DB 읽기
```

### 5.3 도메인 이벤트 패턴

엔티티 변경 후 후속 작업(캐시 만료, 파일 정리, 배치 트리거)을 이벤트로 처리한다.

```
Entity (DomainEventEntity)
  └─ changeInfo() 시 이벤트 등록 (addDomainEvent)
       ↓
EventPublisher (AbstractDomainEventPublisher 상속)
  └─ saveAndPublish() / deleteAndPublish()
  └─ 저장 + ApplicationEventPublisher.publishEvent()
       ↓
EventHandler (@TransactionalEventListener(AFTER_COMMIT) + @Async)
  └─ 트랜잭션 커밋 후 비동기 실행
  └─ 캐시 만료, 파일 삭제, 배치 Job 트리거 등
```

**이벤트 정의**: Java `record` 사용
```java
public record DatasetUpsertedEvent(String dsId, String dsNm) {}
public record DatasetDeletedEvent(String dsId) {}
```

### 5.4 AOP 기반 인증/인가

Spring Security 미사용. AOP로 대체.

```
요청
  ↓
CheckJwtToken (Order 1) -- Authorization 헤더에서 JWT 검증
  ├─ VALID → 통과
  ├─ EXPIRED → RestApiException(JwtTokenErrorCode.EXPIRED)
  ├─ INVALID → RestApiException(JwtTokenErrorCode.INVALID)
  └─ @UncheckedJwtToken 어노테이션 → 검사 생략
  ↓
CheckUserRole (Order 2) -- @UserRoleCheckRequired 어노테이션 존재 시
  ├─ JWT 클레임에서 역할 추출
  └─ NORMAL 권한 → RestApiException(UserErrorCode.ENABLE_USER_AUTH)
```

**CORS**: `OncePerRequestFilter` 기반 커스텀 `CorsFilter` (`Access-Control-Allow-Origin: *`)

### 5.5 통합 응답 래퍼 (ResponseObject)

모든 API 응답은 동일한 형태를 가진다.

```json
// 성공
{ "code": "SUCCESS", "data": { ... } }

// 실패
{ "code": "USER_NOT_FOUND", "data": null }
```

```java
public class ResponseObject<T> {
    private String code;   // "SUCCESS" 또는 ErrorCode.name()
    private T data;
}
```

`CommonController`의 헬퍼 메서드로 생성:
```java
return getResponseEntity(data);   // 데이터 있는 응답
return getResponseEntity();       // 데이터 없는 성공 응답
```

### 5.6 글로벌 예외 처리

```java
// ErrorCode: 마커 인터페이스
public interface ErrorCode {
    String name();
}

// 도메인별 구현 (열거형)
public enum UserErrorCode implements ErrorCode {
    USER_NOT_FOUND, ENABLE_USER_AUTH, DUPLICATE_USER_ID
}

// 예외 발생
throw new RestApiException(UserErrorCode.USER_NOT_FOUND);

// 글로벌 핸들러 (HTTP 상태 코드 매핑)
@RestControllerAdvice
public class RestApiAdvice {
    // JwtTokenErrorCode → 401/403
    // ProgramHistErrorCode → 200
    // UserErrorCode.ENABLE_USER_AUTH → 406
    // 그 외 RestApiException → 400
    // 모든 Exception → 500
}
```

### 5.7 Caffeine 캐시

```java
// TTL 프리셋 (CacheConst)
public static final String CACHE_1SEC  = "1sec";
public static final String CACHE_5SEC  = "5sec";
public static final String CACHE_1MIN  = "1min";
public static final String CACHE_10MIN = "10min";
public static final String CACHE_1HOUR = "1hour";
public static final String CACHE_1DAY  = "1day";

// 사용
@Cacheable(value = CacheConst.CACHE_5SEC, key = "#dsId", sync = true)
public DatasetDto getDataset(String dsId) { ... }

// 이벤트 핸들러에서 만료
@CacheEvict(value = CacheConst.CACHE_5SEC, allEntries = true)
public void onDatasetUpserted(DatasetUpsertedEvent event) { ... }
```

### 5.8 비동기 처리 (AsyncConfig)

```java
// asyncExecutor: 이벤트 핸들러 등 일반 비동기
ThreadPoolTaskExecutor async = new ThreadPoolTaskExecutor();
async.setCorePoolSize(8);
async.setMaxPoolSize(24);
async.setQueueCapacity(200);
async.setRejectedExecutionHandler(new CallerRunsPolicy());

// batchExecutor: 배치 Job 전용
ThreadPoolTaskExecutor batch = new ThreadPoolTaskExecutor();
batch.setCorePoolSize(16);
batch.setMaxPoolSize(32);
batch.setQueueCapacity(1000);
batch.setRejectedExecutionHandler(new AbortPolicy());

// 사용
@Async("asyncExecutor")
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onDatasetDeleted(DatasetDeletedEvent event) { ... }
```

### 5.9 서비스 간 통신

API ↔ Batch 간 HTTP 통신은 WebClient(WebFlux) 사용.

```
API → Batch: WebClient, ${batch.url}/internal, X-Internal-Request: true 헤더
Batch → API: WebClient, ${api.url}/internal, X-Internal-Request: true 헤더
```

내부 요청 식별: `X-Internal-Request: true` 헤더로 CORS 필터에서 구분.

---

## 6. 설정 관리

### 프로파일 기반 리소스 오버레이

Gradle 빌드 시 `-Pprofile=local|dev|prod` 인자로 환경 결정.
기본값은 `common` (공통 설정만 적용).

```
src/main/
  resources/               -- 공통 (application.yml, application-common.yml)
  resources-env/
    local/                 -- 로컬 개발 환경 오버라이드
    dev/                   -- 개발 서버 오버라이드
    prod/                  -- 운영 서버 오버라이드
```

### application.yml 구조

```yaml
# application.yml (환경별 기본값)
spring:
  datasource:
    simulation: { url, username, password, pool 설정 }
    waternet:   { url, username, password, pool 설정 }

# application-common.yml (모든 환경 공통)
spring:
  servlet.multipart:
    max-file-size: 1GB
    max-request-size: 1GB
  batch:
    initialize-schema: never    # Batch 메타 테이블 수동 관리
  quartz:
    job-store-type: jdbc
    auto-startup: false         # 수동 스케줄러 시작
springdoc:
  api-docs.path: /simulation-api-docs
  swagger-ui.path: /simulation-swagger

# 파일 경로 설정
file:
  program-dir: /path/to/programs
  library-dir: /path/to/libraries
  dataset-dir: /path/to/datasets
  venv-dir:    /path/to/venvs
  layer-dir:   /path/to/layers
```

### 환경별 주요 차이점

| 항목 | local | dev | prod |
|---|---|---|---|
| simulation DB | localhost:5432 | 내부망 서버 | 운영 서버 |
| hbm2ddl.auto | update | update | none |
| HikariCP pool | 5/5 | 5/5 | 50/15 |
| API port | 8080 | - | 60083 |
| Batch port | 8081 | - | 60084 |

---

## 7. 네이밍 규칙

### DB 테이블 / 컬럼명

약어 기반 스네이크케이스. 테이블은 `_{도메인 약어}_m` 형태.

| 규칙 | 예시 |
|---|---|
| 테이블명 | `ds_m` (데이터셋), `pgm_m` (프로그램), `user_m` (사용자) |
| PK 컬럼 | `ds_id`, `pgm_id`, `user_id` |
| 이름 컬럼 | `ds_nm`, `pgm_nm` |
| 등록 정보 | `rgst_id`, `rgst_dttm` |
| 수정 정보 | `mdf_id`, `mdf_dttm` |
| 코드 컬럼 | `ds_type_cd`, `auth_cd`, `exec_stat_cd` |

### Java 클래스 / 메서드명

| 분류 | 규칙 | 예시 |
|---|---|---|
| 엔티티 | PascalCase | `Dataset`, `Program`, `VirtualEnvironment` |
| 컨트롤러 | `{도메인}Controller` | `DatasetController` |
| 서비스 | `{도메인}Service` | `DatasetService` |
| 리포지토리 | `{도메인}Repository`, `{도메인}CustomRepository`, `{도메인}CustomRepositoryImpl` | - |
| DTO (응답) | `{도메인}Dto` | `DatasetDto` |
| DTO (요청) | `{도메인}UpsertDto` | `DatasetUpsertDto` |
| DTO (검색) | `{도메인}SearchDto` | `DatasetSearchDto` |
| 이벤트 | `{도메인}{동작}Event` (record) | `DatasetDeletedEvent` |
| 이벤트 퍼블리셔 | `{도메인}EventPublisher` | `DatasetEventPublisher` |
| 에러코드 | `{도메인}ErrorCode` (enum) | `ProgramErrorCode` |

### Swagger API 태그 순서

```java
@Tag(name = "01. 사용자 관리")
@Tag(name = "02. 라이브러리 관리")
@Tag(name = "03. 데이터셋 관리")
// 숫자 접두사로 API 문서 내 순서 고정
```

---

## 8. 빌드 설정

### 모듈별 역할

```groovy
// settings.gradle
rootProject.name = 'simulation'
include 'common', 'api', 'batch'

// common/build.gradle
plugins { id 'java-library' }   // API 의존성을 소비 모듈에 노출

// api/build.gradle, batch/build.gradle
plugins { id 'org.springframework.boot' }
bootJar { archiveFileName = 'api.jar' }   // 또는 'batch.jar'
```

### 환경 프로파일 처리

```groovy
// api/build.gradle, batch/build.gradle
def profile = project.findProperty('profile') ?: 'common'
sourceSets.main.resources.srcDirs "src/main/resources-env/${profile}"

// 빌드 명령
./gradlew :api:bootJar -Pprofile=prod
```

### 커스텀 Maven 저장소

```groovy
// build.gradle (루트)
repositories {
    maven { url 'https://repo.osgeo.org/repository/release/' }  // GeoTools
    flatDir { dirs "$rootDir/libs" }  // 벤더 JAR (Tibero JDBC 등)
}
```

### QueryDSL Q클래스 생성

```groovy
// common/build.gradle
dependencies {
    implementation "com.querydsl:querydsl-jpa:5.0.0:jakarta"
    annotationProcessor "com.querydsl:querydsl-apt:5.0.0:jakarta"
}
// Q클래스 출력 경로: src/main/generated/
```

---

## 부록: 주요 파일 경로

| 구분 | 경로 |
|---|---|
| 공통 베이스 엔티티 | `common/src/main/java/com/hscmt/common/domain/BaseEntity.java` |
| 도메인 이벤트 엔티티 | `common/src/main/java/com/hscmt/common/domain/DomainEventEntity.java` |
| 이벤트 퍼블리셔 베이스 | `common/src/main/java/com/hscmt/common/event/AbstractDomainEventPublisher.java` |
| 응답 래퍼 | `common/src/main/java/com/hscmt/common/response/ResponseObject.java` |
| 베이스 컨트롤러 | `api/src/main/java/com/hscmt/common/controller/CommonController.java` |
| 글로벌 예외 핸들러 | `common/src/main/java/com/hscmt/common/exception/advice/RestApiAdvice.java` |
| JWT 검사 AOP | `api/src/main/java/com/hscmt/simulation/common/aop/CheckJwtToken.java` |
| 역할 검사 AOP | `api/src/main/java/com/hscmt/common/aop/CheckUserRole.java` |
| CORS 필터 | `common/src/main/java/com/hscmt/common/web/CorsFilter.java` |
| 캐시 설정 | `common/src/main/java/com/hscmt/common/cache/CacheConfig.java` |
| 비동기 설정 | `common/src/main/java/com/hscmt/common/config/AsyncConfig.java` |
| simulation JPA 설정 | `api/src/main/java/com/hscmt/simulation/common/config/jpa/SimulationJpaConfig.java` |
| waternet JPA 설정 | `api/src/main/java/com/hscmt/simulation/common/config/jpa/WaternetJpaConfig.java` |
| 커스텀 트랜잭션 어노테이션 | `api/src/main/java/com/hscmt/simulation/common/config/jpa/SimulationTx.java` |
| Swagger 설정 | `api/src/main/java/com/hscmt/common/swagger/SwaggerConfig.java` |
| DDL 스크립트 | `doc/ddl/*.sql` |
