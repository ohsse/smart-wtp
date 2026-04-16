# 5단계: 결과 정리 (RESULT 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:result jwt_인증_추가`" 안내 후 중단
2. TASK 문서 탐색 (`docs/tasks/` 하위에서 슬러그 일치):
   - TASK 문서가 없거나 `status: completed`가 아니면 → "구현이 완료되지 않았습니다. `/dev:impl $ARGUMENTS`를 먼저 실행하세요." 경고
3. 기준 날짜: PLAN/TASK 문서의 날짜를 재사용
4. `docs/results/{날짜}/$ARGUMENTS/` 탐색:
   - 기존 RESULT 문서가 있으면 이어서 업데이트할지 확인

## 결과 문서 작성

다음 정보를 수집하여 RESULT 문서를 작성한다:

**변경 사항 수집:**
```bash
git diff --stat HEAD          # 변경된 파일 목록
git diff --name-only HEAD     # 파일 경로 목록
```

**작성 내용:**
- 변경된 파일 목록과 각 파일의 변경 성격 (신규/수정/삭제)
- 추가/변경된 클래스, 메서드, 엔티티 목록
- 실행한 테스트와 결과 (통과/실패 건수)
- 계획 대비 실제 구현의 차이점 (있을 경우)
- 특이 사항, 기술 부채, 후속 작업 필요 항목

**RESULT 문서 템플릿** (`.claude/rules/doc-harness.md` 참조):
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 작업
- [계획안](../../../plan/{YYYYMMDD}/$ARGUMENTS/PLAN1.md)
- [태스크](../../../tasks/{YYYYMMDD}/$ARGUMENTS/TASK1.md)
## 작업 요약
## 변경 사항
## 테스트 결과
## 비고
```

## 완료 후 자동 전이

문서 작성 완료 후:
1. `status: completed`로 설정
2. `/dev:review $ARGUMENTS`를 **자동 실행**한다 (사용자에게 안내만 하지 않고 직접 전이)
