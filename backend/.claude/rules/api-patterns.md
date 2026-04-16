# API 계층 코드 패턴

## Service 패턴

```java
@Service
@Slf4j
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DatasetService {

    private final DatasetRepository datasetRepository;
    private final DatasetEventPublisher publisher;

    @Transactional
    public void saveDataset(DatasetUpsertDto dto) {
        // 쓰기 로직
    }
}
```

## Repository 패턴

```java
public interface DatasetRepository
        extends JpaRepository<Dataset, String>, DatasetCustomRepository {
}

public interface DatasetCustomRepository {
    List<DatasetDto> findList(DatasetSearchDto searchDto);
}
```

커스텀 조회 메서드명은 반환 목적이 드러나게 작성한다.
- 예: `findAllDatasets`, `findDatasetDtoById`, `groupingForDataset`

## DTO 패턴

```java
@Data
@NoArgsConstructor
@Schema(description = "데이터셋 DTO")
public class DatasetDto extends BaseDto {
    @Schema(description = "데이터셋 ID", example = "ds-001")
    private String dsId;
}
```

- 공통 검색 조건은 부모 클래스, 특화 조건은 자식 클래스로 상속 구조를 사용한다.
- `@JsonTypeInfo` / `@JsonSubTypes`로 다형성 역직렬화가 필요한 경우에만 사용한다.

## Swagger/OpenAPI 패턴

```java
@Tag(name = "03. 데이터셋 관리")
@Operation(summary = "데이터셋 목록 조회")
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "성공"),
    @ApiResponse(responseCode = "400", description = "잘못된 요청"),
    @ApiResponse(responseCode = "401", description = "인증 실패"),
    @ApiResponse(responseCode = "403", description = "권한 없음"),
    @ApiResponse(responseCode = "404", description = "리소스 없음"),
    @ApiResponse(responseCode = "500", description = "서버 오류")
})
```

- `@Tag` 이름은 정렬 순서가 필요하면 번호 접두사를 사용한다.
- `summary`는 한 줄 목적 중심으로 작성한다.
- `description`은 조건/제약/예외가 필요한 경우에만 짧게 작성한다.
- 동일 의미의 필드는 문서 전반에서 같은 이름을 사용한다. (예: `userId`와 `memberId` 혼용 금지)
