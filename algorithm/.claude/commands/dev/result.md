# 5단계: 결과 정리 (RESULT 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증

1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:result pms_이관`" 안내 후 중단
2. TASK 문서 탐색 (`docs/tasks/` 하위에서 슬러그 일치):
   - 같은 날짜 디렉토리 내에서 **가장 큰 번호**의 TASK 문서를 찾는다.
   - TASK 문서가 없거나 `status: completed`가 아니면 → "구현이 완료되지 않았습니다. `/dev:impl $ARGUMENTS`를 먼저 실행하세요." 경고
3. 기준 날짜: PLAN/TASK 문서의 날짜를 재사용
4. 현재 TASK 번호가 N이면 RESULT{N}을 생성한다 (TASK1→RESULT1, TASK2→RESULT2)
5. `docs/results/{날짜}/$ARGUMENTS/` 탐색:
   - RESULT{N} 문서가 이미 있으면 이어서 업데이트할지 확인

## 결과 문서 작성

다음 정보를 수집하여 RESULT 문서를 작성한다:

**변경 사항 수집:**

```bash
git diff --stat HEAD          # 변경된 파일 목록
git diff --name-only HEAD     # 파일 경로 목록
```

**작성 내용:**

- 변경된 파일 목록과 각 파일의 변경 성격 (신규/수정/삭제)
- 추가/변경된 함수·클래스 목록
- 실행한 테스트와 결과 (ruff/pytest 통과 건수)
- CLI 스모크 테스트 결과 (종료 코드 확인)
- 계획 대비 실제 구현의 차이점 (있을 경우)
- 5대 원칙 위반 제거 완료 목록
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

- [계획안](../../../plan/{YYYYMMDD}/$ARGUMENTS/PLAN{N}.md)
- [태스크](../../../tasks/{YYYYMMDD}/$ARGUMENTS/TASK{N}.md)

## 작업 요약

## 변경 사항

## 5대 원칙 위반 제거 결과

## 테스트 결과

## 비고
```

> PLAN{N}/TASK{N}의 N은 현재 fix cycle 번호와 맞춘다. 최초 사이클이면 1, 첫 번째 fix cycle이면 2.

## 완료 후 자동 전이

문서 작성 완료 후:

1. `status: completed`로 설정
2. `/dev:review $ARGUMENTS`를 **자동 실행**한다 (사용자에게 안내만 하지 않고 직접 전이)
