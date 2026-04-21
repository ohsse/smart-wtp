package com.mo.smartwtp.user.repository;

import com.mo.smartwtp.user.domain.User;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 사용자 JPA 리포지토리.
 */
public interface UserRepository extends JpaRepository<User, String> {

    /**
     * 사용자 ID와 사용 여부로 사용자를 조회한다.
     */
    Optional<User> findByUserIdAndUseYn(String userId, String useYn);
}
