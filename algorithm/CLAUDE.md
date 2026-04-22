# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

Smart WTP(상수도 처리 시설) 예지보전·운영 예측을 담당하는 **Python 알고리즘 레이어의 리팩토링 워크스페이스**다.

- `legacy/` — 기존 레거시 코드. 도메인 지식·롤백용 참조 전용. **신규 로직 추가·수정 금지.**
- `alg/` — 리팩토링 타깃 (현재 비어 있음). 레거시 4개 모듈을 1:1로 재개발하는 목적지.

오케스트레이션·DB·스케줄링은 `../backend/scheduler` (Java Spring Batch) 가 전담하고, Python은 **순수 연산(추론·진단) 계층**만 담당한다.

---

## 5대 리팩토링 원칙

이 원칙은 `alg/` 하위 모든 Python 코드에 강제 적용된다. 레거시 어디가 위반이었는지 함께 명시한다.

### 1. DB I/O는 Java에서만

Python 코드에 DB 드라이버를 두지 않는다. `PyMySQL`, `SQLAlchemy`, `pandas.to_sql/read_sql` 의존성 자체를 `alg/` 에서 제거한다.

> 레거시 위반 위치: `pms/util/utils/db.py`의 `DBConnect`, `predict_power/predictpower_Gosan_main.py`의 `open_db()`·`get_db_config()`, `predict_flow_pressure/main_e_250904.py`의 `to_sql(if_exists='append')`.

### 2. 스케줄링도 Java에서

Python 은 **1회 실행 → 결과 파일 저장 → 종료** (stateless CLI) 형태여야 한다. 장기 실행 데몬·루프·스레드풀을 `alg/` 에 두지 않는다.

> 레거시 위반 위치: `pms/main.py`의 `while True:` 폴링 루프, `predict_power`의 `schedule.every(60).minute.do(...)`, `predict_flow_pressure`의 `ThreadPoolExecutor(max_workers=100)` + `schedule.every().minute.do(...)`.

### 3. 입출력은 JSON/CSV 파일

Python은 CLI 인자 또는 환경변수로 **입력 파일 경로**를 받고, 결과를 **JSON/CSV 파일**로 내린다. `stdout`·`stderr`는 로그 전용.

```
python -m alg.<module> --input <from-java>.json --output <to-java>.json --config <cfg>.json
```

> 구체 파일명·스키마 컨벤션은 첫 모듈 이관 시 확정한다(현재 TBD). 결정되면 해당 모듈 CLAUDE.md에 기재.

### 4. 하드코딩 금지

경로 리터럴·사이트 식별자·장비 상수를 소스에 묻지 않는다. 외부화 대상:

| 레거시 하드코딩 예시                             | 대체 방법               |
| ------------------------------------------------ | ----------------------- |
| `/home/app/power/`, `/home/app/pump3/` 배포 경로 | CLI `--input` / env var |
| `fs = 12800` (4개 파일 중복)                     | `--config` JSON 필드    |
| `OPT_IDX = "701-367-FRI:..."` 사이트 리터럴      | `--config` JSON 필드    |
| taglist xlsx 시트명 하드코딩                     | `--config` JSON 필드    |

### 5. 설정 인풋도 파일로

사이트·기기별 파라미터(Pole/RPM/FREQ/BPF, taglist, 임계값, `TB_AL_SETTING` 스냅샷 등) 를 Python 코드 안에 직접 두지 않는다. Java가 JSON/CSV로 직렬화해 `--config <path>` 로 전달하면 Python이 읽는다.

---

## 디렉토리 레이아웃

```
algorithm/
  CLAUDE.md                     ← 이 파일. 리팩토링 원칙·모듈 진입표.
  legacy/                       ← 수정 금지. 도메인 지식·롤백용 참조.
    CLAUDE.md                   ← 레거시 4모듈 공통 아키텍처·DB 테이블·스택
    pms/CLAUDE.md
    predict_power/CLAUDE.md
    predict_flow_pressure/CLAUDE.md
    model_train/CLAUDE.md
  alg/                          ← 신규 타깃 (현재 비어 있음)
    pms/
    predict_power/
    predict_flow_pressure/
    model_train/
```

---

## 4개 모듈

