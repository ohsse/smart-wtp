#!/usr/bin/env bash
# Claude Code PostToolUse 훅: ErrorCode 구현 enum의 String 타입 필드 금지
# exit 0 = 허용, exit 2 = 차단 (stderr → Claude 피드백)
#
# 규약: ErrorCode 구현 enum은 httpStatus(int)만 허용한다.
#       message 등 사용자 표기 문자열 필드는 금지.
#       CommonResponseDto에 message 필드가 없으며, RestApiAdvice는 errorCode.name()만 직렬화한다.
#       사용자 표기 문구는 프론트엔드가 errorCode.name()으로 명세 기반 매핑한다.
# 참조: .claude/rules/exception-patterns.md
# 주의: Claude Code 세션 내 Write/Edit 시에만 동작. 터미널/IDE 직접 편집에는 미적용.

set -uo pipefail

input=$(cat)

# ── 파일 경로 추출 ──
file_path=$(echo "$input" | grep -oP '"file_path"\s*:\s*"\K[^"]+' | head -1)
[ -z "$file_path" ] && exit 0

# ── Java 소스 파일이 아니면 통과 ──
[[ "$file_path" != *.java ]] && exit 0

# ── 파일이 존재하지 않으면 통과 ──
[ ! -f "$file_path" ] && exit 0

# ── 대상 조건: *ErrorCode.java이거나 파일 내 implements ErrorCode 포함 ──
is_target=0
[[ "$(basename "$file_path")" == *ErrorCode.java ]] && is_target=1
grep -q "implements ErrorCode" "$file_path" 2>/dev/null && is_target=1
[ "$is_target" -eq 0 ] && exit 0

# ── 위반 검사 ──
violations=()
grep -qP '^\s+private\s+final\s+String\s+\w+' "$file_path" 2>/dev/null \
    && violations+=("String 타입 final 필드 발견 (message, description 등 사용자 표기 문자열 금지)")
grep -qP 'String\s+getMessage\s*\(\s*\)' "$file_path" 2>/dev/null \
    && violations+=("getMessage() 메서드 선언 발견")

[ ${#violations[@]} -eq 0 ] && exit 0

# ── 차단 ──
{
    echo ""
    echo "[ErrorCode 계약 위반] ${file_path}"
    echo ""
    for v in "${violations[@]}"; do
        echo "  위반: $v"
    done
    echo ""
    echo "  규약: ErrorCode 구현 enum은 httpStatus(int)만 허용한다."
    echo "        CommonResponseDto에 message 필드가 없으며 RestApiAdvice는 errorCode.name()만 직렬화한다."
    echo "        사용자 표기 문구는 프론트엔드가 errorCode.name()으로 명세 기반 매핑한다."
    echo ""
    echo "  올바른 예:"
    echo "    PUMP_NOT_FOUND(404),"
    echo "    private final int httpStatus;"
    echo ""
    echo "  참조: .claude/rules/exception-patterns.md"
    echo ""
} >&2
exit 2
