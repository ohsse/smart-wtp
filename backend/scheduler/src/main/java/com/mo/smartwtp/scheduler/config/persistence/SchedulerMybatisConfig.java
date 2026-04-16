package com.mo.smartwtp.scheduler.config.persistence;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan(
        basePackages = "com.mo.smartwtp",
        annotationClass = SchedulerMybatisMapper.class
)
public class SchedulerMybatisConfig {
}
