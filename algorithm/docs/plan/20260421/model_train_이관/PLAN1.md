---
status: review
created: 2026-04-21
updated: 2026-04-21
---

# legacy/model_train → alg/model_train 이관 계획

## 목적

`legacy/model_train/At_LSTM_training_GS_1011.ipynb` 단일 Jupyter 노트북을 `alg/model_train/` Python 패키지로 재개발하여, Java `backend/scheduler` 가 사이트 단위 단발성 CLI로 호출 가능한 stateless 학습 모듈을 구축한다.

핵심 성과물:
- `python -m alg.model_train --input <manifest>.json --output <result>.json --config <cfg>.json`
- `custom_loss`·`MASK_VALUE=10` 를 `alg/model_train/core/losses.py` 에 단일 정의 — 후속 `predict_flow_pressure`·`predict_power` 이관이 import로 재사용
- 하드코딩된 18개 사이트 루프 제거 → Java가 사이트별 개별 호출

## 배경

레거시 노트북은 5대 리팩토링 원칙 중 3건을 위반한다(DB I/O·스케줄러는 위반 없음):
- **CLI화 위반**: Jupyter 노트북 + `global window_size=60` 등 전역 초기화
- **하드코딩 위반**: 경로(`./Rawdata/`, `./saved_model/`), 사이트 리스트 18개, Gosan 필터 7개, 모델명 접미사 `_test`
- **설정 외부화 위반**: 하이퍼파라미터 21개 이상(window_size, batch_size, epochs, IQR fence, train_ratio 등)

`alg/` 하위 최초 이관 모듈이며, 본 이관에서 공유 계약(`custom_loss`)의 정식 위치를 확정한다.

## 범위

- **포함**: `alg/model_train/` 패키지 신규 생성, CLI 진입점, config 외부화, 선언형 필터 규칙, pytest 도입
- **제외**: `predict_flow_pressure`·`predict_power` 동시 이관 (각 모듈 이관 시 `from alg.model_train.core.losses import custom_loss` 로 전환)
- **제외**: Python 3.9 + numpy 고정핀 레이어 공통 해소 (pms 이관 시 재산정)
- **레거시 `legacy/`**: 수정 금지. 참조 전용.

## 구현 방향

### 아키텍처

Java `ProcessBuilder` → `python -m alg.model_train` (1회 = 1사이트 = 1모델) → `.keras` + `.pkl` + result JSON

`Gosan_mini` (FLUX/PRES 분리): Java가 동일 사이트에 두 번 호출 (`mode: "FLUX"` / `mode: "PRES"` 각각). Python 코드에서 `Gosan_mini` 하드코딩 분기 제거.

### 학습 파이프라인 (이관 함수 매핑)

| 레거시 셀 | 신규 모듈 | 변경 요지 |
|-----------|----------|----------|
| Cell 7 `custom_loss` + `MASK_VALUE=10` | `core/losses.py` | 상수 분리, 3모듈 공유 단일 정의 |
| Cell 5 `to_sequences_x/y` | `core/sequences.py` | `pad_value=MASK_VALUE` 인자화 |
| Cell 3 `IQR_scale()` | `core/scaling.py` | `fence=config["training"]["iqr_fence"]` 주입 |
| Cell 13 `preprocessing()` | `core/preprocessing.py` | 하드코딩 필터 → 선언형 규칙 적용기 (`{column, op, value}`), `except: pass` → `[WARN]` 로그 유지 |
| Cell 11 `import_data()` | `core/data_loader.py` | taglist 경로·사용 컬럼 값 config화, `filter_by_mode()` 분리 |
| Cell 17 `building_model()` | `core/model.py` | 아키텍처 파라미터 config 주입 |
| Cell 21 `CustomEarlyStopping` | `core/callbacks.py` | `min_epoch_ratio`·`patience` 생성자 인자화 |
| Cell 23/25 `save/load_trained_model()` | `core/persistence.py` | 경로 config화, 폴백 실패 시 `sys.exit(3)` |
| Cell 34 `main_full()` | `core/training.py` + `cli.py` | global 제거, 단일 사이트 단발 실행 |

### Attention-LSTM 모델 구조 (변경 없음)

