package com.mo.smartwtp.common.domain;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import lombok.Getter;

import java.time.LocalDateTime;

/**
 * 공통 감사(Audit) 필드를 제공하는 엔티티 베이스 클래스.
 *
 * <p>모든 엔티티는 이 클래스 또는 {@link DomainEventEntity}를 상속한다.
 * 도메인 이벤트가 필요한 엔티티는 {@link DomainEventEntity}를, 그렇지 않은 경우 이 클래스를 상속한다.</p>
 */
@MappedSuperclass
@Getter
public abstract class BaseEntity {

    /** 엔티티 최초 생성 일시 */
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    /** 엔티티 최종 수정 일시 */
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    /**
     * 최초 저장 시 생성/수정 일시를 현재 시각으로 설정한다.
     */
    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    /**
     * 업데이트 시 수정 일시를 현재 시각으로 갱신한다.
     */
    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}
