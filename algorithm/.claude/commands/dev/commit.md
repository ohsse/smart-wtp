# 7단계: 커밋 (최종 승인 및 Git 반영)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:commit pms_이관`" 안내 후 중단

2. **문서 완전성 검증** — 작업 규모에 따라 필수 문서가 모두 존재하는지 확인한다:

   먼저 `docs/` 하위에서 슬러그 `$ARGUMENTS`와 일치하는 문서들을 탐색한다:
   - `docs/plan/` → PLAN 문서 존재 여부
   - `docs/tasks/` → TASK 문서 존재 여부
   - `docs/results/` → RESULT 문서 존재 여부
   - `docs/reviews/` → REVIEW 문서 존재 여부

   **규모별 필수 문서:**

   | 규모 | PLAN | TASK | RESULT | REVIEW |
   |------|------|------|--------|--------|
   | Small | - | - | - | - |
   | Medium | 필수 | 필수 | - | - |
   | Large | 필수 | 필수 | 필수 | 필수 |

   **규모 판단 기준:**
   - PLAN/TASK 문서가 모두 없으면 → Small
   - PLAN/TASK 문서가 있고 RESULT/REVIEW가 없으면 → Medium
   - RESULT 또는 REVIEW 문서가 있으면 → Large

   **차단 조건 (커밋 진행 불가):**
   - Medium인데 PLAN 문서가 없으면 → 경고 후 중단
   - Medium인데 TASK 문서가 없으면 → 경고 후 중단
   - Large인데 RESULT 문서가 없으면 → 경고 후 중단
   - Large인데 REVIEW 문서가 없거나 `status: approved`가 아니면 → 경고 후 중단

3. REVIEW 문서가 존재하는 경우 추가 검증:
   - `status: approved`가 아닌 경우 → "리뷰에 블로커가 있습니다. `/dev:review $ARGUMENTS`를 확인하세요." 경고

## 미완료 작업 파일 교차 검증

현재 커밋 대상 슬러그(`$ARGUMENTS`) 이외의 TASK 문서 중 `status != completed`인 문서가 있는지 확인한다.

1. `docs/tasks/` 하위의 모든 TASK 문서를 탐색한다.
2. 현재 슬러그(`$ARGUMENTS`)와 경로가 다르고 `status != completed`인 TASK 문서를 찾는다.
3. 해당 문서의 Phase 체크박스에 기록된 파일 경로 목록을 읽는다.
4. `git diff --cached --name-only`로 staged 파일 목록을 획득한다.
5. 교차 비교하여 겹치는 파일이 있으면:
   - 해당 파일을 `git reset HEAD -- <파일>` 로 자동 unstage한다.
   - unstage된 파일 목록을 아래 형식으로 출력한다:

   ```
   [미완료 작업 파일 제외]
   파일                                          미완료 작업
   ----                                          ----------
   algorithm/alg/pms/core/feature_extraction.py  predict_power_io_계약
   ```

6. 남은 staged 파일이 없으면 → "커밋할 파일이 없습니다." 안내 후 중단한다.
7. 남은 staged 파일이 있으면 → 변경된 커밋 범위를 보여주고 계속 진행한다.

## 최종 테스트 실행

커밋 전 최종 검증을 실행한다:
```bash
# 린트
ruff check alg/

# 테스트 (alg/ 디렉토리가 비어 있지 않은 경우)
python -m pytest alg/ -v --tb=short
```

실패 시 → "테스트가 실패했습니다. 구현을 수정한 뒤 다시 시도하세요." 안내 후 중단

## 커밋 준비

다음 정보를 수집하여 커밋 내용을 사용자에게 제시한다:

**변경 사항 확인:**
```bash
git status
git diff --stat HEAD
```

**스테이징 파일 결정:**
- 코드 파일: `alg/` 하위 Python 소스, JSON 스키마, `config/sample.json`
- 문서 파일: `docs/{plan,tasks,results,reviews}/{날짜}/$ARGUMENTS/` 하위 파일
- 설정 파일: `.claude/`, `.gitignore`, `.gitattributes`, `README.md`
- 제외: `.env`, 민감 정보 파일, `__pycache__/`, `.venv/`, IDE 설정 (`.idea/`, `.vscode/`)
- 보존 (커밋 포함): `*.keras`, `*.pkl` (모델 아티팩트, 필요 시만 포함)

**커밋 메시지 초안 작성** (CLAUDE.md 커밋 규칙):
```
{prefix}: {한국어 설명}

예시:
feat: pms 진동 진단 모듈 stateless CLI로 이관
fix: predict_power CLI 입력 스키마 검증 오류 수정
refactor: predict_flow_pressure DB 드라이버 제거 및 파일 I/O 전환
docs: io-contract 규칙에 종료 코드 정의 추가
chore: algorithm 프로젝트 harness 초기 설정
test: pms 스냅샷 테스트 추가
```

접두사 선택 기준:
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 코드 구조 개선
- `docs`: 문서 변경
- `chore`: 빌드/설정 변경
- `test`: 테스트 추가/수정

## ⚠️ 사용자 명시적 승인 필수

다음 내용을 사용자에게 표시하고 **반드시 명시적 승인을 기다린다**:

```
=== 커밋 준비 완료 ===

[스테이징할 파일]
{git diff --stat 출력}

[커밋 메시지]
{초안 메시지}

커밋하려면 "커밋" 또는 "commit"으로 응답하세요.
커밋 메시지를 수정하려면 원하는 메시지를 직접 입력하세요.
```

사용자가 승인하면 커밋을 실행한다. 승인 없이는 절대 커밋하지 않는다.

## 커밋 실행

사용자 승인 후:
```bash
git add {스테이징 파일 목록}
git commit -m "$(cat <<'EOF'
{커밋 메시지}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
git status
```

## PR 생성 여부 확인

커밋 완료 후 PR 생성 여부를 확인한다:
- 필요하면 `gh pr create`로 PR 생성
- PR 제목: 커밋 메시지와 동일 (한국어)
- PR 본문: PLAN/RESULT 문서 링크 포함

커밋/PR 완료 후 → "작업이 완료되었습니다." 안내
