# 코딩 컨벤션

## 목적
- 이 문서는 `simulation` 백엔드 프로젝트의 구현 규칙을 정의한다.
- 신규 기능 개발, 유지보수, 코드 리뷰 시 공통 기준으로 사용한다.
- 세부 기준은 `docs/REFERENCE.md`를 우선 따르며, 이 문서는 실무에서 바로 적용할 수 있는 코딩 규칙 중심으로 정리한다.

## 적용 범위
- `common`: 공통 인프라, 공통 DTO, 예외, 이벤트, 유틸리티
- `api`: REST API 애플리케이션
- `batch`: 배치 및 스케줄링 애플리케이션

## 공통 원칙
- Java 21, UTF-8, 들여쓰기 4칸을 기준으로 한다.
- 패키지는 소문자만 사용하고, 클래스는 `PascalCase`, 메서드와 필드는 `camelCase`, 상수는 `UPPER_SNAKE_CASE`를 사용한다.
- 모듈 책임을 넘는 중복 로직은 피하고, 공통화가 필요한 경우에만 `common`으로 이동한다.
- 생성 코드는 `src/main/generated`에 두며 직접 수정하지 않는다.
- Lombok, Spring Boot, QueryDSL 등 현재 프로젝트의 기술 스택과 기존 패턴을 우선 존중한다.

## 패키지 및 모듈 규칙
- 최상위 구조는 기술 계층보다 도메인 중심의 feature-based 패키지를 사용한다.
- 공통 인프라는 `com.hscmt.common` 아래에 둔다.
- 시뮬레이션 도메인은 `com.hscmt.simulation.{도메인명}` 구조를 사용한다.
- 보조 데이터소스 도메인은 `com.hscmt.waternet.{도메인명}` 구조를 사용한다.
- 도메인 패키지 내부는 기본적으로 아래 구조를 따른다.

```text
{domain}/
  controller/
  service/
  repository/
    impl/
  event/
  dto/
  domain/
  comp/
```

- `common`에는 범용 인프라만 두고, 특정 도메인에 종속된 로직은 각 도메인 패키지에 둔다.

## 네이밍 규칙

### Java 클래스
- 엔티티: `{도메인명}`
- 컨트롤러: `{도메인명}Controller`
- 서비스: `{도메인명}Service`
- 리포지토리: `{도메인명}Repository`
- 커스텀 리포지토리: `{도메인명}CustomRepository`
- 커스텀 리포지토리 구현체: `{도메인명}CustomRepositoryImpl`
- 조회/응답 DTO: `{도메인명}Dto`
- 생성/수정 요청 DTO: `{도메인명}UpsertDto`
- 검색 조건 DTO: `{도메인명}SearchDto`
- 이벤트: `{도메인명}{동작}Event`
- 이벤트 발행기: `{도메인명}EventPublisher`
- 검증기/보조 컴포넌트: `{도메인명}Validator`, `{도메인명}FileManager`, `{도메인명}Comp`
- 에러 코드: `{도메인명}ErrorCode`
- 테스트 클래스: `{대상클래스명}Test`

### 데이터베이스
- 테이블명은 스네이크 케이스를 사용한다.
- 마스터 성격 테이블은 `_{약어}_m` 형식을 우선 사용한다.
- PK 컬럼은 `{도메인약어}_id` 형식을 사용한다.
- 이름 컬럼은 `{도메인약어}_nm` 형식을 사용한다.
- 등록/수정 메타 컬럼은 `rgst_id`, `rgst_dttm`, `mdf_id`, `mdf_dttm` 형식을 사용한다.
- 코드값 컬럼은 `_cd` 접미사를 사용한다.

## Entity 규칙
- 엔티티는 `@Getter`만 사용하고 `@Setter`는 사용하지 않는다.
- 기본 생성자는 `@NoArgsConstructor(access = AccessLevel.PROTECTED)`로 제한한다.
- 전체 필드 생성자는 외부 노출을 제한하고 필요 시 `PRIVATE` 접근 수준을 사용한다.
- PK는 `@GeneratedValue(strategy = GenerationType.UUID)`를 기본으로 사용한다.
- 공통 메타 정보 또는 이벤트 기능이 필요하면 `BaseEntity` 또는 `DomainEventEntity`를 상속한다.
- 상태 변경은 setter 대신 의도가 드러나는 메서드로 처리한다.
  - 예: `changeInfo(...)`, `changeGrpInfo(...)`
- 엔티티 생성은 생성자 직접 호출보다 정적 팩토리 메서드 또는 용도가 분명한 생성 방식을 우선 사용한다.
- null 또는 빈 문자열 처리 기준이 필요한 경우 변경 메서드 내부에서 일관되게 처리한다.

