# 3단계: 작업 분해 (TASK 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:task pms_이관`" 안내 후 중단
2. PLAN 문서 탐색:
   - `docs/plan/` 하위에서 슬러그 `$ARGUMENTS`와 일치하는 디렉토리 탐색 (날짜 불문)
   - 같은 날짜 디렉토리 내에서 **가장 큰 번호**의 PLAN 문서(예: PLAN2.md > PLAN1.md)를 찾아 `status` 확인
   - `status: approved`가 아니면 → "계획이 아직 승인되지 않았습니다. `/dev:plan $ARGUMENTS`를 먼저 실행하고 승인받으세요." 경고 후 중단
3. PLAN 문서의 날짜를 기준 날짜로 사용 (TASK도 동일 날짜 디렉토리에 생성)
4. 현재 PLAN 번호가 N이면 TASK{N}을 생성한다 (PLAN1→TASK1, PLAN2→TASK2)
5. `docs/tasks/{날짜}/$ARGUMENTS/` 디렉토리 탐색:
   - TASK{N} 문서가 이미 있으면 이어서 수정할지 확인

## TASK 문서 작성

PLAN 문서 내용을 읽고 구체적인 Phase/Task 목록으로 분해한다.
- 경로: `docs/tasks/{PLAN날짜}/$ARGUMENTS/TASK1.md`

**분해 기준:**
- Phase는 독립적으로 완료 가능한 작업 단위로 구성
- 각 Task는 단일 파일 또는 단일 함수 수준의 구체적 작업
- 체크박스 형식으로 작성 (`- [ ] Task 설명`)
- 의존 관계가 있는 Task는 같은 Phase에 묶기

**파일 경로 기록 규칙** (`.claude/rules/doc-harness.md` "TASK 체크박스 파일 경로 기록 규칙" 참조):
- 반드시 `alg/<module>/path/to/file.py` 형태의 전체 상대 경로 기록
- 축약·글롭 금지. 명령어(`ruff`, `pytest`)는 코드블록 또는 일반 텍스트로 별도 표기
- pre-commit 훅이 이 경로를 파싱하여 자동 unstage함

**TASK 문서 템플릿** (`.claude/rules/doc-harness.md` 참조):
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 계획
- [계획안](../../../plan/{YYYYMMDD}/$ARGUMENTS/PLAN1.md)
## Phase
### Phase 1: {이름}
- [ ] `alg/<module>/__main__.py` 생성
- [ ] `alg/<module>/cli.py` 생성
### Phase 2: {이름}
- [ ] `alg/<module>/core/diagnosis.py` 이관
## 검증
- [ ] `ruff check alg/<module>/` 실행 성공 확인
- [ ] `python -m pytest alg/<module>/` 실행 성공 확인
## 산출물
- [결과](../../../results/{YYYYMMDD}/$ARGUMENTS/RESULT1.md)
```

## 확인 요청

문서 작성 완료 후:
1. `status: draft` → `status: review`로 변경
2. 사용자에게 Phase/Task 목록 검토 요청
3. 사용자가 확인하면 `status: review` → `status: approved`로 변경
4. 승인 완료 후 → `/dev:impl $ARGUMENTS`를 **자동 실행**한다 (사용자에게 안내만 하지 않고 직접 전이)
