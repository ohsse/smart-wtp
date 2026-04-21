package com.mo.smartwtp.user.domain;

import com.mo.smartwtp.common.domain.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 사용자 마스터 엔티티.
 *
 * <p>비밀번호는 BCrypt 인코딩된 값만 저장하며 원본은 저장하지 않는다.
 * 삭제는 {@link #deactivate(String)}을 통한 논리 삭제만 허용한다.</p>
 */
@Entity
@Table(name = "user_m")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class User extends BaseEntity {

    @Id
    @Column(name = "user_id", nullable = false, length = 50)
    private String userId;

    /** 사용자 이름 */
    @Column(name = "user_nm", nullable = false, length = 100)
    private String userNm;

    /** BCrypt 해시 비밀번호 */
    @Column(name = "user_pw", nullable = false, length = 255)
    private String userPw;

    /** 사용자 권한 역할 */
    @Enumerated(EnumType.STRING)
    @Column(name = "user_role", nullable = false, length = 20)
    private UserRole userRole;

    /** 사용 여부 (Y: 활성, N: 비활성) */
    @Column(name = "use_yn", nullable = false, length = 1)
    private String useYn;

    /** 등록자 ID */
    @Column(name = "rgstr_id", length = 50)
    private String rgstrId;

    /** 수정자 ID */
    @Column(name = "updt_id", length = 50)
    private String updtId;

    /**
     * 신규 사용자를 생성한다.
     *
     * @param userId      사용자 ID
     * @param userNm      사용자 이름
     * @param encodedPw   BCrypt 인코딩된 비밀번호
     * @param role        권한 역할
     * @param registrarId 등록자 ID
     */
    public static User create(String userId, String userNm, String encodedPw, UserRole role, String registrarId) {
        return new User(userId, userNm, encodedPw, role, "Y", registrarId, registrarId);
    }

    /**
     * 비밀번호를 변경한다.
     *
     * @param encodedPw 새 BCrypt 인코딩 비밀번호
     * @param updaterId 수정자 ID
     */
    public void changePw(String encodedPw, String updaterId) {
        this.userPw = encodedPw;
        this.updtId = updaterId;
    }

    /**
     * 사용자 기본 정보를 변경한다.
     *
     * @param userNm    변경할 이름 (null이면 유지)
     * @param userRole  변경할 권한 (null이면 유지)
     * @param updaterId 수정자 ID
     */
    public void changeInfo(String userNm, UserRole userRole, String updaterId) {
        if (userNm != null) {
            this.userNm = userNm;
        }
        if (userRole != null) {
            this.userRole = userRole;
        }
        this.updtId = updaterId;
    }

    /**
     * 사용자를 비활성화(논리 삭제)한다.
     *
     * @param updaterId 수정자 ID
     */
    public void deactivate(String updaterId) {
        this.useYn = "N";
        this.updtId = updaterId;
    }
}
