# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 상위 레거시 알고리즘 레이어 전반에 대한 설명은 `../CLAUDE.md` 참조.
> 이 문서는 **`predict_flow_pressure`** 모듈 전용 지침만 다룬다.

---

## 모듈 개요

고산(Gosan) 정수장과 그에 속한 배수지(sub-distribution)들의 **유량(Q) / 압력(P) / 수위(H)** 를
1분 간격으로 5분(또는 10분) 앞 예측하고, 예측 결과를 기반으로 펌프 운전조합을 추천하여
MariaDB `EMS_DB` 테이블에 적재하는 단일 프로세스.

구조는 다음 한 파일이 전부다:

- `main_e_250904.py` — 스케줄러, DB I/O, 전처리, 추론, 펌프조합 로직을 모두 포함한 단일 엔트리포인트.

Keras 모델과 MinMaxScaler는 외부 파일로 분리되어 있다:

- `saved_model/250903/<site>_250904.keras` (우선) 또는 `.h5` (폴백)
- `saved_scaler/250903/<site>_250904/<feature>_scaler.pkl`

`GS_taglist_250904.xlsx` — 사이트별(시트별) 입력 태그 정의서.
각 시트는 `사용`, `비고`(`target`/`NU`), `변수명`, `태그명`, `태그 설명` 컬럼을 가진다.
변수명 **첫 글자**로 종류를 구분한다: `P*` 압력, `Q*` 유량, `H*` 수위.

---

## 실행

```bash
# 의존 패키지는 상위 CLAUDE.md 참조 (keras/tensorflow, pymysql, sqlalchemy, openpyxl, schedule, pytz, numpy, pandas)

# 운영 실행 (배포 환경 기준 경로 하드코딩되어 있음)
python main_e_250904.py
```

실행 전 준비되어야 하는 런타임 리소스(코드 내 하드코딩 경로):

| 경로 | 용도 |
|------|------|
| `/home/app/pump3/GS_taglist.xlsx` | `initialization()` 이 읽는 태그 정의서 |
| `/home/app/pump3/saved_model/250903/` | Keras `.keras` / `.h5` 모델 |
| `/home/app/pump3/saved_scaler/250903/<site>/` | 변수별 MinMaxScaler `.pkl` |
| `./libs/connections.json` | `open_db()` 가 읽는 조회용 DB 접속정보 (`maria-ems-db-dev` 키) |
| `./log/log.txt` | RotatingFileHandler 로그 출력 (5MB × 3 백업) |

> `get_db_config()` 의 업로드용 DB 접속정보는 **소스에 하드코딩** 되어 있다 (`10.103.11.112 / ems_user / ems2023 / EMS_DB`).
> 사이트 이관 시 `get_db_config()`, `open_db()`, `initialization()`, `taglist_name` 경로를 전부 수정해야 한다.

파일 하단의 `while True: schedule.run_pending()` 루프는 **주석 처리** 되어 있다.
실사용 시 이 루프를 활성화하거나, 외부 크론/systemd에서 주기 실행해야 한다.

---

## 핵심 설계 결정 (비자명 사항)

### 1. 사이트 = 모델 + scaler + xlsx 시트 트리플

`initialization(sheetname, model_name, mode)` 은 동일한 `model_name` 으로
모델 파일(`<model_name>.keras`), scaler 디렉터리(`<model_name>/`), xlsx 시트(`sheetname`)를 동시에 찾는다.

예: `Gosan` 시트 + `Gosan_250904.keras` + `saved_scaler/.../Gosan_250904/` 세트.

신규 사이트 추가 시 이 세 가지를 **동일 이름**으로 맞춰야 한다.
현재 `pred_and_upload_gs_test()` 는 `model_name='Gosan_test_ss_XGBoost'` 로 호출하지만
실제 디렉터리에는 `Gosan_250904` 만 존재한다 — **운영 배포 시 이름 정합을 반드시 확인**해야 한다.

### 2. mode 플래그로 태그 필터링

`initialization()` 의 `mode` 는 xlsx 시트에서 사용할 변수를 거른다:

| mode | 필터 |
|------|------|
| `PRES` | 변수명이 `P`로 시작 (압력) |
| `FLUX` | 변수명이 `P`로 시작하지 **않음** (유량·수위 포함) |
| `BOTH` | 전체 사용 변수 |

Gosan 정수장은 PRES/FLUX를 **따로 두 번** 추론하고(`pred_and_upload_gs_test`),
하위 배수지는 `BOTH` 한 번으로 처리(`predict_and_upload_flux_test`).

### 3. H 변수(수위) 합산 규칙

`H1_1`, `H1_2`, `H1_3` 처럼 접두(`_` 앞 토큰)가 같은 H 변수가 여러 개이면
`initialization()` 과 `Predict_5min_test()` 양쪽에서 `sum()` 으로 접두명(`H1`)으로 합치고 원본을 버린다.
**두 함수가 동일 로직을 중복 구현**하므로 규칙 변경 시 양쪽 모두 수정해야 한다.
scaler 파일명도 합쳐진 접두명(예: `H20_1_scaler.pkl`)을 따른다.

