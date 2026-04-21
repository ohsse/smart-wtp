package com.mo.smartwtp.user.service;

import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.user.domain.User;
import com.mo.smartwtp.user.dto.UserUpsertDto;
import com.mo.smartwtp.user.exception.UserErrorCode;
import com.mo.smartwtp.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 사용자 CRUD 서비스.
 */
@Service
@Slf4j
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    /**
     * 활성 사용자를 조회한다.
     *
     * @param userId 사용자 ID
     * @return 활성 사용자 엔티티
     * @throws RestApiException USER_NOT_FOUND — 존재하지 않거나 비활성인 경우
     */
    public User findActiveUser(String userId) {
        return userRepository.findByUserIdAndUseYn(userId, "Y")
                .orElseThrow(() -> new RestApiException(UserErrorCode.USER_NOT_FOUND));
    }

    /**
     * 신규 사용자를 등록한다. 등록자·수정자는 JPA Auditing 이 자동 주입한다.
     *
     * @param dto 등록 요청 DTO
     * @throws RestApiException DUPLICATE_USER_ID — 동일 ID가 이미 존재하는 경우
     */
    @Transactional
    public void registerUser(UserUpsertDto dto) {
        if (userRepository.existsById(dto.getUserId())) {
            throw new RestApiException(UserErrorCode.DUPLICATE_USER_ID);
        }
        String encodedPw = passwordEncoder.encode(dto.getUserPw());
        User user = User.create(dto.getUserId(), dto.getUserNm(), encodedPw, dto.getUserRole());
        userRepository.save(user);
    }

    /**
     * 사용자 정보를 수정한다 (비밀번호 제외). 수정자는 JPA Auditing 이 자동 주입한다.
     *
     * @param userId 수정 대상 사용자 ID
     * @param dto    수정 요청 DTO (null 필드는 유지)
     */
    @Transactional
    public void updateUser(String userId, UserUpsertDto dto) {
        User user = findActiveUser(userId);
        user.changeInfo(dto.getUserNm(), dto.getUserRole());
    }

    /**
     * 사용자를 비활성화(논리 삭제)한다. 수정자는 JPA Auditing 이 자동 주입한다.
     *
     * @param userId 비활성화 대상 사용자 ID
     */
    @Transactional
    public void deactivateUser(String userId) {
        User user = findActiveUser(userId);
        user.deactivate();
    }
}
