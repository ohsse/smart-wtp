# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 모듈 개요

`predict_flow_pressure` 운영 추론용 Keras 모델을 학습하는 **Attention-LSTM 학습 노트북** 디렉토리.
단일 파일 `At_LSTM_training_GS_1011.ipynb` 로 구성되며, 18개 정수장(Gosan, bd, bw, dy, gb, gg, gg2, hs, is, jh, jj, nw, sc, sj, sl, yb, yj) 태그별 유량·압력 모델을 일괄 학습한다.

상위 레이어 아키텍처(PMS·predict_power 포함)는 `../CLAUDE.md` 참조.

---

## 실행

```bash
jupyter notebook At_LSTM_training_GS_1011.ipynb
```

노트북을 위에서 아래로 모두 실행하면 `__main__` 블록이 `main_full()`을 호출해 학습을 수행한다. 결과 요약은 `./GS_model_result_{yyyymmdd_HHMMSS}.xlsx`로 저장된다.

### 단일 시트만 학습하려는 경우

`main_full()`의 루프 대신 다음 함수를 직접 호출한다:

```python
result = import_train_save_model(
    model_name="Gosan_test",
    sheetname="Gosan",
    mode="BOTH",        # FLUX(유량만) / PRES(압력만) / BOTH
    training=True,      # False → 기존 모델 로드 후 평가만
    save_=True, plot_=True, train_=True, test_=True,
    epoches=1000,
)
```

### 실행 전 반드시 세팅되어야 하는 전역 변수

`main_full()`이 `global`로 초기화하는 값이다. 셀을 개별 실행할 때는 수동으로 먼저 정의해야 한다.

| 전역                   | 기본값                        | 의미                               |
| ---------------------- | ----------------------------- | ---------------------------------- |
| `window_size`          | 60                            | 입력 시퀀스 길이 (분)              |
| `sliding_step`         | 1                             | 슬라이딩 스텝                      |
| `step_topredict_model` | 10                            | 모델 출력 스텝 수                  |
| `step_topredict_user`  | 10                            | 평가·플롯 시 사용할 실제 예측 스텝 |
| `KST`                  | `pytz.timezone('Asia/Seoul')` | 저장 파일명 타임스탬프용           |
| `taglist_name`         | `./GS_taglist_backup.xlsx`    | 태그 정의 엑셀 경로                |

---

## 필요한 외부 입력 파일

노트북 디렉토리 기준 상대경로로 접근하므로, Jupyter 실행 경로(working dir)가 이 폴더여야 한다.

1. **태그 정의**: `./GS_taglist_backup.xlsx`
   - 시트 하나 = 하나의 정수장
   - 첫 번째 시트는 건너뛴다 (`worksheet.sheetnames[1:]`)
   - 필수 컬럼: `태그명`, `변수명`, `태그 설명`, `비고`, `사용`
   - `비고` 값: `NU`(입력 제외), `target`(예측 대상), 그 외(입력 피처)
   - `사용 == 'Y'`인 행만 사용

2. **SCADA 원시 데이터**: `./Rawdata/KSSCADA.{태그명}.F_CV.csv`
   - 시트명이 `Gosan_mini`인 경우에만 `./Rawdata_0815/KSSCADA.*` 경로 사용
   - 포맷: `Datetime, value, value2(optional)` — `value2 == 100`인 행만 유효 처리, 해당 컬럼이 없으면 전체 사용
   - 최초 로딩 후 `./Rawdata/KSSCADA.{sheetname}_{mode}.pkl`에 joblib 캐시. 원본 CSV가 바뀌면 pkl을 삭제해야 재로딩된다.

3. **Gosan_mini 전용 분기**: `mode='FLUX'`·`'PRES'`로 두 번 학습하고 모델명이 `gs_flux_test`, `gs_pres_test`로 고정됨. 그 외 시트는 `mode='BOTH'` 단일 학습.

---

## 출력 아티팩트

동일 디렉토리에 다음 구조로 생성된다. `predict_flow_pressure/` 런타임이 이 구조를 그대로 기대한다.

```
./saved_model/{model_name}.keras
./saved_model/{model_name}.h5             # 호환용 동시 저장
./saved_scaler/{model_name}/{변수명}_scaler.pkl   # 피처별 MinMaxScaler (pickle)
./{model_name}_{yyyy-MM-dd HH:mm}_train.png
./{model_name}_{yyyy-MM-dd HH:mm}_test.png
./GS_model_result_{yyyymmdd_HHMMSS}.xlsx
```

운영 배포 시에는 `saved_model/`·`saved_scaler/` 폴더를 통째로 `../predict_flow_pressure/` 하위의 날짜별 디렉토리(예: `250903/`)에 복사한다.

---

## 모델 아키텍처

`building_model()` 정의 (셀 6):

