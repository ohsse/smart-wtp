---
status: completed
created: 2026-04-21
updated: 2026-04-21
---

# harness plan 단계 agents 팀 공동 설계 도입 — 태스크

## 관련 계획

- [계획안](../../../plan/20260421/harness_plan_agents/PLAN1.md)

## Phase

### Phase 1: plan.md 핵심 흐름 교체

- [x] `algorithm/.claude/commands/dev/plan.md` — `## 도메인 검토 게이트` 섹션 제거
- [x] `algorithm/.claude/commands/dev/plan.md` — `## 팀 설계 게이트 (Phase A — Medium/Large 필수)` 삽입
- [x] `algorithm/.claude/commands/dev/plan.md` — `## 계획 문서 작성` 앞에 Phase A 결과 분배 안내 문단 추가

### Phase 2: team-lead agent 업데이트

- [x] `algorithm/.claude/agents/wtp-ml-team-lead.md` — `## 표준 작업 단계` 앞에 "PLAN 설계 모드 vs 리뷰 오케스트레이션 모드" 분기 섹션 추가

### Phase 3: 전문가 agents PLAN 기여 템플릿 추가

- [x] `algorithm/.claude/agents/python-ml-expert.md` — `## 출력 형식` 하단에 `## PLAN 기여용 요약 (Phase A 호출 시)` 부록 추가
- [x] `algorithm/.claude/agents/wtp-plant-maintenance-expert.md` — 동일 부록 추가

### Phase 4: CLAUDE.md 참조 추가

- [x] `algorithm/CLAUDE.md` — 규칙 인덱스 테이블에 `wtp-ml-team-lead` 참조 한 줄 추가

### Phase 5: 검증

- [ ] `pms_이관` 슬러그로 `/dev plan` 드라이 런 — Phase A team-lead 호출 확인
- [ ] 스킵 경로 확인 — 단순 수정 슬러그에서 스킵 사유 기재 확인
- [ ] Fix Cycle 경로 확인 — REVIEW1(블로커) 상태에서 Phase A 스킵 확인

## 산출물

- [결과](../../../results/20260421/harness_plan_agents/RESULT1.md)