```
Input(None, n_features)
→ LSTM(64, tanh, return_sequences=True) → Dropout(0.2)
→ SelfAttention → Concatenate([lstm_out, attention])
→ LSTM(32, tanh, return_sequences=True) → Dropout(0.2)
→ TimeDistributed(Dense(n_targets))
```

레거시의 MultiHeadAttention·Bidirectional 주석 변형은 이관 대상 제외.

### 선언형 필터 규칙

```json
"site": {
  "filters": [
    {"column": "Q_GS_NEW", "op": "<",  "value": 6000},
    {"column": "H55_4",    "op": ">",  "value": 2.5},
    {"column": "H56_4",    "op": ">",  "value": 2.5},
    {"column": "H59_2",    "op": ">",  "value": 1.9},
    {"column": "Q_GS_OLD", "op": ">",  "value": 14000}
  ]
}
```

op 지원: `<`, `>`, `<=`, `>=`, `==`, `!=` (operator 모듈). 컬럼 미존재 시 `[WARN]` 후 스킵(레거시 try/except 의도 보존).

### 재현성 제약

- IQR_scale → MinMaxScaler.fit 순서 고정 (역전 시 기존 pkl 무효화, docstring 명문화)
- `MASK_VALUE=10` 변경 시 3개 모듈 동시 수정 필수
- TF 핀: `tensorflow>=2.12,<2.16` (`.keras` 포맷 + Keras 2.x import 경로)

## I/O 계약 변경

| 항목 | 변경 전 (레거시) | 변경 후 |
|------|---------------|--------|
| 진입점 | Jupyter 노트북 `Cell 35 __main__` | `python -m alg.model_train --input --output --config` |
| 입력 | `./Rawdata/{tag}.csv` 직접 경로 하드코딩 | `--input <manifest>.json` — raw CSV 디렉토리 + taglist 경로 포함 |
| 출력 | `./GS_model_result_{ts}.xlsx` | `--output <result>.json` — 모델명, val_loss, MAE, R², trained_at, artifact_paths |
| 모델 아티팩트 | `./saved_model/{name}_test.keras` | `config["model"]["model_dir"]/{model_name}.keras` |
| 스케일러 | `./saved_scaler/{name}/` | `config["model"]["scaler_dir"]/{model_name}/` |
| 사이트 반복 | 노트북 내부 18개 루프 | Java가 사이트별 개별 호출 (1실행 = 1사이트) |
| 종료 코드 | 없음 | 0=정상, 1=입력오류, 2=런타임, 3=모델오류 |

### `--input` manifest JSON 구조

```json
{
  "rawdata_dir": "path/to/Rawdata",
  "taglist_path": "path/to/GS_taglist.xlsx",
  "taglist_sheet": "Gosan"
}
```

### `--output` result JSON 구조

```json
{
  "model_name": "gosan_both_20260421",
  "site_id": "Gosan",
  "mode": "BOTH",
  "trained_at": "2026-04-21T09:00:00+09:00",
  "artifact": {
    "model_path": "alg/model_train/saved_model/gosan_both_20260421.keras",
    "scaler_dir":  "alg/model_train/saved_scaler/gosan_both_20260421/"
  },
  "metrics": {
    "val_loss": 0.0032,
    "variables": [
      {"name": "Q_GS_NEW", "train_mae": 0.012, "test_mae": 0.015, "r2": 0.97}
    ]
  },
  "status": "success"
}
```

> `status: "failed"` 인 경우 Java가 재시도 스케줄 결정. `error_message` 필드 포함.

### `--config` JSON 네임스페이스 (신규 확정 섹션)

```json
{
  "runtime": { "log_dir": "C:/logs/alg", "log_level": "INFO" },
  "site": {
    "site_id": "Gosan",
    "mode": "BOTH",
    "timezone": "Asia/Seoul",
    "filters": [...]
  },
  "training": {
    "window_size": 60, "sliding_step": 1,
    "step_topredict_model": 10, "step_topredict_user": 10,
    "iqr_fence": 2.8, "train_ratio": 0.8,
    "val_split": 0.1, "batch_size": 256, "epochs": 1000,
    "early_stopping": { "min_epoch_ratio": 0.4, "patience": 20 },
    "resample_rule": "1min", "interpolate_method": "linear",
    "pearson_threshold": 0.95, "value2_filter": 100
  },
  "model": {
    "model_dir": "alg/model_train/saved_model",
    "scaler_dir": "alg/model_train/saved_scaler",
    "model_name": "gosan_both_20260421",
    "architecture": {
      "lstm1_units": 64, "lstm2_units": 32, "dropout": 0.2
    }
  }
}
```