```
Input (None, n_features)
  → LSTM(64, tanh, return_sequences=True)
  → Dropout(0.2)
  → Self-Attention (Q=K=V=lstm_out)
  → Concatenate([lstm_out, attention])
  → LSTM(32, tanh, return_sequences=True)
  → Dropout(0.2)
  → TimeDistributed(Dense(n_targets))
```

- **Optimizer**: Adam (기본 lr)
- **Loss**: `custom_loss` — 마스킹된 MSE. `y_true`의 마지막 축에 값 `10`이 포함된 스텝은 손실 계산에서 제외한다(패딩 처리용).
- **Batch size**: 256, **validation_split**: 0.1
- **EarlyStopping**: `CustomEarlyStopping` 클래스 — `min_epochs = epoch × 0.4`(기본 400) 지날 때까지는 절대 중단하지 않고, 이후 `patience=20`으로 best weights 복원.

---

## 전처리 핵심 사항 (비자명)

1. **IQR 스케일링**: `IQR_scale()`은 Tukey fence를 ±`2.8×IQR`로 확장 사용(표준 1.5 아님). 데이터 분포 바뀌면 임계 재튜닝 필요.
2. **Gosan 하드코딩 필터**: `preprocessing()` 상단의 `try/except pass` 블록에 Gosan 전용 조건(`Q_GS_NEW < 6000`, `H55_4 > 2.5`, `Q_GS_OLD > Q_GS_NEW` 등)이 하드코딩되어 있다. 다른 정수장에서는 컬럼이 없어 `KeyError`가 발생하며, 의도적으로 `except: pass`로 건너뛰게 설계됨. 새 사이트 추가 시 이 블록 수정 금지, 필요하면 사이트별 분기 추가.
3. **1분 리샘플링 + 선형 보간**: `resample('1min').mean()` → `interpolate('linear')`. 원본 샘플링 주기가 분 단위보다 짧다고 가정한다.
4. **Train/Test 분할**: 시계열 순서를 유지한 8:2. `trainset[:len_train]`, `testset[len_train+1:]`.
5. **Y 패딩**: `window_size != step_topredict_model`인 경우 `to_sequences_y`가 앞쪽을 값 `10`으로 채운다(손실 마스킹과 짝). 값 `10`을 실제 유효 데이터로 쓰면 안 된다.
6. **Pearson 중복 경고**: `del_var=True`이면 상관계수 0.95 초과 쌍을 출력만 한다(실제 컬럼 drop 코드는 주석 처리). 재현/참고 목적 로그일 뿐.

---

## 평가 로직

`evaluation_model_{train,test}()`는 `step_topredict_user`와 `step_topredict_model`의 일치 여부로 슬라이싱이 달라진다.

- `step_topredict_user == step_topredict_model` → 출력 뒤쪽 `step_topredict_model` 스텝 전체 평가
- `step_topredict_user < step_topredict_model` → 뒤에서 `step_topredict_model`부터 `step_topredict_user-1` 스텝까지만 평가

수정 시 인덱싱 끝값(`-step_topredict_model+step_topredict_user-1`)에 오프바이원 주의.

---

## 기술 스택

- Python 3.9+
- TensorFlow/Keras (`LSTM`, `Attention`, `TimeDistributed`)
- PyTorch (import만, 실제 미사용 — 제거 가능)
- scikit-learn (`MinMaxScaler`, `r2_score`)
- pandas, numpy, openpyxl, matplotlib, seaborn, joblib, pickle, pytz

---

## 주의사항

- 노트북은 Jupyter에서 **작업 디렉토리를 이 폴더로** 두고 실행해야 상대경로(`./Rawdata/...`, `./saved_model/...`)가 맞는다. VSCode 등에서 상위 디렉토리로 실행하면 파일을 찾지 못한다.
- 학습된 `.keras` / `.h5`를 로드할 때 반드시 `custom_objects={'custom_loss': custom_loss}`를 지정해야 한다 (`load_trained_model()` 참조).
- `Gosan_mini` 시트는 FLUX/PRES 두 모델을 별도로 생성하지만, 그 외 시트는 `BOTH` 단일 모델이다. 운영 쪽 로더가 모델명·모드 쌍을 어떻게 참조하는지는 `../predict_flow_pressure/main_e_250904.py`에서 확인.
- `main_full()` 내 `model_name`이 `*_test` 접미사로 고정되어 있어, 실운영 배포 전에는 이름을 버전명(`gs_v11` 등)으로 변경해야 기존 파일을 덮어쓰지 않는다.
- 노트북 내부에 주석 처리된 대체 `building_model` 변형(`MultiHeadAttention`, `Bidirectional`, `Dual-Stage Attention`)이 남아 있다. 실험 이력이며 현재 활성 정의는 셀 6의 단일 Self-Attention 버전.
