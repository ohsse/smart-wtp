# 엔티티 코드 패턴

## 기본 엔티티 패턴

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

    /**
     * 정적 팩토리 메서드 — 생성자 직접 호출 대신 사용
     */
    public static Dataset create(DatasetUpsertDto dto) {
        return new Dataset(null, dto.getDsNm());
    }

    /**
     * 상태 변경은 의도가 드러나는 메서드로 처리
     */
    public void changeInfo(DatasetUpsertDto dto) {
        if (dto.getDsNm() != null) {
            this.dsNm = dto.getDsNm();
        }
    }
}
```

## 규칙 요약

- `@Getter`만 사용, `@Setter` 사용 금지
- 기본 생성자: `@NoArgsConstructor(access = AccessLevel.PROTECTED)`
- 전체 필드 생성자: 필요 시 `PRIVATE` 접근 수준
- PK: `@GeneratedValue(strategy = GenerationType.UUID)` 기본
- 공통 메타 필요 시 `BaseEntity` 상속, 이벤트 기능 필요 시 `DomainEventEntity` 상속
- 상태 변경은 `changeInfo(...)`, `changeGrpInfo(...)` 형태의 의도 드러나는 메서드로 처리
- null 또는 빈 문자열 처리 기준이 필요한 경우 변경 메서드 내부에서 일관되게 처리
