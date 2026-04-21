package com.mo.smartwtp.user.dto;

import com.mo.smartwtp.user.domain.User;
import com.mo.smartwtp.user.domain.UserRole;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.LocalDateTime;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 사용자 조회 응답 DTO.
 *
 * <p>비밀번호 해시를 포함하지 않으며, 웹 계층 응답 전용으로 사용한다.</p>
 */
@Getter
@NoArgsConstructor
@Schema(description = "사용자 조회 응답 DTO")
public class UserDto {

    @Schema(description = "사용자 ID", example = "admin")
    private String userId;

    @Schema(description = "사용자 이름", example = "관리자")
    private String userNm;

    @Schema(description = "권한 역할", example = "ADMIN")
    private UserRole userRole;

    @Schema(description = "사용 여부", example = "Y")
    private String useYn;

    @Schema(description = "등록자 ID", example = "system")
    private String rgstrId;

    @Schema(description = "수정자 ID", example = "system")
    private String updtId;

    @Schema(description = "등록 일시")
    private LocalDateTime rgstrDtm;

    @Schema(description = "수정 일시")
    private LocalDateTime updtDtm;

    private UserDto(User user) {
        this.userId = user.getUserId();
        this.userNm = user.getUserNm();
        this.userRole = user.getUserRole();
        this.useYn = user.getUseYn();
        this.rgstrId = user.getRgstrId();
        this.updtId = user.getUpdtId();
        this.rgstrDtm = user.getRgstrDtm();
        this.updtDtm = user.getUpdtDtm();
    }

    /**
     * User 엔티티로부터 조회 응답 DTO를 생성한다.
     *
     * @param user 사용자 엔티티
     * @return 비밀번호 해시가 제외된 응답 DTO
     */
    public static UserDto from(User user) {
        return new UserDto(user);
    }
}
