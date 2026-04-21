package com.mo.smartwtp.user.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.mo.smartwtp.auth.web.ApiErrorResponseWriter;
import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.user.domain.User;
import com.mo.smartwtp.user.domain.UserRole;
import com.mo.smartwtp.user.dto.UserUpsertDto;
import com.mo.smartwtp.user.exception.UserErrorCode;
import com.mo.smartwtp.user.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.test.annotation.Commit;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

/**
 * UserService 통합 테스트 — 실제 PostgreSQL 연결 사용.
 *
 * <p>WebEnvironment.NONE: 웹 서버 없이 서비스·JPA 레이어만 기동.
 * 각 테스트는 @Transactional로 격리되며 테스트 종료 후 자동 롤백된다.</p>
 *
 * <p>JPA Auditing이 활성화되어 있으며, HTTP 요청 컨텍스트 부재 시
 * {@code ApiAuditorAware}가 {@code "SYSTEM"}을 auditor로 반환한다.</p>
 */
@SpringBootTest(webEnvironment = WebEnvironment.NONE)
@ActiveProfiles("test")
@Transactional
class UserServiceTest {

    /**
     * ApiErrorResponseWriter는 Jackson 2.x ObjectMapper를 주입받으나,
     * Spring Boot 4.0.5는 Jackson 3.x(tools.jackson)를 제공한다.
     * 서비스 테스트에서 불필요한 웹 레이어 빈이므로 mock으로 대체한다.
     */
    @MockitoBean
    private ApiErrorResponseWriter apiErrorResponseWriter;

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository;

    private UserUpsertDto buildDto(String userId, String userNm, String userPw, UserRole role) {
        UserUpsertDto dto = new UserUpsertDto();
        dto.setUserId(userId);
        dto.setUserNm(userNm);
        dto.setUserPw(userPw);
        dto.setUserRole(role);
        return dto;
    }

    @Test
    void 중복_사용자ID_등록_시_예외가_발생한다() {
        userService.registerUser(buildDto("testuser", "테스트유저", "password", UserRole.USER));

        assertThatThrownBy(() -> userService.registerUser(
                buildDto("testuser", "테스트유저2", "password2", UserRole.USER)))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.DUPLICATE_USER_ID);
    }

    @Test
    void 신규_사용자_등록_시_비밀번호가_인코딩된다() {
        userService.registerUser(buildDto("user01", "테스트유저", "raw-password", UserRole.USER));

        User saved = userRepository.findByUserIdAndUseYn("user01", "Y").orElseThrow();
        assertThat(saved.getUserPw()).startsWith("$2a$");
        assertThat(saved.getUserPw()).isNotEqualTo("raw-password");
    }

    @Test
    void 비활성_사용자_조회_시_예외가_발생한다() {
        assertThatThrownBy(() -> userService.findActiveUser("nonexistent"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.USER_NOT_FOUND);
    }

    /**
     * Persistable 구현으로 em.persist() 경로를 따르므로 신규 저장 후 rgstrDtm == updtDtm 이 보장된다.
     * JPA Auditing이 활성화되어 auditor는 "SYSTEM"(요청 컨텍스트 부재 시 fallback)으로 주입된다.
     */
    @Test
    void 신규_사용자_등록_후_감사_필드가_설정된다() {
        userService.registerUser(buildDto("user03", "감사필드유저", "password", UserRole.USER));

        User saved = userRepository.findByUserIdAndUseYn("user03", "Y").orElseThrow();
        assertThat(saved.getRgstrDtm()).isNotNull();
        assertThat(saved.getUpdtDtm()).isNotNull();
        assertThat(saved.getRgstrDtm()).isEqualTo(saved.getUpdtDtm());
        assertThat(saved.getRgstrId()).isEqualTo("SYSTEM");
        assertThat(saved.getUpdtId()).isEqualTo("SYSTEM");
    }

    /**
     * admin 사용자를 실제 DB에 저장하고 커밋한다 — DB 연결 확인용.
     *
     * <p>@Commit으로 트랜잭션을 롤백하지 않아 테스트 종료 후 DB에 레코드가 영속된다.
     * 재실행 시에도 안전하도록 시작 전 기존 admin 레코드를 먼저 제거한다.</p>
     */
    @Test
    @Commit
    void admin_사용자를_실제_DB에_저장한다() {
        userRepository.findById("admin").ifPresent(userRepository::delete);

        userService.registerUser(buildDto("admin", "관리자", "admin", UserRole.ADMIN));

        User saved = userRepository.findByUserIdAndUseYn("admin", "Y").orElseThrow();
        assertThat(saved.getUserId()).isEqualTo("admin");
        assertThat(saved.getUserNm()).isEqualTo("관리자");
        assertThat(saved.getUserRole()).isEqualTo(UserRole.ADMIN);
        assertThat(saved.getUserPw()).startsWith("$2a$");
        assertThat(saved.getUserPw()).isNotEqualTo("admin");
        assertThat(saved.getUseYn()).isEqualTo("Y");
    }

    @Test
    void 사용자_비활성화_후_조회하면_예외가_발생한다() {
        userService.registerUser(buildDto("user02", "테스트유저", "password", UserRole.USER));
        userService.deactivateUser("user02");

        assertThatThrownBy(() -> userService.findActiveUser("user02"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.USER_NOT_FOUND);
    }
}
