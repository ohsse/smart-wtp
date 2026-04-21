package com.mo.smartwtp.user.exception;

import com.mo.smartwtp.common.exception.ErrorCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 사용자 도메인 에러 코드.
 */
@Getter
@RequiredArgsConstructor
public enum UserErrorCode implements ErrorCode {

    USER_NOT_FOUND(404, "존재하지 않는 사용자입니다."),
    DUPLICATE_USER_ID(409, "이미 사용 중인 사용자 ID입니다."),
    INVALID_USER_PW(400, "비밀번호가 올바르지 않습니다."),
    FORBIDDEN_ROLE(403, "해당 작업을 수행할 권한이 없습니다.");

    private final int httpStatus;
    private final String message;
}
