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

    LOGIN_FAILED(401),
    FORBIDDEN(403);

    private final int httpStatus;
}
