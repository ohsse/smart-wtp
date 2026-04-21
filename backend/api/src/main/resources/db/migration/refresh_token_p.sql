-- 리프레시 토큰 명세 테이블 (1계정 1토큰 정책)
CREATE TABLE IF NOT EXISTS refresh_token_p (
    token_id      VARCHAR(36)  NOT NULL,
    user_id       VARCHAR(50)  NOT NULL,
    token_hash    VARCHAR(64)  NOT NULL,
    expr_dtm      TIMESTAMP    NOT NULL,
    revoke_dtm    TIMESTAMP,
    last_used_dtm TIMESTAMP,
    rgstr_id      VARCHAR(50),
    updt_id       VARCHAR(50),
    rgstr_dtm     TIMESTAMP    NOT NULL DEFAULT NOW(),
    updt_dtm      TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_refresh_token_p         PRIMARY KEY (token_id),
    CONSTRAINT uk_refresh_token_p_user_id UNIQUE (user_id),
    CONSTRAINT fk_refresh_token_p_user_id FOREIGN KEY (user_id) REFERENCES user_m (user_id)
);

COMMENT ON TABLE  refresh_token_p               IS '리프레시 토큰 명세 (1계정 1토큰)';
COMMENT ON COLUMN refresh_token_p.token_id      IS '토큰 식별자 (UUID)';
COMMENT ON COLUMN refresh_token_p.user_id       IS '사용자 ID (user_m.user_id 참조)';
COMMENT ON COLUMN refresh_token_p.token_hash    IS 'SHA-256 해시된 토큰값';
COMMENT ON COLUMN refresh_token_p.expr_dtm      IS '토큰 만료 일시';
COMMENT ON COLUMN refresh_token_p.revoke_dtm    IS '토큰 폐기 일시 (null이면 활성)';
COMMENT ON COLUMN refresh_token_p.last_used_dtm IS '마지막 사용 일시';
COMMENT ON COLUMN refresh_token_p.rgstr_id      IS '등록자 ID';
COMMENT ON COLUMN refresh_token_p.updt_id       IS '수정자 ID';
COMMENT ON COLUMN refresh_token_p.rgstr_dtm     IS '등록 일시';
COMMENT ON COLUMN refresh_token_p.updt_dtm      IS '수정 일시';

CREATE INDEX IF NOT EXISTS idx_refresh_token_p_expr_dtm ON refresh_token_p (expr_dtm);
