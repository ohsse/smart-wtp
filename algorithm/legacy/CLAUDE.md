# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

Smart WTP(상수도 처리 시설)의 설비 예지보전·운영 예측을 담당하는 Python 기반 **레거시 알고리즘 레이어**.  
네 개의 독립 서브프로젝트로 구성되며, 각 프로젝트는 DB 폴링 → 추론/진단 → DB 적재의 단일 프로세스 파이프라인이다.

| 서브프로젝트 | 역할 | 상세 문서 |
| --- | --- | --- |
| `pms/` | 진동·온도 기반 모터/펌프 이상진단 (12,800 Hz 파형 분석) | `pms/CLAUDE.md` |
| `predict_power/` | 고산 정수장 1시간 단위 전력 사용량 예측 (DLinear Keras) | `predict_power/CLAUDE.md` |
| `predict_flow_pressure/` | 18개 정수장 유량/압력/수위 1분 주기 예측 + 펌프 조합 추천 (Attention-LSTM Keras) | `predict_flow_pressure/CLAUDE.md` |
| `model_train/` | `predict_flow_pressure`용 Attention-LSTM 학습 노트북 | `model_train/CLAUDE.md` |

> **세부 실행 방법·설계 결정·주의사항은 각 서브프로젝트의 CLAUDE.md를 먼저 확인한다.**  
> 이 문서는 네 프로젝트에 공통으로 적용되는 원칙·패턴만 기술한다.

---

## 빠른 실행 레퍼런스

각 프로젝트가 독립 실행되며 **디렉토리 이동 후 실행**이 원칙이다 (상대 import·상대 경로 가정 때문).

```bash
# PMS (진동 이상진단) — pms/ 디렉토리에서 실행 (main.py가 sys.path.append(os.getcwd()))
cd pms && pip install -r requirements.txt && python main.py

# 전력 예측 (고산)
python predict_power/predictpower_Gosan_main.py

# 유량/압력 예측 (다사이트)
python predict_flow_pressure/main_e_250904.py

# 모델 학습 (Attention-LSTM) — legacy/model_train/ 디렉토리에서 실행
jupyter notebook model_train/At_LSTM_training_GS_1011.ipynb
```

테스트 프레임워크 없음. `pms/main_test*.py`는 수동 검증용 스냅샷이지 정식 테스트 스위트가 아니다.

---

## 공통 아키텍처 패턴

### 1. DB 폴링 루프 구조

세 운영 모듈 모두 동일 패턴이다:

```
schedule(혹은 while True) → DB 조회 → 전처리/특징추출 → 모델 추론/규칙 판정 → DB 적재
```

- **PMS**: `TB_MOTOR`에서 `proc_stat=0` 행만 소비 → 진단 결과를 `TB_PMS_ALR` / `TB_AI_DIAG_*`에 적재.
- **predict_power**: `TB_RAWDATA` 폴링 → 예측 결과를 `TB_CTR_OPT_RST`에 `append`. (60분 주기)
- **predict_flow_pressure**: `TB_RAWDATA` 폴링 → `TB_CTR_TNK_RST`에 `append`. (1분 주기, `schedule` + `ThreadPoolExecutor(max_workers=100)`)

중복 적재 방지 로직은 어느 모듈에도 없다. 재실행 시 중복 주의.

### 2. 외부 파일 의존

Keras 모델 + 변수별 `MinMaxScaler` pkl + 엑셀 태그 정의서가 **이름으로 묶인 트리플**을 이룬다.  
`predict_flow_pressure`·`predict_power` 모두 동일 규약을 따른다:

```
saved_model/<버전>/<site>_<date>.keras    (실패 시 .h5 폴백)
saved_scaler/<버전>/<site>_<date>/<variable>_scaler.pkl
<site>_taglist_<date>.xlsx                  (시트명 = 사이트명)
```

신규 사이트 추가 시 **세 이름을 동일하게** 맞춰야 한다. 학습 노트북(`model_train/`)이 이 구조로 산출물을 내므로 그대로 운영 경로에 복사한다.

### 3. `custom_loss` 계약

두 예측 모듈과 학습 노트북이 공유하는 규약: `y_true == 10`은 마스킹값(무효 스텝).  
모델 로딩 시 `load_model(..., custom_objects={'custom_loss': custom_loss})`를 반드시 주입해야 한다. 함수 시그니처 변경은 모든 호출부에 동시 반영 필요.

### 4. 경로 하드코딩

예측 모듈은 배포 서버 경로(`/home/app/power/`, `/home/app/pump3/`)와 DB 접속정보 일부(`get_db_config()` 내부 호스트)가 **소스에 하드코딩**되어 있다. 로컬/신규 환경 이관 시 각 CLAUDE.md의 "수정 체크리스트"를 참고해 경로·접속정보를 일괄 교체한다.

---

## 기술 스택 (전체 레이어 공통)

- **Python**: PMS는 고정핀(numpy 1.20.3 / scipy 1.7.1 / numba 0.54.1) 때문에 **3.9 환경 권장**. 예측 모듈은 3.9+에서 동작.
- **신호처리**: NumPy FFT, SciPy(Butterworth), Numba `@njit` JIT (PMS 전용)
- **ML/DL**: Scikit-learn(SVM/LR), TensorFlow/Keras(예측·학습), PyTorch(학습 노트북에서 import만, 실제 미사용)
- **DB**: MariaDB/MySQL via PyMySQL + SQLAlchemy. `charset=utf8`(utf8mb3) 고정 → 4바이트 문자 깨짐
- **직렬화**: Joblib / pickle (스케일러·모델)
- **설정**: PyYAML (PMS), 나머지는 코드 내 하드코딩 + `connections.json`
- **스케줄링**: `schedule` 라이브러리 + Python `threading` / `ThreadPoolExecutor`