### 4. 시계열 입력 포맷

- DB 조회: `TB_RAWDATA` 에서 태그별로 `test_timestamp` 이전 **1440건** 을 역순 조회 (24시간 ≒ 1분 단위)
- 전처리: `resample('10min', origin='end').mean()` — 종료점 기준 10분 평균
- 모델 입력: `np.expand_dims(array, axis=0)` 으로 배치 차원 추가한 `(1, T, F)` 형태
- 모델 출력: `testPredict[:, -5, :]` — 시퀀스 출력 중 **끝에서 5번째 타임스텝**을 "1분 뒤 예측" 으로 사용

> 주석에 `5분 앞 예측` 과 `1분 뒤 예측` 이 섞여 있다. 실제 사용 포인트는 `-5` 인덱스이므로,
> 학습 시 정의한 출력 시퀀스 구조와 반드시 일치해야 한다. 모델을 교체할 때 `[:, -5, :]` 슬라이스도 재검토.

### 5. 사용자 정의 loss

`custom_loss` 는 `y_true == 10` 을 마스킹값으로 보고 제외한 masked MSE.
학습/서빙 양쪽에서 동일 정의가 필요하므로 `load_model(..., custom_objects={'custom_loss': custom_loss})` 로 주입.
RELU 후처리로 예측 음수는 0으로 절삭한다.

### 6. Gosan 실측 보정 (β-blending)

`pred_and_upload_gs_test()` 는 예측값을 마지막 실측치(`cur_flux`, `cur_pres`)와 섞어 최종 결과를 만든다:

```
β = mean(|predict − actual| / actual)     # 변수별 상대오차
β > 0.2  →  result = (1−β)·predict + β·actual   # 실측 가중치 ↑ (보수적)
β ≤ 0.2  →  result = 0.8·predict + 0.2·actual    # 예측 우선
```

β 임계 0.2 와 기본 0.8/0.2 블렌드는 실험적으로 정한 값. 모델 성능이 바뀌면 재튜닝 대상.

### 7. 펌프 운전조합 결정 (OLD / NEW)

`pred_pump()` 는 예측된 Q, P 를 Q–P 평면의 **다항식 경계**와 비교해
사전 정의된 7개(OLD) 또는 4개(NEW) 조합 중 하나를 선택한다.

- OLD 모드: 7대 펌프 → 7개 구간의 불연속 조합 (`[0,1,0,1,0,1,1]` 등)
- NEW 모드: 4대 펌프 → 현재는 `[0,0,1,0]` 고정

경계식 계수는 **소스에 하드코딩**되어 있다. 펌프 교체·수리 시 이 계수를 직접 수정해야 한다.

### 8. 업로드 테이블

- `EMS_DB.TB_CTR_TNK_RST` — 탱크/배수지 예측값 (`DSTRB_ID`, `PRDCT_VALUE`, `RGSTR_TIME`) — `create_tnk_df()` 가 append
- 펌프 DataFrame(`create_pump_df`)은 현재 코드에서 **리스트에만 적재**되고 DB 업로드는 구현되어 있지 않다.
  운영 시 누락된 부분이므로, 펌프 로직 활성화할 때 `to_sql` 호출을 추가해야 한다.

### 9. 동시성 모델

- `ThreadPoolExecutor(max_workers=100)` 로 예측 작업을 submit
- `schedule.every().minute.do(schedule_job, taglist)` — 매 분 예측 사이클 큐잉
- `run_subprocess_with_timeout()` 은 정의만 되어 있고 현재 흐름에서 호출되지 않음 (과거 사용 흔적).
  300초 타임아웃 가드가 필요한 외부 명령 도입 시 활용 가능.
- `load_model` 을 매 실행 때 반복 호출하므로, I/O·메모리가 병목이면 초기화 결과를 캐시하도록 리팩터링 가치가 있다.

---

## 수정 시 체크리스트

- 변수 접두 규칙(`P`/`Q`/`H`)을 바꾸려면 `initialization()` 의 mode 필터와 H 합산 로직, `pred_pump()` 의 컬럼명(`Q_GS_OLD_Predict` 등)을 동시에 수정.
- `testPredict[:, -5, :]` 슬라이스는 모델 출력 시퀀스 길이/오프셋에 종속. 모델 재학습 시 반드시 확인.
- 경로(`/home/app/pump3/`)는 배포 환경 전제. 로컬 실행은 `initialization()`, `taglist_name`, `open_db()` 경로를 함께 수정.
- `GS_taglist_250904.xlsx` 의 시트명을 바꾸면 `pred_and_upload_gs_test` 의 `'Gosan'` 리터럴과 `predict_and_upload_flux_test` 의 `taglist.sheetnames[2:]` 슬라이스 영향.
- xlsx 첫 두 시트는 **설명/메타**로 간주되고 `[2:]` 슬라이스로 스킵된다. 시트 순서 변경 시 슬라이스 인덱스 재확인.
