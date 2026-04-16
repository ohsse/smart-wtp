package com.mo.smartwtp.common.exception;

public interface ErrorCode {

    String name();

    int getHttpStatus();
}
