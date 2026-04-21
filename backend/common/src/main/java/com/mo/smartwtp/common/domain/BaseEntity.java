package com.mo.smartwtp.common.domain;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import jakarta.persistence.PostLoad;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Transient;
import lombok.Getter;
import org.springframework.data.domain.Persistable;

import java.time.LocalDateTime;

/**
 * 공통 감사(Audit) 필드를 제공하는 엔티티 베이스 클래스.
 *
 * <p>모든 엔티티는 이 클래스 또는 {@link DomainEventEntity}를 상속한다.
 * 도메인 이벤트가 필요한 엔티티는 {@link DomainEventEntity}를, 그렇지 않은 경우 이 클래스를 상속한다.</p>
 *
 * <p>외부에서 PK를 할당받는 엔티티({@code @GeneratedValue} 미사용)는
 * {@code implements Persistable<ID>}를 선언하고 {@code getId()}만 구현한다.
 * {@code isNew()} 판정은 이 클래스의 {@code newEntity} 플래그가 담당하므로
 * {@link org.springframework.data.repository.CrudRepository#save save()} 호출 시
 * 신규 엔티티는 항상 {@code em.persist()} 경로를 따른다.</p>
 */
@MappedSuperclass
@Getter
public abstract class BaseEntity {

    /** 엔티티 최초 생성 일시 */
    @Column(name = "rgstr_dtm", nullable = false)
    private LocalDateTime rgstrDtm;

    /** 엔티티 최종 수정 일시 */
    @Column(name = "updt_dtm", nullable = false)
    private LocalDateTime updtDtm;

    /**
     * {@link Persistable#isNew()} 판정용 신규 여부 플래그.
     * JPA 리플렉션 생성·기본 생성자 호출 시 true, persist 또는 로드 후 false로 전환된다.
     */
    @Transient
    private boolean newEntity = true;

    /**
     * {@link Persistable}을 구현하는 하위 엔티티가 위임하는 신규 여부 판정 메서드.
     */
    public boolean isNew() {
        return newEntity;
    }

    /**
     * 최초 저장 시 생성/수정 일시를 현재 시각으로 설정하고 신규 플래그를 해제한다.
     */
    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        this.rgstrDtm = now;
        this.updtDtm = now;
        this.newEntity = false;
    }

    /**
     * 업데이트 시 수정 일시를 현재 시각으로 갱신한다.
     */
    @PreUpdate
    protected void onUpdate() {
        this.updtDtm = LocalDateTime.now();
    }

    /**
     * DB에서 로드된 엔티티의 신규 플래그를 해제한다.
     */
    @PostLoad
    protected void onLoad() {
        this.newEntity = false;
    }
}