| 모듈                    | 역할                                                            | 레거시 상세                                                                        | 신규 위치                    |
| ----------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------- |
| `pms`                   | 진동·온도 기반 모터/펌프 이상진단 (12,800 Hz 파형, SVM+LR 혼합) | [`legacy/pms/CLAUDE.md`](legacy/pms/CLAUDE.md)                                     | `alg/pms/`                   |
| `predict_power`         | 고산 정수장 1시간 단위 전력 예측 (DLinear Keras)                | [`legacy/predict_power/CLAUDE.md`](legacy/predict_power/CLAUDE.md)                 | `alg/predict_power/`         |
| `predict_flow_pressure` | 18 정수장 유량/압력/수위 예측 + 펌프 조합 추천 (Attention-LSTM) | [`legacy/predict_flow_pressure/CLAUDE.md`](legacy/predict_flow_pressure/CLAUDE.md) | `alg/predict_flow_pressure/` |
| `model_train`           | `predict_flow_pressure` 용 Attention-LSTM 학습 노트북           | [`legacy/model_train/CLAUDE.md`](legacy/model_train/CLAUDE.md)                     | `alg/model_train/`           |

> 도메인 지식(파이프라인 세부, 진단 튜플 포맷, 심각도 임계값, 사이트 변형 파일 정리, 모델 트리플 규약 등)은 각 `legacy/*/CLAUDE.md` 를 그대로 참조한다. 여기서 중복 서술하지 않는다.

---

## Java ↔ Python I/O 계약 — 원칙

| 항목            | 원칙                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------ |
| **호출 방식**   | Java `ProcessBuilder` 로 단발성 Python 프로세스 실행 (stateless CLI)                                               |
| **포맷**        | JSON 우선, 시계열 원시 데이터는 CSV 허용. 바이너리(pkl/keras)는 모델 아티팩트 전용                                 |
| **설정 주입**   | Java가 사이트·기기 파라미터를 JSON으로 직렬화해 `--config <path>` 전달                                             |
| **모델 파일**   | `saved_model/<name>.keras` ↔ `saved_scaler/<name>/*.pkl` ↔ taglist 트리플 규약 유지                                |
| **로깅**        | Python stdout은 구조화 로그(JSON-lines 또는 평문). stderr는 오류·경고 전용. 로그 파일 경로는 Java가 env var로 지정 |
| **DB 책임**     | `backend/scheduler` 가 DB 조회 → 입력 파일 생성 → Python 호출 → 출력 파일 파싱 → DB 적재를 전담                    |
| **스케줄 주기** | `backend/scheduler` 의 `application.yml` + `@Scheduled` 로 관리. Python 쪽에 주기 로직 없음                        |

구체 파일명·경로 컨벤션·JSON 스키마 정의는 **첫 모듈 이관 시 해당 모듈 CLAUDE.md에 확정 기재**한다.

---

## 보존 vs 제거 가이드

| 레거시 자산                                                            | 신규 조치                                                                                                  |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Keras/pkl 모델, scaler                                                 | **보존** — 모델 트리플 규약 그대로 유지                                                                    |
| `custom_loss` (`y_true == 10` 마스킹)                                  | **보존** — `predict_power`·`predict_flow_pressure`·`model_train` 3개 모듈 공유 계약. 변경 시 3곳 동시 수정 |
| 신호처리·특징추출·진단 알고리즘 본체                                   | **보존** (함수 단위 이관) — 비즈니스 로직은 그대로, I/O 경계만 교체                                        |
| DB 폴링 루프·`schedule.every`·`ThreadPoolExecutor`                     | **제거** → Java 스케줄러로 이관                                                                            |
| `open_db()`, `get_db_config()`, `to_sql(if_exists='append')`           | **제거** → JSON/CSV 파일 I/O로 대체                                                                        |
| `/home/app/...` 리눅스 하드코딩 경로                                   | **제거** → 전부 CLI 인자 또는 env var                                                                      |
| `main_2.py`, `main_hy_backup_*`, `*_org`, `main_YYYYMMDD.py` 변형 포크 | **이관 시 취사선택** — `git log` 로 사이트·이슈 확인 후 정식 모듈로 흡수 또는 레거시에 잔류                |
| `requirements.txt` 고정핀 (`numpy==1.20.3` 등 Python 3.9 전용)         | **재검토** — 이관 시 최신 지원 버전으로 재산정                                                             |

