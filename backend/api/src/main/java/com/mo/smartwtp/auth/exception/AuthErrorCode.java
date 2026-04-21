package com.mo.smartwtp.auth.exception;

import com.mo.smartwtp.common.exception.ErrorCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 인증 도메인 에러 코드.
 */
@Getter
@RequiredArgsConstructor
public enum AuthErrorCode implements ErrorCode {

    LOGIN_FAILED(401, "사용자 ID 또는 비밀번호가 올바르지 않습니다."),
    FORBIDDEN(403, "접근 권한이 없습니다.");

    private final int httpStatus;
    private final String message;
}