```java
@Entity
@Table(name = "ds_m")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Dataset extends DomainEventEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "ds_id")
    private String dsId;

    @Column(name = "ds_nm")
    private String dsNm;

    public void changeInfo(DatasetUpsertDto dto) {
        if (dto.getDsNm() != null) {
            this.dsNm = dto.getDsNm();
        }
    }
}
```

## DTO 규칙
- DTO는 역할에 따라 명확히 분리한다.
  - `XxxDto`: 조회/응답
  - `XxxUpsertDto`: 생성/수정 요청
  - `XxxSearchDto`: 검색 조건
- DTO에는 Swagger/OpenAPI 문서를 위해 `@Schema`를 적극적으로 작성한다.
- QueryDSL 조회 DTO는 필요한 경우 프로젝션 필드 정의 메서드를 제공한다.
- 상속 구조를 가진 DTO는 `@JsonTypeInfo`와 `@JsonSubTypes`로 다형성 역직렬화를 명시한다.
- 요청 DTO와 응답 DTO를 한 클래스로 혼용하지 않는다.
- 공통 검색 조건이 있으면 `FromToSearchDto` 같은 베이스 DTO를 상속해 재사용한다.

```java
@Data
@NoArgsConstructor
@Schema(description = "데이터셋 DTO")
public class DatasetDto extends BaseDto {
    @Schema(description = "데이터셋 ID", example = "ds-001")
    private String dsId;
}
```

## Repository 규칙
- 조회와 영속화 책임을 분리하기 위해 3계층 패턴을 사용한다.
  - `JpaRepository`
  - `CustomRepository`
  - `CustomRepositoryImpl`
- 단순 CRUD는 `JpaRepository`에 맡기고, 복잡한 조회는 커스텀 리포지토리와 QueryDSL로 분리한다.
- QueryDSL 구현체는 `JPAQueryFactory`를 사용한다.
- 조회 결과가 엔티티가 아니라 화면/응답 중심이면 DTO 프로젝션을 우선 사용한다.
- 커스텀 조회 메서드명은 반환 목적이 드러나게 작성한다.
  - 예: `findAllDatasets`, `findDatasetDtoById`, `groupingForDataset`

```java
public interface DatasetRepository
        extends JpaRepository<Dataset, String>, DatasetCustomRepository {
}

public interface DatasetCustomRepository {
    List<DatasetDto> findList(DatasetSearchDto searchDto);
}
```

## Service 규칙
- 서비스는 인터페이스 없이 구체 클래스를 기본으로 사용한다.
- 의존성 주입은 `@RequiredArgsConstructor` 기반 생성자 주입을 사용한다.
- 클래스 레벨에는 읽기 전용 트랜잭션을 기본으로 선언한다.
  - 예: `@SimulationTx(readOnly = true)`
- 쓰기 작업 메서드에는 메서드 레벨 `@SimulationTx`로 오버라이드한다.
- `@Transactional`을 직접 사용하지 않고 프로젝트 전용 트랜잭션 어노테이션을 사용한다.
- 유효성 검사는 서비스에 과도하게 쌓지 말고 `Validator` 컴포넌트로 분리한다.
- 파일 처리, 외부 연동, 이벤트 발행 같은 부가 책임도 전용 컴포넌트로 분리한다.
- 서비스는 비즈니스 흐름을 조합하는 계층으로 유지하고, 컨트롤러/리포지토리 역할을 침범하지 않는다.

```java
@Service
@Slf4j
@RequiredArgsConstructor
@SimulationTx(readOnly = true)
public class DatasetService {

    private final DatasetRepository datasetRepository;
    private final DatasetEventPublisher publisher;

    @SimulationTx
    public void saveDataset(DatasetUpsertDto dto) {
        // 쓰기 로직
    }
}
```

## Controller 규칙
- 모든 컨트롤러는 `CommonController`를 상속한다.
- 응답 타입은 `ResponseEntity<ResponseObject<T>>`를 기본으로 사용한다.
- 성공 응답은 `getResponseEntity(data)` 또는 `getResponseEntity()`로 래핑한다.
- 요청 매핑 경로는 자원 의미가 드러나게 작성한다.
- 읽기/쓰기 API를 명확히 구분하고, 권한이 필요한 쓰기 API에는 `@UserRoleCheckRequired`를 적용한다.
- JWT 검사 제외가 필요한 엔드포인트에는 `@UncheckedJwtToken`을 명시한다.
- 컨트롤러는 입력 수집과 서비스 호출에 집중하고 비즈니스 로직을 직접 담지 않는다.