---

## 명령어

신규 `alg/` 모듈은 아래 형태를 목표로 한다 (첫 모듈 이관 시 실제 스펙 확정):

```bash
# 신규 alg 모듈 실행 (예시)
python -m alg.pms         --input raw.json   --output result.json --config site.json
python -m alg.predict_power --input raw.csv  --output pred.json   --config site.json

# 백엔드 scheduler 실행 — Python 프로세스를 트리거하는 주체
cd ../backend && ./gradlew.bat :scheduler:bootRun
```

레거시 실행 방법은 각 모듈의 CLAUDE.md를 참조:

- `legacy/pms/CLAUDE.md` → `python main.py` (pms/ 디렉토리에서 실행 필수)
- `legacy/predict_power/CLAUDE.md` → `python predictpower_Gosan_main.py`
- `legacy/predict_flow_pressure/CLAUDE.md` → `python main_e_250904.py`
- `legacy/model_train/CLAUDE.md` → `jupyter notebook At_LSTM_training_GS_1011.ipynb`

신규 `alg/` 에서는 모듈 이관 시 **pytest 기반 스냅샷 테스트** 도입을 권장한다(현재 미확정).

---

## 규칙·컨벤션

- **언어**: 커뮤니케이션·커밋·문서 한국어. 변수명·함수명·파일명은 영어.
- **커밋 스타일**: 백엔드와 동일한 접두 관례 — `feat`·`fix`·`refactor`·`docs`·`chore`·`test`.
- **보안**: Python 쪽은 DB 자격증명을 아예 받지 않도록 설계한다 (원칙 1). 비밀 설정은 소스에 두지 않는다.

---

## 규칙 인덱스

Claude Code 작업 시 참조할 규칙 파일. `.claude/rules/` 에 위치하며 CLAUDE.md와 중복 서술하지 않는다.

| 규칙 파일 | 적용 범위 |
| --------- | --------- |
| [`.claude/rules/doc-harness.md`](.claude/rules/doc-harness.md) | `docs/**` 산출물 생성·상태 전이·Fix Cycle |
| [`.claude/rules/module-layout.md`](.claude/rules/module-layout.md) | `alg/**/*` Python 모듈 구조·금지 패턴 |
| [`.claude/rules/io-contract.md`](.claude/rules/io-contract.md) | `alg/**` CLI 입출력·종료 코드·로깅 |

> **계획 수립(Medium/Large)**: `/dev:plan` 실행 시 `.claude/agents/wtp-ml-team-lead.md` 가 `wtp-plant-maintenance-expert`·`python-ml-expert` 두 전문가를 조율하여 PLAN 초안의 근거를 제공한다. 단순 수정·Fix Cycle은 스킵 가능 (`.claude/commands/dev/plan.md` 팀 설계 스킵 조건 참조).

> P2 도입 예정 규칙: `naming.md`, `config-externalization.md`, `legacy-migration.md`, `test-strategy.md`, `logging.md`

---

## 참조 문서

| 문서                                                               | 용도                                             |
| ------------------------------------------------------------------ | ------------------------------------------------ |
| [`legacy/CLAUDE.md`](legacy/CLAUDE.md)                             | 레거시 4모듈 공통 아키텍처·DB 테이블·기술 스택   |
| `legacy/pms/CLAUDE.md`                                             | PMS 진단 파이프라인·튜플 포맷·SVM/LR 혼합 비율   |
| `legacy/predict_power/CLAUDE.md`                                   | taglist 분류 규칙·`custom_loss`·OPT_IDX 포맷     |
| `legacy/predict_flow_pressure/CLAUDE.md`                           | PRES/FLUX/BOTH mode·β-blending·펌프 조합         |
| `legacy/model_train/CLAUDE.md`                                     | Attention-LSTM 구조·IQR 스케일·산출물 규약       |
| [`../backend/CLAUDE.md`](../backend/CLAUDE.md)                     | Java 백엔드 규칙·멀티모듈 구조                   |
| [`../backend/scheduler/CLAUDE.md`](../backend/scheduler/CLAUDE.md) | Python 오케스트레이션 담당 모듈의 허용·금지 범위 |