## 모듈 레이아웃

```
alg/model_train/
  __init__.py
  __main__.py                   # argparse → cli.run(), sys.exit()
  cli.py                        # --input/--output/--config 검증, core 호출
  io_contract.py                # runtime 섹션 공통 검증, input/output 스키마
  core/
    __init__.py
    losses.py                   # custom_loss, MASK_VALUE=10 (3모듈 공유 단일 정의)
    sequences.py                # to_sequences_x/y (pad_value=MASK_VALUE)
    scaling.py                  # IQR_scale (fence 인자화), MinMaxScaler 래퍼
    preprocessing.py            # resample + 선언형 필터 규칙 적용기
    data_loader.py              # taglist xlsx 파싱, filter_by_mode(), CSV 로드
    model.py                    # building_model (Attention-LSTM, 아키텍처 파라미터화)
    callbacks.py                # CustomEarlyStopping (min_epoch_ratio·patience 인자화)
    persistence.py              # save/load_trained_model (.keras→.h5 폴백 + ModelLoadError)
    training.py                 # 단일 사이트 학습 오케스트레이션
  config/
    __init__.py
    loader.py                   # --config JSON 로더·네임스페이스 검증
    sample.json                 # Gosan 1사이트 BOTH 모드 예시
  schemas/
    input.schema.json
    output.schema.json
    config.schema.json
  tests/
    __init__.py
    fixtures/
      mini_raw.csv              # 200행 × 3컬럼 스냅샷
      sample_config.json
      sample_manifest.json
    test_losses.py
    test_sequences.py
    test_scaling.py
    test_preprocessing.py
    test_cli.py
    test_training_smoke.py
  requirements.txt              # tensorflow>=2.12,<2.16; numpy>=1.23,<2.0; ...
```

## 5대 원칙 위반 제거 계획

| 원칙 | 위반 항목 | 제거 조치 |
|------|----------|----------|
| 원칙 1 (DB I/O) | 없음 | — |
| 원칙 2 (스케줄러) | 없음 | — |
| 원칙 3 (CLI화) | Jupyter 노트북 진입점, `global window_size` 초기화 | `__main__.py` + `cli.py` 진입점 신설, global 제거 |
| 원칙 4 (하드코딩) | `./Rawdata/`, `./saved_model/`, 사이트 리스트 18개, Gosan 필터 7개, 모델명 접미사 `_test`, 시트 슬라이스 `[1:]`, `Asia/Seoul` 상수 | config JSON + manifest JSON으로 전환 |
| 원칙 5 (설정 외부화) | window_size=60, batch_size=256, epochs=1000, IQR fence=2.8, train_ratio=0.8, val_split=0.1, patience=20 등 21개 이상 | `config["training"]` 네임스페이스 |

### 주요 블로커 — 구현 전 확인 필요

| 심각도 | 항목 | 확인 방법 |
|--------|------|---------|
| 높음 | taglist xlsx 시트 슬라이스: 노트북 `[1:]` vs predict_flow_pressure CLAUDE.md `[2:]` 불일치 | `GS_taglist_backup.xlsx` 직접 열어 첫 시트 개수 확인 |
| 높음 | `사용` 컬럼 값: 노트북 코드 `'Y'` vs predict_flow_pressure CLAUDE.md `'O'` 불일치 | xlsx 실제 값 확인 |
| 높음 | `except: pass` → `[WARN]` 대체 시 Gosan 필터 컬럼 존재 여부 로그 확인 추가 필수 | — |
| 높음 | pms `numpy==1.20.3` vs model_train `numpy>=1.23` 충돌 — 동일 venv 사용 불가 | Java ProcessBuilder 호출 시 Python 인터프리터 경로 분리 확인 |
| 높음 | `load_trained_model()` `.h5` 폴백 시 `model` 미정의 통과 가능 | alg/ 에서 `ModelLoadError` + `sys.exit(3)` 교체 필수 |

