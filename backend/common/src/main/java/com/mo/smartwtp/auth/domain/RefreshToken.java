package com.mo.smartwtp.auth.domain;

import com.mo.smartwtp.common.domain.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * JWT 리프레시 토큰 명세 엔티티.
 *
 * <p>토큰 원본은 저장하지 않고 SHA-256 해시값만 보관한다.
 * 1계정 1토큰 정책 — {@code user_id} 가 유니크 키 역할을 한다.</p>
 */
@Entity
@Table(name = "refresh_token_p")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class RefreshToken extends BaseEntity {

    /** 토큰 식별자 (UUID 자동 생성) */
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "token_id", nullable = false, length = 36)
    private String tokenId;

    /** 토큰 주체 (사용자 ID, user_m.user_id 참조) */
    @Column(name = "user_id", nullable = false, length = 50)
    private String userId;

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

    /** 등록자 ID */
    @Column(name = "rgstr_id", length = 50)
    private String rgstrId;

    /** 수정자 ID */
    @Column(name = "updt_id", length = 50)
    private String updtId;

    /**
     * 새 리프레시 토큰 레코드를 생성한다.
     *
     * @param userId      사용자 ID
     * @param tokenHash   SHA-256 해시된 토큰값
     * @param exprDtm     만료 일시
     * @param registrarId 등록자 ID
     */
    public static RefreshToken create(String userId, String tokenHash, LocalDateTime exprDtm, String registrarId) {
        return new RefreshToken(null, userId, tokenHash, exprDtm, null, null, registrarId, registrarId);
    }

    /**
     * 폐기 여부를 확인한다.
     */
    public boolean isRevoked() {
        return revokeDtm != null;
    }

    /**
     * 만료 여부를 확인한다.
     *
     * @param now 비교 기준 일시
     */
    public boolean isExpired(LocalDateTime now) {
        return exprDtm.isBefore(now);
    }

    /**
     * 토큰을 갱신한다 (리프레시 토큰 로테이션).
     *
     * @param tokenHash   새 SHA-256 해시된 토큰값
     * @param exprDtm     새 만료 일시
     * @param lastUsedDtm 마지막 사용 일시
     * @param updaterId   수정자 ID
     */
    public void rotate(String tokenHash, LocalDateTime exprDtm, LocalDateTime lastUsedDtm, String updaterId) {
        this.tokenHash = tokenHash;
        this.exprDtm = exprDtm;
        this.lastUsedDtm = lastUsedDtm;
        this.revokeDtm = null;
        this.updtId = updaterId;
    }

    /**
     * 토큰을 폐기한다 (로그아웃).
     *
     * @param revokeDtm 폐기 일시
     * @param updaterId 수정자 ID
     */
    public void revoke(LocalDateTime revokeDtm, String updaterId) {
        this.revokeDtm = revokeDtm;
        this.lastUsedDtm = revokeDtm;
        this.updtId = updaterId;
    }
}
