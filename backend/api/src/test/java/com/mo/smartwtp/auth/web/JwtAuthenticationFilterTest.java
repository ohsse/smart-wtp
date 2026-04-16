package com.mo.smartwtp.auth.web;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mo.smartwtp.auth.config.AuthJwtProperties;
import com.mo.smartwtp.auth.service.JwtTokenManagementService;
import com.mo.smartwtp.common.exception.JwtErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.jwt.JwtTokenInspection;
import com.mo.smartwtp.common.jwt.JwtTokenStatus;
import java.time.Instant;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

class JwtAuthenticationFilterTest {

    @Test
    void skipsExcludedPath() throws Exception {
        JwtAuthenticationFilter filter = new JwtAuthenticationFilter(
                mock(JwtTokenManagementService.class),
                new ApiErrorResponseWriter(new ObjectMapper()),
                createAuthJwtProperties()
        );

        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/swagger-ui/index.html");
        request.setServletPath("/swagger-ui/index.html");
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockFilterChain filterChain = new MockFilterChain();

        filter.doFilter(request, response, filterChain);

        assertEquals(200, response.getStatus());
    }

    @Test
    void returnsUnauthorizedWhenAuthorizationHeaderIsMissing() throws Exception {
        JwtAuthenticationFilter filter = new JwtAuthenticationFilter(
                mock(JwtTokenManagementService.class),
                new ApiErrorResponseWriter(new ObjectMapper()),
                createAuthJwtProperties()
        );

        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/secure/resource");
        request.setServletPath("/secure/resource");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertEquals(401, response.getStatus());
        assertEquals("{\"code\":\"MISSING_ACCESS_TOKEN\",\"data\":null}", response.getContentAsString());
    }

    @Test
    void setsRequestAttributesWhenTokenIsValid() throws Exception {
        JwtTokenManagementService service = mock(JwtTokenManagementService.class);
        JwtAuthenticationFilter filter = new JwtAuthenticationFilter(
                service,
                new ApiErrorResponseWriter(new ObjectMapper()),
                createAuthJwtProperties()
        );

        when(service.validateAccessToken("valid-token")).thenReturn(new JwtTokenInspection(
                JwtTokenStatus.VALID,
                "user-1",
                Map.of("role", "ADMIN"),
                Instant.now(),
                Instant.now().plusSeconds(60)
        ));

        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/secure/resource");
        request.setServletPath("/secure/resource");
        request.addHeader("Authorization", "Bearer valid-token");
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockFilterChain filterChain = new MockFilterChain();

        filter.doFilter(request, response, filterChain);

        assertEquals("user-1", request.getAttribute(JwtAuthenticationFilter.AUTH_SUBJECT_ATTRIBUTE));
        assertEquals(Map.of("role", "ADMIN"), request.getAttribute(JwtAuthenticationFilter.AUTH_CLAIMS_ATTRIBUTE));
        verify(service).validateAccessToken("valid-token");
    }

    @Test
    void returnsUnauthorizedWhenTokenValidationFails() throws Exception {
        JwtTokenManagementService service = mock(JwtTokenManagementService.class);
        JwtAuthenticationFilter filter = new JwtAuthenticationFilter(
                service,
                new ApiErrorResponseWriter(new ObjectMapper()),
                createAuthJwtProperties()
        );

        doThrow(new RestApiException(JwtErrorCode.INVALID_TOKEN))
                .when(service)
                .validateAccessToken("invalid-token");

        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/secure/resource");
        request.setServletPath("/secure/resource");
        request.addHeader("Authorization", "Bearer invalid-token");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertEquals(401, response.getStatus());
        assertEquals("{\"code\":\"INVALID_TOKEN\",\"data\":null}", response.getContentAsString());
        assertNull(request.getAttribute(JwtAuthenticationFilter.AUTH_SUBJECT_ATTRIBUTE));
    }

    private AuthJwtProperties createAuthJwtProperties() {
        AuthJwtProperties properties = new AuthJwtProperties();
        properties.setSecret("smart-wtp-jwt-secret-key-must-be-long-enough-2026");
        properties.setIssuer("smart-wtp-api");
        properties.setAccessTokenExpirationMinutes(30);
        properties.setRefreshTokenExpirationDays(7);
        properties.setExcludePaths(java.util.List.of(
                "/swagger-ui/**",
                "/v3/api-docs/**",
                "/swagger-ui.html",
                "/error"
        ));
        return properties;
    }
}