## 보존 항목

| 자산 | 보존 이유 |
|------|----------|
| `custom_loss` 함수 본문·마스킹값 `10` | 3모듈 공유 계약 (predict_flow_pressure·predict_power와 동일) |
| Attention-LSTM 아키텍처 (LSTM→SelfAttention→LSTM→TimeDistributed) | 운영 중인 추론 모듈과 모델 트리플 규약 호환 |
| `.keras → .h5` 폴백 저장 | predict_flow_pressure 로드 쪽이 폴백 구조에 의존 |
| `custom_objects={'custom_loss': custom_loss}` 주입 방식 | Keras 2.x·3.x 동일 API |
| IQR_scale → MinMaxScaler.fit 순서 | 역전 시 기존 pkl 무효화 |
| 모델 트리플 규약: `saved_model/{name}.keras` + `saved_scaler/{name}/{var}_scaler.pkl` + taglist 시트명 | predict_flow_pressure `initialization(model_name=...)` 동시 참조 |
| Y 패딩 앞쪽 `MASK_VALUE` + 유효 뒤쪽 `step_topredict_model`행 구조 | predict_flow_pressure 서빙 슬라이스 `[:, -5, :]` 와 정합 |

## 테스트 전략

### 계층 1 — 결정적 단위 테스트

- `test_losses.py`: `custom_loss` 마스킹/비마스킹 MSE 회귀값 고정 assert
- `test_sequences.py`: output shape, Y 앞쪽 `MASK_VALUE` 채움 assert
- `test_scaling.py`: IQR fence=2.8 아웃라이어 제거 행 수 감소, MinMaxScaler fit 범위 assert

### 계층 2 — 계약 테스트

- `test_cli.py`: 파일 미존재 → exit(1), config 섹션 누락 → exit(1), 모델 로드 실패 → exit(3)
- `test_preprocessing.py`: 선언형 필터 op별 동작, 컬럼 미존재 시 WARN + 스킵 확인

### 계층 3 — Smoke Test (비결정적)

- `test_training_smoke.py`: 200행 × 3컬럼 fixture, epochs=1
- assert: `.keras` 파일 존재, scaler pkl 존재, `val_loss`가 `float` 이고 `nan/inf` 아님
- val_loss 임계값 assert **금지** (1 epoch 결과로 품질 보장 불가)

실행: `python -m pytest alg/model_train/tests/`

## 제외 사항

- `predict_flow_pressure`·`predict_power` 동시 이관 — 각 모듈 이관 PLAN에서 처리
- 결과 xlsx(`GS_model_result_{ts}.xlsx`) — `--output` JSON으로 대체. xlsx 시각화 도구 별도
- `plot_model()` graphviz 의존성 — CI 기본값 `plot_=False`
- `joblib` pkl 캐시 — alg/ 에서는 매번 CSV 재로딩 (캐시 무효화 관리 복잡도 제거). 필요 시 P2 검토

## 예상 산출물

- [태스크](../../../tasks/20260421/model_train_이관/TASK1.md)

## 부록: 팀 설계 결과

- **plant-expert**: 블로커 3건, 권고 2건
  - 블로커: 시트 슬라이스 `[1:]`vs`[2:]` 불일치, `사용` 컬럼 값 `'Y'`vs`'O'` 불일치, `except: pass` 침묵 장애
  - 권고: Gosan FLUX/PRES 두 번 호출 Java scheduler 명시, 학습 실패 사이트별 예외 격리
- **ml-expert**: 블로커 3건, 권고 3건, 미결 3건
  - 블로커: numpy 핀 충돌(독립 venv 필요), load 폴백 미정의 통과, IQR→MinMaxScaler 순서 제약
  - 권고: torch import 제거, MASK_VALUE=10 원시 스케일 확인, off-by-one 보존 주석
  - 미결: pkl 캐시 허용, value2==100 SCADA 플래그 의미, 결과 xlsx 유지 여부
- **미결 사용자 결정 항목**: taglist xlsx `사용` 컬럼 값·시트 슬라이스 인덱스는 구현 단계에서 직접 파일 열어 확인 후 확정
