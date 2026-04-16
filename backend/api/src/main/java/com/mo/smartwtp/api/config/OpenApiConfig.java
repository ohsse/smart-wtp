package com.mo.smartwtp.api.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "Smart WTP API",
                description = "smart-wtp API Swagger specification",
                version = "v1",
                contact = @Contact(name = "smart-wtp backend"),
                license = @License(name = "Proprietary")
        )
)
public class OpenApiConfig {
}
