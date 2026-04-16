# 문서 하네스 규칙

작업 산출물은 `docs/` 하위에 역할/날짜/작업목적 3뎁스 구조로 관리한다.

```
docs/
├── plan/
│   └── {YYYYMMDD}/
│       └── {작업목적}/
│           └── PLAN1.md
├── tasks/
│   └── {YYYYMMDD}/
│       └── {작업목적}/
│           └── TASK1.md
├── results/
│   └── {YYYYMMDD}/
│       └── {작업목적}/
│           └── RESULT1.md
└── reviews/
    └── {YYYYMMDD}/
        └── {작업목적}/
            └── REVIEW1.md
```

## 디렉토리 및 파일 네이밍 규칙

| 뎁스 | 형식 | 예시 |
|------|------|------|
| 1뎁스 | 역할명 | `plan`, `tasks`, `results`, `reviews` |
| 2뎁스 | `YYYYMMDD` | `20260416` |
| 3뎁스 | 작업목적 (스네이크케이스) | `legacy_재개발` |
| 파일명 | `{역할명대문자}{번호}.md` | `PLAN1.md`, `TASK1.md` |

- 동일 작업목적에 문서가 여러 개면 번호를 증가한다. (`PLAN1.md`, `PLAN2.md`)
- 동일 흐름의 문서는 같은 날짜/작업목적 경로를 사용한다.

```
docs/plan/20260416/legacy_재개발/PLAN1.md
docs/tasks/20260416/legacy_재개발/TASK1.md
docs/results/20260416/legacy_재개발/RESULT1.md
docs/reviews/20260416/legacy_재개발/REVIEW1.md
```

## 문서 상태 흐름

모든 문서는 프론트매터로 상태를 관리한다.

```
draft → review → approved → completed
```

| 상태 | 의미 |
|------|------|
| `draft` | 작성 중 |
| `review` | 검토 요청 상태 |
| `approved` | 사용자 승인 완료 (PLAN에서 다음 단계 진입 조건) |
| `completed` | 작업 완료 |

## 수정 사이클 (Fix Cycle)

REVIEW에서 블로커(높음)가 발견되면, **동일 슬러그에 번호를 증가**한 새 문서를 생성하여 fix cycle을 수행한다.

```
1차 사이클: PLAN1 → TASK1 → impl → RESULT1 → REVIEW1 (블로커 발견)
                                                       ↓
2차 사이클: PLAN2 → TASK2 → impl → RESULT2 → REVIEW2 (승인)
```

### 번호 증가 규칙

- 같은 날짜, 같은 슬러그 경로에 번호를 증가하여 생성한다.
- 예: `docs/plan/20260416/p6spy_로깅정책/PLAN2.md`
- PLAN{n}, TASK{n}, RESULT{n}, REVIEW{n}은 같은 fix cycle 번호 `n`으로 대응한다.

### 상호 참조 규칙

fix cycle 문서는 이전 REVIEW를 참조하여 트레이서빌리티를 유지한다.

**PLAN{n}.md 헤더 (n ≥ 2):**
```markdown
## 배경
- [이전 리뷰](../../../reviews/{YYYYMMDD}/{슬러그}/REVIEW{n-1}.md) 블로커 해소
```

**REVIEW{n}.md 헤더 (n ≥ 2):**
```markdown
## 관련 결과
- [결과](../../../results/{YYYYMMDD}/{슬러그}/RESULT{n}.md)
- [이전 리뷰](REVIEW{n-1}.md)
```

## 문서 템플릿

**PLAN{n}.md**
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 목적
## 배경
## 범위
## 구현 방향
## 테스트 전략
## 제외 사항
## 예상 산출물
- [태스크](../../../tasks/YYYYMMDD/작업목적/TASK1.md)
```

**TASK{n}.md**
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 계획
- [계획안](../../../plan/YYYYMMDD/작업목적/PLAN1.md)
## Phase
### Phase 1: {이름}
- [ ] Task 1
- [ ] Task 2
### Phase 2: {이름}
- [ ] Task 1
## 산출물
- [결과](../../../results/YYYYMMDD/작업목적/RESULT1.md)
```

### TASK 체크박스 파일 경로 기록 규칙

pre-commit 훅이 TASK 문서를 파싱하여 파일을 자동 unstage하므로, **정확한 경로 기록이 필수**다.

| 규칙 | 설명 |
|------|------|
| **전체 상대 경로 필수** | 모듈 루트 기준 전체 경로를 백틱으로 감싸 기록한다 |
| **축약 경로 금지** | `common/.../p6spy/...` 형태 금지 |
| **글롭 패턴 금지** | `api/src/main/resources-env/local/*` 형태 금지 |
| **명령어 별도 표기** | `./gradlew.bat ...` 등 실행 명령어는 백틱 경로와 구분되도록 코드블록 또는 일반 텍스트로 기록 |

```markdown
# 올바른 예
- [ ] `common/src/main/java/com/mo/smartwtp/common/p6spy/CustomP6SpySqlFormatter.java` 생성
- [ ] `api/src/main/resources/application.yml` 수정

# 잘못된 예 (훅 파싱 오류 유발)
- [ ] `common/.../p6spy/CustomP6SpySqlFormatter.java` 생성   ← 축약 금지
- [ ] `api/src/main/resources-env/local/*` 설정 추가         ← 글롭 금지
- [ ] `./gradlew.bat clean build` 성공 확인                  ← 명령어 금지
```

명령어 검증 항목은 Phase 내에서 다음과 같이 별도 표기한다:

```markdown
### Phase 5: 빌드 검증
- [ ] `./gradlew.bat clean build` 실행 성공 확인
```

> `./` 로 시작하는 항목은 훅이 자동으로 파일 경로가 아닌 명령어로 인식하여 스킵한다.

**RESULT{n}.md**
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 작업
- [계획안](../../../plan/YYYYMMDD/작업목적/PLAN1.md)
- [태스크](../../../tasks/YYYYMMDD/작업목적/TASK1.md)
## 작업 요약
## 변경 사항
## 테스트 결과
## 비고
```

**REVIEW{n}.md**
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 결과
- [결과](../../../results/YYYYMMDD/작업목적/RESULT1.md)
## 리뷰 범위
## 발견 사항
## 개선 제안
## 결론
```
