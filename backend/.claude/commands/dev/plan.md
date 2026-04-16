# 2단계: 계획 수립 (PLAN 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:plan jwt_인증_추가`" 안내 후 중단
2. 오늘 날짜를 YYYYMMDD 형식으로 확인
3. `docs/reviews/` 하위에서 슬러그 일치 REVIEW 문서 탐색:
   - 가장 최신 REVIEW가 `status: draft`이고 블로커(높음)가 있으면 → **Fix Cycle 모드**
     - 기존 PLAN 중 가장 큰 번호 N을 파악하고, PLAN{N+1}.md 생성
     - PLAN{N+1}의 "배경" 섹션에 REVIEW{N}의 블로커 항목을 참조
     - 아래 "계획 문서 작성" 단계로 바로 진행
4. `docs/plan/` 하위에서 슬러그 일치 디렉토리 탐색 (Fix Cycle 모드가 아닌 경우):
   - `status: approved` 또는 `status: completed` 문서가 이미 존재하면 → "계획이 이미 승인되었습니다. `/dev:task $ARGUMENTS`를 실행하세요." 안내 후 중단
   - `status: draft` 또는 `status: review` 문서가 존재하면 → 해당 문서를 이어서 작성
   - 다른 날짜 디렉토리에 같은 슬러그의 문서가 있는지도 확인

## 계획 문서 작성

**plan 모드**에서 코드베이스를 충분히 분석한 뒤 다음 경로에 문서를 생성한다:
- 경로: `docs/plan/{YYYYMMDD}/$ARGUMENTS/PLAN1.md`
- 기존 문서가 있다면 번호를 증가 (PLAN2.md, PLAN3.md...)

**⚠️ 필수: PLAN 문서는 반드시 `docs/plan/` 경로에 파일로 생성해야 한다.**

plan 모드(Claude의 내장 plan 파일)는 대화 내 임시 작업 도구이다.
`docs/plan/` 경로의 PLAN 문서는 프로젝트에 영구 보존되는 공식 산출물이다.

- plan 모드를 사용하여 계획을 수립하는 것은 자유이다.
- 그러나 plan 모드의 결과물을 **반드시 `docs/plan/{YYYYMMDD}/$ARGUMENTS/PLAN1.md`에 작성**해야 한다.
- plan 모드 파일에만 내용을 남기고 `docs/plan/` 파일을 생성하지 않으면 **후속 단계에서 차단**된다.

**작성 전 분석 내용:**
- 관련 도메인의 기존 코드 구조 파악 (Controller/Service/Repository/Entity)
- 영향받는 모듈(common/api/scheduler) 식별
- 유사 구현이 이미 존재하는지 확인 (재사용 가능한 코드)
- DB 스키마 변경 필요 여부

**PLAN 문서 템플릿** (`.claude/rules/doc-harness.md` 참조):
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
- [태스크](../../../tasks/{YYYYMMDD}/$ARGUMENTS/TASK1.md)
```

**작성 기준:**
- CLAUDE.md 코딩 규칙 반영 (Java 21, Lombok, SOLID, 패키지 구조)
- `.claude/rules/naming.md` 네이밍 컨벤션 준수
- 테스트 전략: 영향받는 모듈의 `./gradlew.bat :{module}:test` 범위 명시

## 검토 요청

문서 작성 완료 후:
1. `status: draft` → `status: review`로 변경
2. 사용자에게 문서 경로와 함께 검토 요청
3. 사용자가 승인하면 `status: review` → `status: approved`로 변경
4. 승인 완료 후 → `/dev:task $ARGUMENTS`를 **자동 실행**한다 (사용자에게 안내만 하지 않고 직접 전이)
