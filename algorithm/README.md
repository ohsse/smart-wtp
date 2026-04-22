# Smart WTP — Algorithm Layer

Smart WTP(상수도 처리 시설) 예지보전·운영 예측을 담당하는 **Python 알고리즘 레이어**다.

Java 백엔드(`../backend/scheduler`)가 DB 조회·스케줄 관리를 전담하고, 이 레이어는 **순수 연산(추론·진단)** 만 수행한다.

---

## 디렉토리 구조

```
algorithm/
  CLAUDE.md                     ← 리팩토링 원칙 · 모듈 진입표
  README.md                     ← 이 파일
  legacy/                       ← 수정 금지. 도메인 지식·롤백용 참조.
    CLAUDE.md
    pms/           predict_power/   predict_flow_pressure/   model_train/
  alg/                          ← 리팩토링 타깃 (모듈별 stateless CLI)
    pms/           predict_power/   predict_flow_pressure/   model_train/
  docs/                         ← 작업 산출물 (plan / tasks / results / reviews)
  .claude/                      ← Claude Code 운영 체계
    agents/  commands/  hooks/  rules/  settings.local.json
```

---

## 4개 모듈

| 모듈 | 역할 | 레거시 참조 | 신규 위치 |
|------|------|------------|----------|
| `pms` | 진동·온도 기반 모터/펌프 이상진단 | `legacy/pms/CLAUDE.md` | `alg/pms/` |
| `predict_power` | 고산 정수장 1시간 단위 전력 예측 | `legacy/predict_power/CLAUDE.md` | `alg/predict_power/` |
| `predict_flow_pressure` | 18 정수장 유량/압력/수위 예측 + 펌프 조합 추천 | `legacy/predict_flow_pressure/CLAUDE.md` | `alg/predict_flow_pressure/` |
| `model_train` | Attention-LSTM 학습 노트북 | `legacy/model_train/CLAUDE.md` | `alg/model_train/` |

---

## 실행 방법

### 신규 `alg/` 모듈 (리팩토링 완료 후)

```bash
python -m alg.pms \
  --input  data/input.json   \
  --output data/result.json  \
  --config config/site.json

python -m alg.predict_power \
  --input  data/raw.csv      \
  --output data/pred.json    \
  --config config/site.json
```

CLI 계약 상세: `.claude/rules/io-contract.md`

### 레거시 (참조·롤백용)

```bash
# pms — pms/ 디렉토리에서 실행 필수
cd legacy/pms && python main.py

# predict_power
cd legacy/predict_power && python predictpower_Gosan_main.py

# predict_flow_pressure
cd legacy/predict_flow_pressure && python main_e_250904.py

# model_train
cd legacy/model_train && jupyter notebook At_LSTM_training_GS_1011.ipynb
```

### 백엔드 스케줄러 (Python 프로세스 트리거 주체)

```bash
cd ../backend && ./gradlew.bat :scheduler:bootRun
```

---

## Java ↔ Python 협업 구조

```
backend/scheduler
  ① DB 조회 → 입력 파일(JSON/CSV) 생성
  ② ProcessBuilder → python -m alg.<module> --input ... --output ... --config ...
  ③ 출력 파일(JSON) 파싱 → DB 적재
```

스케줄 주기·DB 계정은 `backend/scheduler/application.yml`에서 관리. Python 쪽에 주기 로직 없음.

---

## 개발 워크플로

Claude Code에서 `/dev` 슬래시 커맨드로 구조화된 작업을 수행한다.

```
/dev <요청>                  ← 진입점. 규모 분류 + 자동 전이.
/dev:plan <슬러그>           ← PLAN 문서 작성
/dev:task <슬러그>           ← TASK 분해
/dev:impl <슬러그>           ← 구현 + ruff/pytest 검증
/dev:result <슬러그>         ← 결과 정리
/dev:review <슬러그>         ← 코드 리뷰 (5대 원칙 체크리스트)
/dev:commit <슬러그>         ← 커밋 (사용자 명시 승인 필수)
```

상세: `.claude/commands/dev.md`

---

## 규칙 참조

| 규칙 | 적용 범위 |
|------|----------|
| `CLAUDE.md` | 5대 리팩토링 원칙 · I/O 계약 원칙 · 모듈 진입표 |
| `.claude/rules/doc-harness.md` | `docs/**` 산출물 생성·상태 전이 |
| `.claude/rules/module-layout.md` | `alg/**/*` Python 모듈 구조 |
| `.claude/rules/io-contract.md` | `alg/**` CLI 입출력 · 종료 코드 |
| `legacy/*/CLAUDE.md` | 도메인 지식 · 도메인 로직 보존 기준 |
