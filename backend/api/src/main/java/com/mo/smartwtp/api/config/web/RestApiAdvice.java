package com.mo.smartwtp.api.config.web;

import com.mo.smartwtp.common.exception.CommonErrorCode;
import com.mo.smartwtp.common.exception.ErrorCode;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.common.response.CommonResponseDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

@Slf4j
@RestControllerAdvice
public class RestApiAdvice {

    @ExceptionHandler(RestApiException.class)
    public ResponseEntity<CommonResponseDto<Void>> handleRestApiException(RestApiException exception) {
        return buildErrorResponse(exception.getErrorCode(), exception);
    }

    @ExceptionHandler({
            HttpMessageNotReadableException.class,
            MissingServletRequestParameterException.class,
            MethodArgumentTypeMismatchException.class
    })
    public ResponseEntity<CommonResponseDto<Void>> handleBadRequest(Exception exception) {
        return buildErrorResponse(CommonErrorCode.INVALID_REQUEST, exception);
    }

    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<CommonResponseDto<Void>> handleMethodNotAllowed(
            HttpRequestMethodNotSupportedException exception
    ) {
        return buildErrorResponse(CommonErrorCode.METHOD_NOT_ALLOWED, exception);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<CommonResponseDto<Void>> handleException(Exception exception) {
        return buildErrorResponse(CommonErrorCode.INTERNAL_SERVER_ERROR, exception);
    }

    private ResponseEntity<CommonResponseDto<Void>> buildErrorResponse(ErrorCode errorCode, Exception exception) {
        if (errorCode == CommonErrorCode.INTERNAL_SERVER_ERROR) {
            log.error("Unhandled exception", exception);
        } else {
            log.warn("API request failed with code={}", errorCode.name(), exception);
        }

        return ResponseEntity.status(errorCode.getHttpStatus())
                .body(new CommonResponseDto<>(errorCode.name(), null));
    }
}