---

## 주요 DB 테이블 (프로젝트 횡단)

| 테이블 | 주 사용 모듈 | 역할 |
| --- | --- | --- |
| `TB_MOTOR` | PMS | 진동 원시 파형 (gzip+Base64+UTF-16, `proc_stat=0`만 처리) |
| `TB_AL_SETTING` | PMS | 설비 파라미터 (Pole/RPM/FREQ/BPF) — 런타임 `device_info` 구성원 |
| `TB_THRESHOLD` | PMS | 민감도 임계값 (JSON) |
| `TB_PMS_ALR`, `TB_AI_DIAG_MOTOR`, `TB_AI_DIAG_PUMP` | PMS | 알람 결과, 항목별 amp/alarm |
| `TB_TIMEWAVE`, `TB_SPECTRUM`, `TB_FREQ`, `TB_RMS` | PMS | 1초 스냅샷·FFT·nX 주파수·RMS |
| `TB_RAWDATA` | predict_* | 원시 SCADA 입력 (태그별 타임스탬프) |
| `TB_CTR_OPT_RST` | predict_power | 전력 예측 결과 (`OPT_IDX = "701-367-FRI:..."`) |
| `TB_CTR_TNK_RST` | predict_flow_pressure | 유량/압력 예측 결과 |

PMS는 쿼리 빌더가 없고 f-string 조립이므로 외부 입력 유입 자리가 아닌지 확인 후 수정.

---

## 사전 학습 모델 배치

| 경로 | 용도 |
| --- | --- |
| `pms/ML_models/unbal_misalign_model_rbf_svm.pkl` | 불균형·오정렬 RBF SVM |
| `pms/ML_models/bearing_LR_model.pkl` | 베어링 결함 로지스틱 회귀 |
| `predict_power/saved_model/Powerprediction_DLinear_Gosan.keras` (`+.h5`) | 고산 전력 DLinear |
| `predict_flow_pressure/saved_model/250903/<site>_250904.keras` | 18개 정수장 Attention-LSTM |

학습 후 pkl/keras 파일을 위 경로에 덮어쓰면 즉시 반영된다 (리로드 재시작 불필요한 모듈도 있지만, 기본은 프로세스 재시작 권장).

---

## 레거시 파일 정리 원칙

- `main_*.py`의 시점·사이트 변형(`main_2`, `main250219`, `main_hy_backup_*`, `main_test*`, `main.py_20250424` 등)은 **특정 사이트·특정 시점의 실험적 포크·롤백 스냅샷**이다.
- `._*`로 시작하는 파일은 macOS 리소스 포크 찌꺼기 — 무시한다.
- `*.py_org`, `*_YYYYMMDD.py`, `*backup*.py` 접미사는 롤백용 스냅샷.
- **신규 로직은 각 모듈의 정식 엔트리포인트(`pms/main.py`, `predictpower_Gosan_main.py`, `main_e_250904.py`)에 통합**하고, 사이트·시점별 분기는 config나 DB 설정으로 처리하는 것이 원칙.
- 변형 파일 삭제 전에는 `git log`로 어느 현장·어떤 이슈 대응인지 확인한 뒤 정리한다.

---

## 공통 주의사항

- **헤드리스 환경**: `pms/motor_status.py`가 matplotlib을 직접 import하므로, 백엔드를 `Agg`로 설정하거나 import 경로를 분리해야 서버 환경에서 오류가 나지 않는다.
- **타임존**: 예측 모듈은 `pytz.timezone('Asia/Seoul')`을 사용한다. 서버 로컬 타임존과 분리해 관리.
- **모델 리로드 비용**: `predict_flow_pressure`의 `main_e_250904.py`는 매 추론 주기마다 `load_model`을 다시 호출한다. I/O·메모리 병목 시 `initialization()` 결과 캐시가 유효한 최적화 포인트.
- **중복 적재 무방어**: 모든 예측 모듈이 `if_exists='append'`만 사용한다. 수동 재실행·배치 백필 시 DELETE 선행이 필요.

---

## 서브프로젝트 문서 인덱스

각 CLAUDE.md는 해당 모듈의 실행, 파이프라인 세부, 비자명한 설계 결정, 수정 체크리스트를 포함한다:

- [`pms/CLAUDE.md`](pms/CLAUDE.md) — 진단 튜플 포맷, 심각도 임계, SVM/LR 혼합 비율, 사이트 변형 파일 정리, GRP_ID 명명 규칙.
- [`predict_power/CLAUDE.md`](predict_power/CLAUDE.md) — taglist `비고` 분류 규칙, `custom_loss` 계약, `.keras→.h5` 폴백, `OPT_IDX` 포맷, 읽기/쓰기 DB 분리.
- [`predict_flow_pressure/CLAUDE.md`](predict_flow_pressure/CLAUDE.md) — PRES/FLUX/BOTH mode, H 변수 접두 합산, β-blending 실측 보정, 펌프 OLD/NEW 조합, xlsx 시트 슬라이스.
- [`model_train/CLAUDE.md`](model_train/CLAUDE.md) — Attention-LSTM 구조, IQR 스케일(±2.8 fence), Y 패딩 마스킹, Gosan 하드코딩 필터, 산출물 디렉토리 규약.
