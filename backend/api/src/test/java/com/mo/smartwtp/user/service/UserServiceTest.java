package com.mo.smartwtp.user.service;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;

import com.mo.smartwtp.common.exception.RestApiException;
import com.mo.smartwtp.user.domain.User;
import com.mo.smartwtp.user.domain.UserRole;
import com.mo.smartwtp.user.dto.UserUpsertDto;
import com.mo.smartwtp.user.exception.UserErrorCode;
import com.mo.smartwtp.user.repository.UserRepository;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void 중복_사용자ID_등록_시_예외가_발생한다() {
        UserUpsertDto dto = new UserUpsertDto();
        dto.setUserId("admin");
        dto.setUserNm("관리자");
        dto.setUserPw("password");
        dto.setUserRole(UserRole.ADMIN);

        given(userRepository.existsById("admin")).willReturn(true);

        assertThatThrownBy(() -> userService.registerUser(dto, "system"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.DUPLICATE_USER_ID);
    }

    @Test
    void 신규_사용자_등록_시_비밀번호가_인코딩된다() {
        UserUpsertDto dto = new UserUpsertDto();
        dto.setUserId("user01");
        dto.setUserNm("테스트유저");
        dto.setUserPw("raw-password");
        dto.setUserRole(UserRole.USER);

        given(userRepository.existsById("user01")).willReturn(false);
        given(passwordEncoder.encode("raw-password")).willReturn("$2a$encoded");
        given(userRepository.save(any(User.class))).willAnswer(inv -> inv.getArgument(0));

        userService.registerUser(dto, "system");

        then(passwordEncoder).should().encode("raw-password");
        then(userRepository).should().save(any(User.class));
    }

    @Test
    void 비활성_사용자_조회_시_예외가_발생한다() {
        given(userRepository.findByUserIdAndUseYn("inactive", "Y")).willReturn(Optional.empty());

        assertThatThrownBy(() -> userService.findActiveUser("inactive"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.USER_NOT_FOUND);
    }

    @Test
    void 사용자_비활성화_후_조회하면_예외가_발생한다() {
        User user = User.create("user01", "테스트유저", "$2a$encoded", UserRole.USER, "system");
        given(userRepository.findByUserIdAndUseYn("user01", "Y")).willReturn(Optional.of(user));

        userService.deactivateUser("user01", "admin");

        given(userRepository.findByUserIdAndUseYn("user01", "Y")).willReturn(Optional.empty());

        assertThatThrownBy(() -> userService.findActiveUser("user01"))
                .isInstanceOf(RestApiException.class)
                .extracting(e -> ((RestApiException) e).getErrorCode())
                .isEqualTo(UserErrorCode.USER_NOT_FOUND);
    }
}
