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


## 외부 할당 PK 엔티티 패턴

PK를 외부에서 할당받는 엔티티(`@GeneratedValue` 미사용) — 예: `user_m.user_id`, `pump_m.pump_id` 같은 도메인 자연키 기반 마스터 — 는 반드시 `Persistable<ID>`를 구현해야 한다.

미구현 시 `save()`가 ID null-check로 신규 여부를 판정하므로 항상 `em.merge()`를 호출, 불필요한 `SELECT`가 선행된다.

```java
@Entity
@Table(name = "user_m")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class User extends BaseEntity implements Persistable<String> {

    @Id
    @Column(name = "user_id", nullable = false, length = 50)
    private String userId;

    // ... 나머지 필드 ...

    /** {@inheritDoc} — PK를 반환한다. */
    @Override
    public String getId() {
        return userId;
    }
    // isNew()는 BaseEntity의 newEntity 플래그에 위임 — 별도 구현 불필요

    public static User create(String userId, /* ... */) {
        return new User(userId, /* ... */);
    }
}
```

- `getId()`만 override하면 된다. `isNew()`는 `BaseEntity`가 `@Transient newEntity` 플래그로 제공한다.
- `@PostLoad`와 `@PrePersist`에서 자동으로 플래그를 전환하므로 직접 조작하지 않는다.
- UUID 자동생성 엔티티는 `Persistable` 구현이 불필요하다.

---

## 규칙 요약

- `@Getter`만 사용, `@Setter` 사용 금지
- 기본 생성자: `@NoArgsConstructor(access = AccessLevel.PROTECTED)`
- 전체 필드 생성자: 필요 시 `PRIVATE` 접근 수준
- PK: `@GeneratedValue(strategy = GenerationType.UUID)` 기본
- **`@GeneratedValue`가 없는 외부할당 PK 엔티티는 `Persistable<ID>` 구현 필수** (`getId()` override, `isNew()`는 `BaseEntity` 위임)
- 공통 메타 필요 시 `BaseEntity` 상속, 이벤트 기능 필요 시 `DomainEventEntity` 상속
- 상태 변경은 `changeInfo(...)`, `changeGrpInfo(...)` 형태의 의도 드러나는 메서드로 처리
- null 또는 빈 문자열 처리 기준이 필요한 경우 변경 메서드 내부에서 일관되게 처리
