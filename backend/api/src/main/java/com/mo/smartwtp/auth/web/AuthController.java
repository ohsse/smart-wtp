package com.mo.smartwtp.auth.web;

import com.mo.smartwtp.api.config.web.CommonController;
import com.mo.smartwtp.auth.dto.LoginRequestDto;
import com.mo.smartwtp.auth.dto.RefreshRequestDto;
import com.mo.smartwtp.auth.dto.TokenResponseDto;
import com.mo.smartwtp.auth.service.AuthService;
import com.mo.smartwtp.common.exception.JwtErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.response.CommonResponseDto;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 인증 API 컨트롤러.
 *
 * <p>로그인, 토큰 갱신, 로그아웃 엔드포인트를 제공한다.
 * /api/auth/login과 /api/auth/refresh는 JWT 필터 제외 경로로 설정해야 한다.</p>
 */
@Tag(name = "00. 인증")
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController extends CommonController {

    private final AuthService authService;

    @Operation(summary = "로그인 — AT/RT 발급")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "성공"),
            @ApiResponse(responseCode = "400", description = "잘못된 요청"),
            @ApiResponse(responseCode = "401", description = "자격 증명 불일치"),
            @ApiResponse(responseCode = "500", description = "서버 오류")
    })
    @PostMapping("/login")
    public ResponseEntity<CommonResponseDto<TokenResponseDto>> login(
            @Valid @RequestBody LoginRequestDto dto
    ) {
        return getResponseEntity(authService.login(dto.getUserId(), dto.getUserPw()));
    }

    @Operation(summary = "토큰 갱신 — RT 회전 및 새 AT/RT 발급")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "성공"),
            @ApiResponse(responseCode = "400", description = "잘못된 요청"),
            @ApiResponse(responseCode = "401", description = "토큰 만료/불일치"),
            @ApiResponse(responseCode = "500", description = "서버 오류")
    })
    @PostMapping("/refresh")
    public ResponseEntity<CommonResponseDto<TokenResponseDto>> refresh(
            @Valid @RequestBody RefreshRequestDto dto
    ) {
        return getResponseEntity(authService.refresh(dto.getRefreshToken()));
    }

    @Operation(summary = "로그아웃 — RT 폐기")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "성공"),
            @ApiResponse(responseCode = "401", description = "인증 실패"),
            @ApiResponse(responseCode = "500", description = "서버 오류")
    })
    @PostMapping("/logout")
    public ResponseEntity<CommonResponseDto<Void>> logout(HttpServletRequest request) {
        String subject = (String) request.getAttribute(JwtAuthenticationFilter.AUTH_SUBJECT_ATTRIBUTE);
        if (subject == null) {
            throw new RestApiException(JwtErrorCode.MISSING_ACCESS_TOKEN);
        }
        authService.logout(subject);
        return getResponseEntity();
    }
}
