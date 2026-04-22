# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 모듈 개요

고산(Gosan) 정수장의 **1시간 단위 전력 사용량 예측** 레거시 알고리즘.
DLinear 기반 Keras 모델을 1시간마다 재실행하여 향후 24시간 전력(`Power_tot`)을 예측하고
결과를 EMS DB의 `TB_CTR_OPT_RST`에 적재한다.

상위 레이어 설명(PMS·predict_flow_pressure 포함)은 `../CLAUDE.md` 참고.

---

## 실행 명령어

```bash
# 운영 스케줄러 (60분 주기 예측 루프)
python predictpower_Gosan_main.py

# 과거 구간 일괄 백필 (코드 상 시작·종료 시각을 직접 편집한 뒤 실행)
python main_gs_range.py
```

실행 전제:
- `/home/app/power/Gosan_taglist.xlsx`
- `/home/app/power/saved_model/<model_name>.keras` (실패 시 `.h5` 폴백)
- `/home/app/power/saved_scaler/<model_name>/*_scaler.pkl` (`Power_tot_scaler.pkl` + 변수별 스케일러)
- `/home/app/connections.json` — `maria-ems-db-gs` 키에 PyMySQL 접속 인자
- Python 3.9+, TensorFlow/Keras, pandas, pymysql, sqlalchemy, schedule, pytz, openpyxl

레포에 requirements가 없으므로 배포 서버의 기존 Python 환경에 맞춰 패키지를 맞춘다.

---

## 실행 파이프라인 (`predictpower_Gosan_main.py`)

```
60분 schedule tick
  ↓
Predict_func → Predict(model_name, window_size)
  ↓
initialization() : taglist.xlsx 로드 + Keras 모델 + 스케일러들(Power_tot + variable별) 로드
  ↓
open_db() : connections.json의 maria-ems-db-gs로 PyMySQL 연결
  ↓
각 태그별 get_db_df() : TB_RAWDATA에서 최근 5일 이내 window_size*60 포인트 조회
  ↓
변수명 접두사 'Power' → data_target / 나머지 → data_var 로 분기
  ↓
clean_and_convert → Power_tot = 타겟 합산 → resampling('1H','mean')
  ↓
cal_time() : hours_sin / hours_cos 추가 → 마지막 window_size 시점 슬라이스
  ↓
Power_tot 스케일 변환 → model.predict (실패 시 np.expand_dims로 배치 차원 추가 후 재시도)
  ↓
testPredict[:, -step_topredict:, :] → Power_tot_scaler.inverse_transform → RELU
  ↓
create_tnk_df() : SQLAlchemy engine 통해 TB_CTR_OPT_RST에 append
```

---

## 핵심 설계 결정 (비자명 사항)

### taglist.xlsx의 `비고` 열이 변수 분류 기준

- `비고 == 'NU'` → 사용하지 않음(제외).
- `비고 == 'variable'` → 외생 변수(`df_variable`), 각각 스케일러 파일이 존재해야 한다.
- 나머지 + 변수명이 `Power`로 시작 → 타겟 채널로 합산되어 `Power_tot`이 된다.
  → 새 태그 추가 시 **스케일러 pkl과 엑셀 비고 값을 함께 갱신**해야 한다.

### 윈도우·스텝 상수

- `window_size = 120` (시간) : 모델 입력 시퀀스 길이.
- `step_topredict = 24` (시간) : 모델 출력 중 최근 24스텝만 사용.
- DB 조회는 `window_size * 60` rows(분 단위 원시 데이터 가정) 후 `1H` 리샘플링으로 윈도우를 맞춘다.
  샘플링 주기가 다른 사이트에 이식하려면 `get_db_df`의 `LIMIT`과 리샘플링 규칙을 동시에 수정해야 한다.

### DB 설정이 두 경로로 분리

- 조회 연결: `open_db()` — `/home/app/connections.json`의 `maria-ems-db-gs`.
- 결과 쓰기 연결: 모듈 하단 `get_db_config()` + SQLAlchemy `engine` (호스트 하드코딩 `10.103.11.112`).
  읽기와 쓰기가 서로 다른 DB를 가리킬 수 있으니 환경 이전 시 두 곳을 모두 점검한다.
  (`main_gs_range.py`에는 `# 188서버로 수정해야함` 주석이 남아 있음 — 환경 이전 흔적.)

