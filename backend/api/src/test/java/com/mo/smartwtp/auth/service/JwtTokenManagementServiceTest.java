package com.mo.smartwtp.auth.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.mo.smartwtp.auth.domain.RefreshToken;
import com.mo.smartwtp.auth.repository.RefreshTokenRepository;
import com.mo.smartwtp.common.exception.JwtErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.jwt.JwtToken;
import com.mo.smartwtp.common.jwt.JwtTokenHelper;
import com.mo.smartwtp.common.jwt.JwtTokenInspection;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;

class JwtTokenManagementServiceTest {

    private static final String SECRET = "smart-wtp-jwt-secret-key-must-be-long-enough-2026";

    @Test
    void issuesAndValidatesAccessToken() {
        AtomicReference<RefreshToken> storedToken = new AtomicReference<>();
        JwtTokenManagementService service = new JwtTokenManagementService(
                inMemoryRepository(storedToken),
                new JwtTokenHelper(SECRET, "smart-wtp", 30, 7)
        );

        JwtToken token = service.issueTokens("user-1", Map.of("role", "ADMIN"));
        JwtTokenInspection inspection = service.validateAccessToken(token.getAccessToken());

        assertEquals("user-1", inspection.subject());
        assertEquals("ADMIN", inspection.claims().get("role"));
    }

    @Test
    void rotatesRefreshTokenAndRejectsPreviousToken() {
        AtomicReference<RefreshToken> storedToken = new AtomicReference<>();
        JwtTokenManagementService service = new JwtTokenManagementService(
                inMemoryRepository(storedToken),
                new JwtTokenHelper(SECRET, "smart-wtp", 30, 7)
        );

        JwtToken firstPair = service.issueTokens("user-1", Map.of("role", "ADMIN"));
        JwtToken secondPair = service.rotateRefreshToken(firstPair.getRefreshToken());

        assertNotEquals(firstPair.getRefreshToken(), secondPair.getRefreshToken());

        RestApiException exception = assertThrows(
                RestApiException.class,
                () -> service.rotateRefreshToken(firstPair.getRefreshToken())
        );
        assertEquals(JwtErrorCode.REFRESH_TOKEN_MISMATCH, exception.getErrorCode());
    }

    @Test
    void rejectsExpiredRefreshToken() {
        AtomicReference<RefreshToken> storedToken = new AtomicReference<>();
        JwtTokenManagementService service = new JwtTokenManagementService(
                inMemoryRepository(storedToken),
                new JwtTokenHelper(SECRET, "smart-wtp", 30, -1)
        );

        JwtToken token = service.issueTokens("user-1", Map.of());

        RestApiException exception = assertThrows(
                RestApiException.class,
                () -> service.rotateRefreshToken(token.getRefreshToken())
        );

        assertEquals(JwtErrorCode.EXPIRED_TOKEN, exception.getErrorCode());
    }

    @Test
    void rejectsRefreshTokenWhenStoredValueIsRevoked() {
        AtomicReference<RefreshToken> storedToken = new AtomicReference<>();
        JwtTokenManagementService service = new JwtTokenManagementService(
                inMemoryRepository(storedToken),
                new JwtTokenHelper(SECRET, "smart-wtp", 30, 7)
        );

        JwtToken token = service.issueTokens("user-1", Map.of());
        service.revokeRefreshToken("user-1");

        RestApiException exception = assertThrows(
                RestApiException.class,
                () -> service.rotateRefreshToken(token.getRefreshToken())
        );

        assertEquals(JwtErrorCode.REFRESH_TOKEN_REVOKED, exception.getErrorCode());
    }

    private RefreshTokenRepository inMemoryRepository(AtomicReference<RefreshToken> storedToken) {
        RefreshTokenRepository repository = mock(RefreshTokenRepository.class);
        when(repository.findByUserId(any())).thenAnswer(invocation -> {
            String userId = invocation.getArgument(0, String.class);
            RefreshToken token = storedToken.get();
            if (token == null || !token.getUserId().equals(userId)) {
                return Optional.empty();
            }
            return Optional.of(token);
        });
        when(repository.save(any(RefreshToken.class))).thenAnswer(invocation -> {
            RefreshToken token = invocation.getArgument(0, RefreshToken.class);
            storedToken.set(token);
            return token;
        });
        return repository;
    }
}
