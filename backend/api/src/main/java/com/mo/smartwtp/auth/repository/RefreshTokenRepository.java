package com.mo.smartwtp.auth.repository;

import com.mo.smartwtp.auth.domain.RefreshToken;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 리프레시 토큰 리포지토리.
 */
public interface RefreshTokenRepository extends JpaRepository<RefreshToken, String> {

    /**
     * 사용자 ID 로 리프레시 토큰을 조회한다.
     *
     * @param userId 사용자 ID
     */
    Optional<RefreshToken> findByUserId(String userId);
}
