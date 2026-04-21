-- 사용자 마스터 테이블
CREATE TABLE IF NOT EXISTS user_m (
    user_id   VARCHAR(50)  NOT NULL,
    user_nm   VARCHAR(100) NOT NULL,
    user_pw   VARCHAR(255) NOT NULL,
    user_role VARCHAR(20)  NOT NULL,
    use_yn    CHAR(1)      NOT NULL DEFAULT 'Y',
    rgstr_id  VARCHAR(50),
    updt_id   VARCHAR(50),
    rgstr_dtm TIMESTAMP    NOT NULL DEFAULT NOW(),
    updt_dtm  TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_user_m PRIMARY KEY (user_id),
    CONSTRAINT ck_user_m_use_yn CHECK (use_yn IN ('Y', 'N')),
    CONSTRAINT ck_user_m_role   CHECK (user_role IN ('ADMIN', 'USER'))
);

COMMENT ON TABLE  user_m           IS '사용자 마스터';
COMMENT ON COLUMN user_m.user_id   IS '사용자 ID';
COMMENT ON COLUMN user_m.user_nm   IS '사용자 이름';
COMMENT ON COLUMN user_m.user_pw   IS 'BCrypt 해시 비밀번호';
COMMENT ON COLUMN user_m.user_role IS '권한 역할 (ADMIN/USER)';
COMMENT ON COLUMN user_m.use_yn    IS '사용 여부 (Y: 활성, N: 비활성)';

-- 초기 관리자 계정 (비밀번호: admin — BCrypt 해시)
INSERT INTO user_m (user_id, user_nm, user_pw, user_role, use_yn, rgstr_id, updt_id)
VALUES (
    'admin',
    '관리자',
    '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Jm3.',
    'ADMIN',
    'Y',
    'system',
    'system'
)
ON CONFLICT (user_id) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_user_m_use_yn ON user_m (use_yn);
