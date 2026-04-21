package com.mo.smartwtp.auth.guard;

import com.mo.smartwtp.auth.exception.AuthErrorCode;
import com.mo.smartwtp.auth.web.JwtAuthenticationFilter;
import com.mo.smartwtp.common.exception.RestApiException;
import jakarta.servlet.http.HttpServletRequest;
import java.util.Map;
import org.springframework.stereotype.Component;

/**
 * 컨트롤러 레이어에서 역할(Role) 기반 접근을 검사하는 컴포넌트.
 *
 * <p>{@link JwtAuthenticationFilter}가 request attribute에 적재한 claims를 사용한다.</p>
 */
@Component
public class RoleGuard {

    /**
     * ADMIN 역할 여부를 검사한다.
     *
     * @param request 현재 HTTP 요청 (claims가 attribute로 적재되어 있어야 함)
     * @return 인증된 사용자의 subject (userId)
     * @throws RestApiException FORBIDDEN — ADMIN 역할이 아닌 경우
     */
    @SuppressWarnings("unchecked")
    public String requireAdmin(HttpServletRequest request) {
        String subject = (String) request.getAttribute(JwtAuthenticationFilter.AUTH_SUBJECT_ATTRIBUTE);
        Map<String, Object> claims =
                (Map<String, Object>) request.getAttribute(JwtAuthenticationFilter.AUTH_CLAIMS_ATTRIBUTE);

        if (claims == null || !"ADMIN".equals(claims.get("role"))) {
            throw new RestApiException(AuthErrorCode.FORBIDDEN);
        }
        return subject;
    }
}
