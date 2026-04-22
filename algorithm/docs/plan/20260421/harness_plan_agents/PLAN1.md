---
status: approved
created: 2026-04-21
updated: 2026-04-21
---

# harness plan 단계 agents 팀 공동 설계 도입

## 목적

`/dev:plan` 커맨드에 `wtp-ml-team-lead` 주도의 팀 설계 게이트(Phase A)를 도입하여, PLAN 초안을 메인 Claude 혼자 작성하던 방식에서 3-전문가 분업 방식으로 전환한다.

## 배경

- `algorithm` 하네스는 backend 원본(메인 혼자 초안 → 조건부 사후 검토 게이트)을 그대로 이식했다.
- 그러나 algorithm에는 backend에 없는 `wtp-ml-team-lead` (Task 도구, opus-4-7, 오케스트레이터) + 전문가 3명 구조가 있다.
- 실제 모듈 이관(pms/predict_power 등)은 5대 원칙·custom_loss 계약·fs=12800 동시 수정 등 복합 제약이 많아 초기부터 분업이 효율적이다.
- 현재 "도메인 검토 게이트"는 조건이 모호하고 조건부 사후 리뷰에 그쳐, team-lead 존재 의미를 살리지 못한다.

## 범위

- `algorithm/.claude/commands/dev/plan.md` — 핵심 흐름 교체
- `algorithm/.claude/agents/wtp-ml-team-lead.md` — PLAN 설계 모드 추가
- `algorithm/.claude/agents/python-ml-expert.md` — PLAN 기여 템플릿 추가
- `algorithm/.claude/agents/wtp-plant-maintenance-expert.md` — PLAN 기여 템플릿 추가
- `algorithm/CLAUDE.md` — 규칙 인덱스에 참조 한 줄 추가

## 구현 방향

### plan.md 흐름 변경

기존: `초안 작성 → 조건부 검토 게이트`

변경 후:

```
[Phase A] 팀 설계 (Medium/Large 필수)
  메인 Claude: 요청 분해 → team-lead 역할 Agent 호출
    team-lead: plant-expert + ml-expert 병렬/순차 호출 → 통합 결과 반환

[Phase B] PLAN 문서 작성
  메인 Claude: 팀 결과를 PLAN 섹션에 분배 + ## 부록: 팀 설계 결과 첨부 → 사용자 검토
```

- Small: 현행 유지 (PLAN 없이 /dev:impl 직행)
- 팀 설계 스킵 조건: 단순 경로·주석·문서 수정 / Fix Cycle 2회차 이상으로 블로커만 해소하면 충분한 경우 (단, ## 배경에 스킵 사유 명시 필수)

### agents 파일 변경

- `wtp-ml-team-lead.md`: `## 표준 작업 단계` 앞에 "PLAN 설계 모드 vs 리뷰 오케스트레이션 모드" 분기 기술 추가
- `python-ml-expert.md`, `wtp-plant-maintenance-expert.md`: `## 출력 형식` 하단에 `## PLAN 기여용 요약` 부록 추가

## I/O 계약 변경

없음. harness 메타 수준 변경.

## 모듈 레이아웃

없음. `.claude/` 하위 설정·agents 파일만 수정.

## 5대 원칙 위반 제거 계획

없음. harness 메타 수준 변경.

## 보존 항목

- `.claude/agents/wtp-ml-code-reviewer.md` — Phase A 에서 호출하지 않음 (코드 미존재 단계)
- backend 하네스 — 영향 없음
- 기존 `harness_golden_seahorse/PLAN1` approved 상태 — 본 변경은 후속 작업에만 적용

## 테스트 전략

1. `pms_이관` 슬러그로 `/dev plan pms_이관` 드라이 런 → Phase A team-lead 호출 + PLAN1.md 섹션 분배 확인
2. 단순 수정 슬러그로 `/dev plan` → `## 배경` 에 스킵 사유 기재 확인
3. REVIEW1(블로커) 상태에서 `/dev plan` → Fix Cycle 경로에서 Phase A 스킵 확인

## 제외 사항

- `wtp-ml-code-reviewer` PLAN 단계 호출 (코드 없으면 무의미)
- Fix Cycle 3회차 이상 처리 정책 (현 하네스에서 미지원)

## 예상 산출물

- [태스크](../../../tasks/20260421/harness_plan_agents/TASK1.md)
