package com.mo.smartwtp.auth.domain;

import com.mo.smartwtp.common.domain.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import java.util.UUID;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * JWT 리프레시 토큰 엔티티.
 *
 * <p>토큰 원본은 저장하지 않고 SHA-256 해시값만 보관한다.
 * 1계정 1토큰 정책 — subject가 유니크 키 역할을 한다.</p>
 */
@Entity
@Table(name = "auth_refresh_token")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class RefreshToken extends BaseEntity {

    @Id
    @Column(name = "token_id", nullable = false, length = 36)
    private String tokenId;

    /** 토큰 주체 (사용자 식별자) */
    @Column(name = "subject", nullable = false, length = 100)
    private String subject;

    /** SHA-256 해시된 토큰값 */
    @Column(name = "token_hash", nullable = false, length = 64)
    private String tokenHash;

    /** 토큰 만료 일시 */
    @Column(name = "expr_dtm", nullable = false)
    private LocalDateTime exprDtm;

    /** 토큰 폐기 일시 (null이면 활성) */
    @Column(name = "revoke_dtm")
    private LocalDateTime revokeDtm;

    /** 마지막 사용 일시 */
    @Column(name = "last_used_dtm")
    private LocalDateTime lastUsedDtm;

    /**
     * 새 리프레시 토큰 레코드를 생성한다.
     */
    public static RefreshToken create(String subject, String tokenHash, LocalDateTime exprDtm) {
        return new RefreshToken(UUID.randomUUID().toString(), subject, tokenHash, exprDtm, null, null);
    }

    /** 폐기 여부 확인 */
    public boolean isRevoked() {
        return revokeDtm != null;
    }

    /** 만료 여부 확인 */
    public boolean isExpired(LocalDateTime now) {
        return exprDtm.isBefore(now);
    }

    /**
     * 토큰을 갱신한다 (리프레시 토큰 로테이션).
     */
    public void rotate(String tokenHash, LocalDateTime exprDtm, LocalDateTime lastUsedDtm) {
        this.tokenHash = tokenHash;
        this.exprDtm = exprDtm;
        this.lastUsedDtm = lastUsedDtm;
        this.revokeDtm = null;
    }

    /**
     * 토큰을 폐기한다 (로그아웃).
     */
    public void revoke(LocalDateTime revokeDtm) {
        this.revokeDtm = revokeDtm;
        this.lastUsedDtm = revokeDtm;
    }
}
