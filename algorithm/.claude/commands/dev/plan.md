# 2단계: 계획 수립 (PLAN 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증

1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:plan pms_이관`" 안내 후 중단
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

## 계획 문서 작성 (Phase B)

**Phase A 팀 설계 결과를 PLAN 섹션에 분배한 뒤** 빈 섹션만 추가 분석으로 채운다.

**plan 모드**에서 코드베이스를 충분히 분석한 뒤 다음 경로에 문서를 생성한다:

- 경로: `docs/plan/{YYYYMMDD}/$ARGUMENTS/PLAN1.md`
- 기존 문서가 있다면 번호를 증가 (PLAN2.md, PLAN3.md...)

**⚠️ 필수: PLAN 문서는 반드시 `docs/plan/` 경로에 파일로 생성해야 한다.**

plan 모드(Claude의 내장 plan 파일)는 대화 내 임시 작업 도구이다.
`docs/plan/` 경로의 PLAN 문서는 프로젝트에 영구 보존되는 공식 산출물이다.

**작성 전 분석 내용:**

- 영향받는 모듈(`alg/<module>/`) 식별
- 레거시 코드 참조: `legacy/<module>/CLAUDE.md` 에서 도메인 지식·파이프라인 구조 파악
- 유사 구현이 레거시에 이미 존재하는지 확인 (이관 가능한 함수)
- I/O 계약 변경 필요 여부 (`.claude/rules/io-contract.md` 참조)
- 모듈 레이아웃 변경 필요 여부 (`.claude/rules/module-layout.md` 참조)
- **5대 리팩토링 원칙 위반 항목**: 레거시에서 어떤 원칙 위반을 제거해야 하는지 식별
  - 원칙 1: DB 드라이버 (`pymysql`, `sqlalchemy`, `to_sql`)
  - 원칙 2: 스케줄러·루프 (`schedule.every`, `while True:`, `ThreadPoolExecutor`)
  - 원칙 3: I/O 형태 (파일 → JSON/CSV 변환 필요 여부)
  - 원칙 4: 하드코딩 경로·식별자·상수
  - 원칙 5: 코드 내 사이트·기기 파라미터

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

## I/O 계약 변경

<!-- 입출력 스키마·CLI 인자가 바뀌는 경우 작성. io-contract.md 원칙 준수 -->

| 항목 | 변경 전 | 변경 후 |
| ---- | ------- | ------- |

## 모듈 레이아웃

<!-- 신규 파일·디렉토리가 있는 경우 작성. module-layout.md 원칙 준수 -->

## 5대 원칙 위반 제거 계획

<!-- 레거시에서 제거해야 하는 위반 항목 목록 -->

## 보존 항목

<!-- custom_loss, 모델 트리플, 신호처리 알고리즘 등 변경하면 안 되는 것 -->

## 테스트 전략

## 제외 사항

## 예상 산출물

- [태스크](../../../tasks/{YYYYMMDD}/$ARGUMENTS/TASK1.md)
```

**작성 기준:**

- `.claude/rules/module-layout.md` 레이아웃 규칙 준수
- `.claude/rules/io-contract.md` I/O 계약 준수
- 테스트 전략: `python -m pytest alg/<module>/` 범위 명시
- `custom_loss` 변경 시 3개 모듈(`predict_power`, `predict_flow_pressure`, `model_train`) 동시 수정 필요 명시

## 팀 설계 게이트 (Phase A — Medium/Large 필수)

**Small 작업은 이 게이트를 건너뛴다.** PLAN 문서가 없는 Small은 `/dev:impl` 직행.

PLAN 초안 작성에 들어가기 **전**, 아래 절차로 팀 설계를 선행한다.

### Phase A 실행 절차

1. 메인 Claude가 요청을 분해한다:
   - 대상 서브프로젝트 (`pms` / `predict_power` / `predict_flow_pressure` / `model_train`)
   - 영향 모듈·파일 후보
   - 예상 5대 원칙 위반 제거 범위

2. 아래 프롬프트로 team-lead 역할 Agent를 호출한다:

```
Agent(
  subagent_type="general-purpose",
  description="팀 설계: {슬러그} 요청 분해 + 전문가 병렬 수집 + 통합",
  prompt="""
  당신은 .claude/agents/wtp-ml-team-lead.md 역할입니다.
  작업 모드: PLAN 초안 설계 (코드 미존재 단계)

  요청: {요약}
  대상 서브프로젝트: {module}

  다음 절차로 PLAN 초안을 위한 설계 정보를 수집하세요:
  1. wtp-plant-maintenance-expert를 호출하여 도메인 제약·SCADA 규약·알람 규칙·동시 수정 포인트를 파악하세요.
  2. python-ml-expert를 호출하여 모델·손실·MLOps 설계 초안, 5대 원칙 위반 제거 계획을 파악하세요.
  3. 두 결과를 통합하여 아래 형식으로 반환하세요:
     - 접수 요약 (서브프로젝트, 핵심 변경)
     - 도메인 전제 (plant-expert 핵심 발견)
     - ML 설계 초안 (ml-expert 핵심 발견)
     - 통합 블로커(높음) / 권고(중간) / 미결 항목
     - 권장 실행 순서

  ⚠️ wtp-ml-code-reviewer는 이 단계에서 호출하지 마세요 (코드 미존재).
  """
)
```

3. 반환된 통합 결과를 아래 PLAN 섹션에 분배한다:

| team-lead 산출 | PLAN 섹션 |
| --- | --- |
| 접수 요약 | `## 목적`, `## 배경` |
| 도메인 전제 + ML 설계 초안 | `## 구현 방향` |
| 통합 블로커 | `## 5대 원칙 위반 제거 계획` |
| 미결 항목 | `## 제외 사항` 또는 사용자 결정 요청 |
| 권장 실행 순서 | `## 예상 산출물` 순서 |

4. PLAN 문서의 `## 부록: 팀 설계 결과` 섹션에 호출 기록을 첨부한다:

```markdown
## 부록: 팀 설계 결과

- plant-expert: 블로커 N건, 권고 N건 (간략 요약)
- ml-expert: 블로커 N건, 권고 N건 (간략 요약)
- 미결 항목: (사용자 결정 필요 항목 목록 또는 "없음")
```

### 팀 설계 스킵 조건 (명시적 기록 필요)

다음 중 하나이면 Phase A를 건너뛸 수 있다. 반드시 `## 배경`에 스킵 사유를 남긴다:

- 단순 경로·주석·문서 수정 (도메인 로직·I/O 계약 변경 없음)
- Fix Cycle 2회차 이상으로 직전 REVIEW 블로커만 해소하면 충분한 경우

## 검토 요청

문서 작성 완료 후:

1. `status: draft` → `status: review`로 변경
2. 사용자에게 문서 경로와 함께 검토 요청
3. 사용자가 승인하면 `status: review` → `status: approved`로 변경
4. 승인 완료 후 → `/dev:task $ARGUMENTS`를 **자동 실행**한다 (사용자에게 안내만 하지 않고 직접 전이)
