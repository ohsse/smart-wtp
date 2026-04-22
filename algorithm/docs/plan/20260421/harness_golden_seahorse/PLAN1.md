---
status: approved
created: 2026-04-21
updated: 2026-04-21
---

# algorithm 프로젝트 harness 이식 (Phase 1: 최소 골격)

## 목적

`algorithm` 프로젝트(Python 리팩토링 워크스페이스)에 `backend` 프로젝트의 Claude Code harness를 이식한다. harness 규칙(문서 워크플로, 훅)은 backend 방식을 따르되, 코드 작성·모듈화 규칙은 Python stateless CLI 운영 기준(5대 리팩토링 원칙)으로 재작성한다.

## 배경

- `algorithm`에는 CLAUDE.md 5단 계층과 `.claude/agents/` 4개만 있고, 작업을 구조화할 운영 체계가 없었다.
- `backend`에 이미 검증된 `/dev` 7단계 워크플로·문서 구조·훅이 안착해 있어 동일한 harness를 적용한다.
- 단, `entity-patterns`, `api-patterns`, `ErrorCode 계약` 같은 Java 고유 규칙은 이식하지 않는다.

## 범위 (Phase 1)

최소 골격만 도입. 규칙 확장·5대 원칙 강제 훅·CI는 P2~P4로 연기.

## 구현 방향

### 이식한 것 (backend 원본 → algorithm 재구성)

- `.claude/settings.local.json` — Python 도구(pytest, ruff) allowlist, 훅 1개 바인딩
- `.claude/hooks/check-task-unstage.sh` — TASKS_DIR, full 경로 프리픽스를 `algorithm/`으로 수정
- `.claude/commands/dev.md` + 6서브커맨드 — 워크플로 문법 유지, Java 힌트 → Python 힌트 치환
- `.claude/rules/doc-harness.md` — 경로 리터럴을 `backend/docs/` → `algorithm/docs/`로 수정

### 신규 작성 (algorithm 고유)

- `.claude/rules/module-layout.md` — `alg/<module>/` 표준 레이아웃, 5대 원칙 금지 패턴
- `.claude/rules/io-contract.md` — `--input/--output/--config` 계약, 종료 코드, 로깅 규칙
- `README.md` — 프로젝트 개요, 디렉토리 지도, 실행 예, `/dev` 워크플로 진입 안내
- `.gitignore` — Python 캐시·venv·로그, 모델 아티팩트 보존
- `.gitattributes` — `*.sh text eol=lf`, `*.py text eol=lf`
- `CLAUDE.md` 수정 — "규칙 인덱스" 섹션 추가

## 5대 원칙 위반 제거 계획

Phase 1은 harness 이식이므로 알고리즘 코드 변경 없음. 5대 원칙 위반 제거는 각 모듈 이관 시 수행.

## 보존 항목

- CLAUDE.md 5단 계층 (루트 + legacy/CLAUDE.md + 4개 모듈 CLAUDE.md)
- `.claude/agents/` 4개 (python-ml-expert, wtp-ml-code-reviewer, wtp-ml-team-lead, wtp-plant-maintenance-expert)
- `legacy/` 전체 (수정 금지)

## 테스트 전략

1. 파일 트리 존재성 확인 (`ls` 로 11개 신규 파일 + 4개 `.gitkeep`)
2. 훅 동작: 미완료 TASK → git commit 시 unstage·차단, 완료 TASK → 통과
3. `/dev` 커맨드 인식: Claude Code 세션에서 `/dev plan pms_이관` 실행 확인
4. 규칙 인덱스 링크 유효성 확인

## 제외 사항

- `rules/naming.md`, `config-externalization.md` 등 5개 확장 규칙 (P2)
- `pyproject.toml` (P2, 첫 모듈 이관 시 확정)
- `check-stateless-cli.sh` 등 5대 원칙 강제 훅 (P3)
- `.github/workflows/algorithm-ci.yml` (P4)
- `alg/CLAUDE.md` (첫 모듈 이관 이후 신설)

## 예상 산출물

- `.claude/settings.local.json`
- `.claude/hooks/check-task-unstage.sh`
- `.claude/commands/dev.md` + 6서브커맨드
- `.claude/rules/doc-harness.md`, `module-layout.md`, `io-contract.md`
- `docs/{plan,tasks,results,reviews}/.gitkeep`
- `README.md`, `.gitignore`, `.gitattributes`
- `CLAUDE.md` (규칙 인덱스 추가)