### `custom_loss` 계약

학습 시 `y_true == 10`을 "모든 차원이 10이면 해당 스텝 마스킹"으로 사용한다.
`load_model(..., custom_objects={'custom_loss': custom_loss})`에 이 함수가 반드시 주입돼야 하므로
로딩 경로에서 함수 시그니처를 임의로 변경하면 모델 로딩이 실패한다.

### `.keras` → `.h5` 폴백

TF 버전 불일치로 `.keras` 로드가 실패하면 자동으로 `.h5`로 재시도한다.
예외가 `print`로만 처리되고 `model` 변수가 정의되지 않은 채 통과할 수 있으므로,
모델 로딩 실패 시 `Predict` 초반에 `NameError`로 드러난다 — 로그를 보면 바로 원인 구분 가능.

### `model.predict` 입력 shape try/except

타겟+변수 결합 결과에 따라 입력이 2D / 3D로 갈라지므로, 첫 시도가 실패하면
`np.expand_dims(..., axis=0)`로 배치 차원을 추가한 뒤 재시도한다. 의도된 이중 경로이므로
예외 제거 시 shape 계약을 모델과 함께 재정렬해야 한다.

### `Power_tot`만 역변환

변수(variable) 채널은 모델 입력에만 쓰이고, 예측 역변환은 `Power_tot_scaler`만 사용한다.
출력 컬럼을 늘리려면 스케일러 dict에 대응하는 키가 있어야 한다.

### `OPT_IDX` 포맷

`create_tnk_df`는 고정 prefix `"701-367-FRI:"` + `YYYYMMDDHH-HHMM` 형태로 인덱스를 만든다.
`701-367-FRI`는 고산 사이트 고정 태그이므로 **사이트 이식 시 필수 수정 포인트**.

### `main_gs_range.py` 특이사항

- 상단의 날짜 리터럴(`2024-08-05 ~ 2024-08-07 17:00`)을 직접 편집해 백필 범위를 결정한다.
- 파일 말미에 `Predict_func(...)`가 **두 번** 호출되고 이어서 `schedule.run_pending()` 루프가 존재한다.
  (레거시 코드의 미정리 흔적으로 보임. 실사용 시 의도 확인 필요.)

---

## 산출물 스키마 (`TB_CTR_OPT_RST`)

`create_tnk_df`가 매 컬럼마다 다음 필드로 행을 `append`한다:

| 필드 | 값 |
| --- | --- |
| `RGSTR_TIME` | 저장 시각 (`datetime.now()`) |
| `PRDCT_TIME` | 예측 대상 시각 |
| `PRDCT_TIME_DIFF` | 1…24 (시간 차) |
| `PRDCT_MEAN` / `PRDCT_STD` / `TUBE_PRSR_PRDCT` / `PUMP_GRP` | 모두 0 (미사용, 스키마 자리채움) |
| `PWR_PRDCT` | RELU 적용된 역스케일 예측치 |
| `ANLY_TIME` | 분석 시각 |
| `OPT_IDX` | `701-367-FRI:YYYYMMDDHH-HHMM` |

`if_exists='append'` 모드이므로 중복 방지 로직이 없다. 재실행 시 중복 적재 주의.

---

## 주의사항

- 파일 경로는 전부 리눅스 하드코딩(`/home/app/power/...`). Windows 개발 환경에서 그대로 실행하면 실패한다.
  로컬 검증 시에는 경로 상수를 환경변수/config로 빼는 패치가 필요하다.
- `custom_loss` 내부는 `y_true == 10`을 "무효 스텝" 표식으로 쓴다. 학습 데이터 스케일이 10에 근접하면 오탐이 발생할 수 있다.
- `cal_time`은 `data_df.index.hour`를 쓰므로 인덱스가 `DatetimeIndex`가 아니면 조용히 실패한다.
  `resampling`이 빈 데이터를 반환하면 이 지점에서 `AttributeError`가 올라온다.
- `data_var`가 비어 있어도 `try/except`로 `target_resampled`만 사용하는 경로가 있으므로,
  변수 채널이 모두 비어 있을 때 모델 입력 차원이 줄어 모델 shape 불일치가 발생할 수 있다.
- `Gosan_taglist.xlsx`는 레포 루트에 있으나 운영에서는 `/home/app/power/`의 사본을 읽는다 — 레포 파일 수정만으로는 반영되지 않는다.
