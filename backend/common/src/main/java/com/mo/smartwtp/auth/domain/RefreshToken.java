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

@Entity
@Table(name = "auth_refresh_token")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class RefreshToken extends BaseEntity {

    @Id
    @Column(name = "token_id", nullable = false, length = 36)
    private String tokenId;

    @Column(name = "subject", nullable = false, length = 100)
    private String subject;

    @Column(name = "token_hash", nullable = false, length = 64)
    private String tokenHash;

    @Column(name = "expires_at", nullable = false)
    private LocalDateTime expiresAt;

    @Column(name = "revoked_at")
    private LocalDateTime revokedAt;

    @Column(name = "last_used_at")
    private LocalDateTime lastUsedAt;

    public static RefreshToken create(String subject, String tokenHash, LocalDateTime expiresAt) {
        return new RefreshToken(UUID.randomUUID().toString(), subject, tokenHash, expiresAt, null, null);
    }

    public boolean isRevoked() {
        return revokedAt != null;
    }

    public boolean isExpired(LocalDateTime now) {
        return expiresAt.isBefore(now);
    }

    public void rotate(String tokenHash, LocalDateTime expiresAt, LocalDateTime lastUsedAt) {
        this.tokenHash = tokenHash;
        this.expiresAt = expiresAt;
        this.lastUsedAt = lastUsedAt;
        this.revokedAt = null;
    }

    public void revoke(LocalDateTime revokedAt) {
        this.revokedAt = revokedAt;
        this.lastUsedAt = revokedAt;
    }
}
