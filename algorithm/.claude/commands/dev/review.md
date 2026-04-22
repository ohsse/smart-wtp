# 6단계: 코드 리뷰 (REVIEW 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:review pms_이관`" 안내 후 중단
2. RESULT 문서 탐색 (`docs/results/` 하위에서 슬러그 일치):
   - 같은 날짜 디렉토리 내에서 **가장 큰 번호**의 RESULT 문서를 찾는다.
   - RESULT 문서가 없으면 → "결과 문서가 없습니다. `/dev:result $ARGUMENTS`를 먼저 실행하세요." 경고 후 중단
3. 기준 날짜: RESULT 문서의 날짜를 재사용
4. 현재 RESULT 번호가 N이면 REVIEW{N}을 생성한다 (RESULT1→REVIEW1, RESULT2→REVIEW2)
5. `docs/reviews/{날짜}/$ARGUMENTS/` 탐색:
   - 기존 REVIEW 문서가 있으면 내용을 확인하여 블로커 해소 여부 재검토
   - Fix cycle 진행 중이면 "관련 결과"에 이전 REVIEW 링크도 추가

## 코드 리뷰 수행

**`feature-dev:code-reviewer` 서브에이전트를 spawn하여 자동 리뷰를 수행한다.**

서브에이전트에게 다음 컨텍스트를 제공한다:
- 변경된 파일 목록 (`git diff --name-only HEAD`)
- PLAN 문서 경로 및 내용
- RESULT 문서 경로 및 내용
- 프로젝트 규칙 파일 경로:
  - `CLAUDE.md` (5대 리팩토링 원칙, I/O 계약, 보안 규칙)
  - `.claude/rules/module-layout.md`
  - `.claude/rules/io-contract.md`

**리뷰 체크리스트:**

### 5대 원칙 준수 (블로커 수준)
- [ ] **원칙 1 — DB 드라이버 없음**: `alg/` 하위 어느 파일에도 `pymysql`, `sqlalchemy`, `psycopg2`, `pandas.to_sql`, `pandas.read_sql` import 없음
- [ ] **원칙 2 — 스케줄러 없음**: `schedule`, `while True:`, `ThreadPoolExecutor`, `multiprocessing.Pool` 없음
- [ ] **원칙 3 — 파일 I/O**: 결과가 `--output` 경로의 JSON으로 저장됨. stdout은 로그 전용.
- [ ] **원칙 4 — 하드코딩 없음**: `/home/app/`, `C:\`, 사이트 ID 리터럴, 장비 파라미터 상수 없음
- [ ] **원칙 5 — 설정 파일**: 사이트·기기 파라미터가 `--config` JSON에서 읽힘

### I/O 계약 (`.claude/rules/io-contract.md`)
- [ ] `--input`, `--output`, `--config` 세 인자 모두 지원
- [ ] 종료 코드 4종 (`0/1/2/3`) 올바르게 사용
- [ ] stdout = 구조화 로그, stderr = 오류·경고

### 모듈 레이아웃 (`.claude/rules/module-layout.md`)
- [ ] `__main__.py`는 argparse + 호출만 (비즈니스 로직 없음)
- [ ] `cli.py`에서 인자 파싱·검증 담당
- [ ] `core/` 함수는 순수 연산 (부작용 없음)

### 보존 항목 무결성
- [ ] **`custom_loss` 계약**: `y_true == 10` 마스킹 로직이 변경되지 않았는지. 변경 시 `predict_power`, `predict_flow_pressure`, `model_train` 3개 모듈 모두 동일하게 수정되었는지.
- [ ] **모델 트리플 규약**: `saved_model/<name>.keras` ↔ `saved_scaler/<name>/*.pkl` ↔ taglist 경로 규약 유지
- [ ] 신호처리·특징추출·진단 알고리즘 본체가 변경되지 않았는지 (I/O 경계만 교체)

### 코드 품질
- [ ] ruff lint 통과 (`ruff check alg/`)
- [ ] Type hint 적절히 사용
- [ ] `io_contract.py`에서 입력 스키마 검증 수행
- [ ] 민감 정보 하드코딩 없음 (DB 자격증명 등)

### 도메인 정합성
- [ ] 레거시 `legacy/<module>/CLAUDE.md` 기준 누락 기능 없음
- [ ] 진단 튜플 포맷·심각도 임계값이 레거시와 동일하게 유지

## REVIEW 문서 작성

발견 사항을 심각도별로 분류하여 문서를 작성한다:

| 심각도 | 기준 |
|--------|------|
| **높음 (블로커)** | 5대 원칙 위반, 보안 취약점, 명백한 버그, custom_loss 계약 훼손 |
| **중간** | 코드 품질 문제, 가독성 저하, type hint 누락 |
| **낮음** | 개선 제안, 스타일 의견 |

**REVIEW 문서 템플릿** (`.claude/rules/doc-harness.md` 참조):
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 결과
- [결과](../../../results/{YYYYMMDD}/$ARGUMENTS/RESULT1.md)
## 리뷰 범위
## 발견 사항
## 개선 제안
## 결론
```

## 완료 후 안내

리뷰 완료 후:
- **블로커(높음) 발견 시**: `status: draft` 유지
  → "블로커 N건 발견. 수정 사이클을 시작하려면 `/dev $ARGUMENTS`를 실행하세요." 안내
  → (fix cycle을 통해 PLAN{n+1}→TASK{n+1}→impl→RESULT{n+1}→REVIEW{n+1} 전체 흐름 수행)
- **블로커 없음**: `status: approved`로 설정
  → "리뷰 완료, 블로커 없음. `/dev:commit $ARGUMENTS`를 실행하세요." 안내
