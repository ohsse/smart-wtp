package com.mo.smartwtp.auth.service;

import com.mo.smartwtp.auth.domain.RefreshToken;
import com.mo.smartwtp.auth.repository.RefreshTokenRepository;
import com.mo.smartwtp.common.exception.JwtErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.jwt.JwtToken;
import com.mo.smartwtp.common.jwt.JwtTokenHelper;
import com.mo.smartwtp.common.jwt.JwtTokenInspection;
import com.mo.smartwtp.common.jwt.JwtTokenStatus;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class JwtTokenManagementService {

    /** 시스템이 자동 발급·회전·폐기하는 토큰의 감사 주체 */
    private static final String AUDIT_ACTOR = "system";

    private final RefreshTokenRepository refreshTokenRepository;
    private final JwtTokenHelper jwtTokenHelper;

    public JwtTokenManagementService(
            RefreshTokenRepository refreshTokenRepository,
            JwtTokenHelper jwtTokenHelper
    ) {
        this.refreshTokenRepository = refreshTokenRepository;
        this.jwtTokenHelper = jwtTokenHelper;
    }

    @Transactional
    public JwtToken issueTokens(String subject, Map<String, Object> claims) {
        JwtToken tokenPair = jwtTokenHelper.generateTokenPair(subject, claims);
        String refreshTokenHash = hashToken(tokenPair.getRefreshToken());
        LocalDateTime refreshTokenExpiresAt = toLocalDateTime(jwtTokenHelper.inspect(tokenPair.getRefreshToken()).expiresAt());

        RefreshToken refreshToken = refreshTokenRepository.findByUserId(subject)
                .map(existing -> {
                    existing.rotate(refreshTokenHash, refreshTokenExpiresAt, null, AUDIT_ACTOR);
                    return existing;
                })
                .orElseGet(() -> RefreshToken.create(subject, refreshTokenHash, refreshTokenExpiresAt, AUDIT_ACTOR));

        refreshTokenRepository.save(refreshToken);
        return tokenPair;
    }

    @Transactional
    public JwtToken rotateRefreshToken(String refreshToken) {
        JwtTokenInspection inspection = validateRefreshToken(refreshToken);
        String subject = inspection.subject();
        String inputTokenHash = hashToken(refreshToken);

        RefreshToken storedToken = refreshTokenRepository.findByUserId(subject)
                .orElseThrow(() -> new RestApiException(JwtErrorCode.REFRESH_TOKEN_NOT_FOUND));

        LocalDateTime now = LocalDateTime.now();
        if (storedToken.isRevoked()) {
            throw new RestApiException(JwtErrorCode.REFRESH_TOKEN_REVOKED);
        }
        if (storedToken.isExpired(now)) {
            throw new RestApiException(JwtErrorCode.EXPIRED_TOKEN);
        }
        if (!storedToken.getTokenHash().equals(inputTokenHash)) {
            throw new RestApiException(JwtErrorCode.REFRESH_TOKEN_MISMATCH);
        }

        JwtToken newTokenPair = jwtTokenHelper.generateTokenPair(subject, sanitizeClaims(inspection.claims()));
        storedToken.rotate(
                hashToken(newTokenPair.getRefreshToken()),
                toLocalDateTime(jwtTokenHelper.inspect(newTokenPair.getRefreshToken()).expiresAt()),
                now,
                AUDIT_ACTOR
        );
        refreshTokenRepository.save(storedToken);
        return newTokenPair;
    }

    @Transactional
    public void revokeRefreshToken(String subject) {
        refreshTokenRepository.findByUserId(subject)
                .ifPresent(token -> {
                    if (!token.isRevoked()) {
                        token.revoke(LocalDateTime.now(), AUDIT_ACTOR);
                        refreshTokenRepository.save(token);
                    }
                });
    }

    public JwtTokenInspection validateAccessToken(String token) {
        JwtTokenInspection inspection = jwtTokenHelper.inspect(token);
        if (inspection.status() == JwtTokenStatus.EXPIRED) {
            throw new RestApiException(JwtErrorCode.EXPIRED_TOKEN);
        }
        if (inspection.status() == JwtTokenStatus.INVALID) {
            throw new RestApiException(JwtErrorCode.INVALID_TOKEN);
        }
        if (!JwtTokenHelper.ACCESS_TOKEN_TYPE.equals(inspection.claims().get(JwtTokenHelper.TOKEN_TYPE_CLAIM))) {
            throw new RestApiException(JwtErrorCode.INVALID_TOKEN);
        }
        return inspection;
    }

    private JwtTokenInspection validateRefreshToken(String refreshToken) {
        JwtTokenInspection inspection = jwtTokenHelper.inspect(refreshToken);
        if (inspection.status() == JwtTokenStatus.EXPIRED) {
            throw new RestApiException(JwtErrorCode.EXPIRED_TOKEN);
        }
        if (inspection.status() == JwtTokenStatus.INVALID) {
            throw new RestApiException(JwtErrorCode.INVALID_TOKEN);
        }
        if (!JwtTokenHelper.REFRESH_TOKEN_TYPE.equals(inspection.claims().get(JwtTokenHelper.TOKEN_TYPE_CLAIM))) {
            throw new RestApiException(JwtErrorCode.INVALID_TOKEN);
        }
        return inspection;
    }

    private Map<String, Object> sanitizeClaims(Map<String, Object> claims) {
        Map<String, Object> sanitized = new LinkedHashMap<>(claims);
        sanitized.remove(JwtTokenHelper.TOKEN_TYPE_CLAIM);
        sanitized.remove("iss");
        sanitized.remove("sub");
        sanitized.remove("exp");
        sanitized.remove("iat");
        sanitized.remove("jti");
        sanitized.remove("nbf");
        return sanitized;
    }

    private LocalDateTime toLocalDateTime(Instant instant) {
        return LocalDateTime.ofInstant(instant, ZoneOffset.UTC);
    }

    private String hashToken(String token) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashed = digest.digest(token.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hashed);
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 algorithm is not available", exception);
        }
    }
}
