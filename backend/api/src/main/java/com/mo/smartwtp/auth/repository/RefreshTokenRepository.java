package com.mo.smartwtp.auth.repository;

import com.mo.smartwtp.auth.domain.RefreshToken;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RefreshTokenRepository extends JpaRepository<RefreshToken, String> {

    Optional<RefreshToken> findBySubject(String subject);
}
