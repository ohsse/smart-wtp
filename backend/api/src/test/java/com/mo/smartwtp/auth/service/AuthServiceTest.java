package com.mo.smartwtp.auth.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyMap;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;

import com.mo.smartwtp.auth.dto.TokenResponseDto;
import com.mo.smartwtp.auth.exception.AuthErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.jwt.JwtToken;
import com.mo.smartwtp.common.jwt.JwtTokenHelper;
import com.mo.smartwtp.common.jwt.JwtTokenInspection;
import com.mo.smartwtp.common.jwt.JwtTokenStatus;
import com.mo.smartwtp.user.domain.User;
import com.mo.smartwtp.user.domain.UserRole;
import com.mo.smartwtp.user.repository.UserRepository;
import java.time.Instant;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenManagementService jwtTokenManagementService;

    @Mock
    private JwtTokenHelper jwtTokenHelper;

    @InjectMocks
    private AuthService authService;

    @Test
    void 로그인_성공_시_토큰이_발급된다() {
        User user = User.create("admin", "관리자", "$2a$encoded", UserRole.ADMIN);
        JwtToken tokenPair = JwtToken.builder().accessToken("at").refreshToken("rt").build();
        Instant now = Instant.now();
        JwtTokenInspection mockInspection =
                new JwtTokenInspection(JwtTokenStatus.VALID, "admin", Map.of("role", "ADMIN"), now, now.plusSeconds(3600));

        given(userRepository.findByUserIdAndUseYn("admin", "Y")).willReturn(Optional.of(user));
        given(passwordEncoder.matches("rawPw", "$2a$encoded")).willReturn(true);
        given(jwtTokenManagementService.issueTokens(anyString(), anyMap())).willReturn(tokenPair);
        given(jwtTokenHelper.inspect("at")).willReturn(mockInspection);
        given(jwtTokenHelper.inspect("rt")).willReturn(mockInspection);

        TokenResponseDto result = authService.login("admin", "rawPw");

        assertThat(result.getAccessToken()).isEqualTo("at");
        assertThat(result.getRole()).isEqualTo(UserRole.ADMIN);
    }

    @Test
    void 존재하지_않는_사용자_로그인_시_LOGIN_FAILED_예외가_발생한다() {
        given(userRepository.findByUserIdAndUseYn("unknown", "Y")).willReturn(Optional.empty());

        assertThatThrownBy(() -> authService.login("unknown", "anyPw"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(AuthErrorCode.LOGIN_FAILED);
    }

    @Test
    void BCrypt_불일치_시_LOGIN_FAILED_예외가_발생한다() {
        User user = User.create("admin", "관리자", "$2a$encoded", UserRole.ADMIN);
        given(userRepository.findByUserIdAndUseYn("admin", "Y")).willReturn(Optional.of(user));
        given(passwordEncoder.matches("wrongPw", "$2a$encoded")).willReturn(false);

        assertThatThrownBy(() -> authService.login("admin", "wrongPw"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(AuthErrorCode.LOGIN_FAILED);
    }

    @Test
    void 비활성_계정_로그인_시_LOGIN_FAILED_예외가_발생한다() {
        // useYn='N' 계정은 findByUserIdAndUseYn("Y")에서 조회되지 않으므로 Optional.empty() 반환
        given(userRepository.findByUserIdAndUseYn("inactive", "Y")).willReturn(Optional.empty());

        assertThatThrownBy(() -> authService.login("inactive", "anyPw"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(AuthErrorCode.LOGIN_FAILED);
    }

    @Test
    void 로그아웃_시_리프레시_토큰이_폐기된다() {
        authService.logout("admin");
        then(jwtTokenManagementService).should().revokeRefreshToken("admin");
    }
}