## Swagger/OpenAPI 규칙
- 모든 API에는 `@Tag`, `@Operation`, `@ApiResponses`를 작성한다.
- `summary`는 한 줄 목적 중심으로 작성한다.
- `description`은 조건, 제약, 예외가 필요한 경우에만 짧게 작성한다.
- 요청/응답 DTO 필드는 `@Schema(description = "...", example = "...")`를 명시한다.
- 성공/실패 응답 코드는 누락 없이 문서화한다.
  - 기본 예: `200`, `400`, `401`, `403`, `404`, `500`
- 인증이 필요한 API는 필요한 헤더 또는 인증 조건을 설명한다.
- 동일 의미의 필드는 문서 전반에서 같은 이름을 사용한다.
  - 예: `userId`와 `memberId` 혼용 금지
- `@Tag` 이름은 정렬 순서가 필요하면 번호 접두사를 사용한다.

```java
@Tag(name = "03. 데이터셋 관리")
@Operation(summary = "데이터셋 목록 조회")
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "성공")
})
```

## 트랜잭션 및 데이터소스 규칙
- 다중 데이터소스 환경이므로 데이터소스별 전용 트랜잭션 어노테이션을 사용한다.
  - `@SimulationTx`
  - `@WaternetTx`
- 읽기 작업은 `readOnly = true`를 기본으로 한다.
- 쓰기 작업 또는 별도 커밋 경계가 필요하면 메서드에 명시적으로 선언한다.
- `REQUIRES_NEW` 사용은 이벤트 후처리, 이력 저장 등 독립 커밋이 필요한 경우로 제한한다.
- 데이터소스 경계를 넘는 로직은 서비스 또는 전용 컴포넌트에서 명확히 분리한다.

## 이벤트 규칙
- 엔티티 변경 후 후속 처리는 도메인 이벤트 패턴으로 분리한다.
- 이벤트는 Java `record`로 정의한다.
- 저장, 수정, 삭제 후 후속 작업이 필요하면 `EventPublisher`를 통해 발행한다.
- 이벤트 핸들러는 `@TransactionalEventListener`와 `@Async` 조합을 기본으로 사용한다.
- 캐시 만료, 파일 정리, 배치 트리거 같은 후속 작업은 이벤트 핸들러에서 처리한다.

```java
public record DatasetDeletedEvent(String dsId) {
}
```

## 예외 및 응답 규칙
- 비즈니스 예외는 `RestApiException`으로 통일한다.
- 에러 코드는 `ErrorCode` 인터페이스를 구현하는 enum으로 관리한다.
- API 응답은 항상 `ResponseObject` 형태를 사용한다.
  - 성공: `code = "SUCCESS"`
  - 실패: `code = ErrorCode.name()`
- 예외별 HTTP 상태 코드는 `RestApiAdvice`에서 일관되게 매핑한다.
- 컨트롤러나 서비스에서 임의 문자열 에러 코드를 직접 만들지 않는다.

## 캐시 및 비동기 규칙
- 캐시 이름은 `CacheConst`에 정의된 TTL 프리셋을 사용한다.
- 캐시 적중 대상은 조회성 데이터에 한정하고, 변경 후에는 이벤트 기반 만료를 우선 사용한다.
- 비동기 처리는 `AsyncConfig`에 정의된 실행기를 사용한다.
- 배치 전용 작업과 일반 비동기 작업은 서로 다른 실행기를 사용한다.

## 사용 방법
- 새 기능 추가 시 아래 순서를 기본으로 따른다.
  1. 도메인 패키지 위치를 정한다.
  2. Entity와 DTO를 역할별로 분리해 정의한다.
  3. `Repository + CustomRepository + Impl` 구조를 만든다.
  4. Service에 읽기 기본 트랜잭션과 쓰기 메서드를 정의한다.
  5. Controller에서 `ResponseObject` 형식으로 API를 노출한다.
  6. Swagger 문서와 에러 응답을 함께 작성한다.
  7. 필요 시 Validator, EventPublisher, FileManager 같은 보조 컴포넌트를 분리한다.

## 주의사항 / 한계
- 이 문서는 현재 코드의 모든 예외적 구현을 그대로 추종하지 않는다.
- 기준은 `docs/REFERENCE.md`의 목표 표준안이며, 일부 기존 코드는 점진적으로 정리 대상이 될 수 있다.
- 기존 기능을 수정할 때는 무리한 대규모 리팩터링보다, 변경 범위 안에서 본 컨벤션에 더 가깝게 맞추는 방향을 우선한다.
