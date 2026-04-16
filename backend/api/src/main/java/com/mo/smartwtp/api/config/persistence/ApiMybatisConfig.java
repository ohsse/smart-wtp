package com.mo.smartwtp.api.config.persistence;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan(
        basePackages = "com.mo.smartwtp",
        annotationClass = ApiMybatisMapper.class
)
public class ApiMybatisConfig {
}
