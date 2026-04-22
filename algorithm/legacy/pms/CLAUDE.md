# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 모듈 개요

PMS(Predictive Maintenance System)는 상수도 처리 시설의 모터/펌프 진동 데이터를 이용해 이상진단을 수행하는 Python 레거시 알고리즘이다. SCADA MariaDB에서 12,800 Hz 진동 파형을 폴링하여 전처리·특징추출·진단 후 알람 테이블에 기록하는 단일 프로세스 파이프라인이다.

상위 `algorithm/legacy/CLAUDE.md`는 PMS, predict_power, predict_flow_pressure 전체를 다루므로 여기서는 PMS 관련 세부사항만 기술한다.

---

## 실행 명령어

```bash
# 의존성 설치 (고정 버전, Python 3.9 기준)
pip install -r requirements.txt

# 메인 진단 루프 실행 (현재 디렉토리 기준으로 실행해야 sys.path.append(os.getcwd()) 가 동작)
python main.py

# 온도 진단 (권선/베어링 온도 파이프라인)
python main_temperature.py

# 센서 고장 탐지
python main_sensorfailure.py
```

`config/config.yaml`의 `database:` 항목 5개(db_ip, db_port, db_name, db_id, db_pw)를 사이트에 맞게 수정한 뒤 실행한다. 실행 로그는 `logs/main_stdout.log`, `logs/main_stderr.log`로 쌓인다.

테스트 프레임워크는 없다. `main_test*.py`는 정식 테스트 스위트가 아니라 특정 시점에 캡처한 수동 검증 스크립트다.

---

## 파이프라인 데이터 흐름

```
TB_MOTOR (gzip+Base64+UTF-16 압축 파형, proc_stat=0 행만 조회)
  ↓ main.decompress()
numpy float 배열 (25,600 샘플 = 12,800 Hz × 2초)
  ↓ preprocess.do_preprocess() — Butterworth 대역통과 → Hilbert 포락선
  ↓ feature_extraction.get_spectral_features() / get_bearing_char_freqs() / get_rms_velocity()
FFT 스펙트럼, 베어링 특성주파수(BPFO/BPFI/BSF/FTF), 속도 RMS
  ↓ motorDiagnosis.diagnose() / PumpDiagnosis.diagnose()
진단 튜플 (motor: 13-튜플, pump: 11-튜플)
  ↓ merge_by_device.merge_by_motor() / merge_by_pump()
DE/NDE 양쪽 센서 결과를 기기 단위로 병합
  ↓ main.send_alarm()
TB_PMS_ALR, TB_AI_DIAG_MOTOR, TB_AI_DIAG_PUMP
```

`motor_status.get_motor_1x()`가 1X 주파수 크기를 보고 **모터 ON/OFF를 판정**한다. OFF 구간의 샘플은 `motorDiagnosis`/`PumpDiagnosis` 내부 히스토리에 쌓이지 않으며, `run_steps`가 `n_hist`(기본 1) 이상이 되어야 실제 진단이 수행된다. 허위 진단을 막기 위한 의도이므로 이 상태 보존 로직은 함부로 건드리지 말 것.

---

## 핵심 파일 책임

| 파일 | 역할 |
| --- | --- |
| `main.py` | DB 폴링 루프, `decompress/compress_array`, `fetch_device_info_from_db`, `send_alarm`, 알람 타입 리스트 정의 |
| `motor_class.py` | 모터 진단 상태객체. **원시 FFT 스펙트럼**으로 베어링 진단 |
| `pump_class.py` | 펌프 진단 상태객체. motor 진단 + 캐비테이션(2–3.5 kHz 밴드) + 임펠러. **포락선 스펙트럼**으로 베어링 진단 |
| `diagnosis_algorithms.py` | SVM/LR 모델 로드, `check_rms_alarm`, `diagnose_bearing`, `diagnose_rotor`, `diagnose_unbalance_misalignment` |
| `feature_extraction.py` | FFT, 포락선 스펙트럼, nX 고조파, `get_iqr_threshold` (Numba `@njit` JIT) |
| `preprocess.py` | Butterworth 필터, Hilbert 포락선 |
| `merge_by_device.py` | DE/NDE 센서 → 기기 단위 집계 |
| `motor_status.py` | 1X 성분 기반 운전/정지 판별 (matplotlib import 있음 — 헤드리스 주의) |
| `Bearingtemperature.py` / `Windingtemperature.py` / `vibrationsensor.py` | 온도·센서 고장 분기 파이프라인 (main_temperature.py, main_sensorfailure.py에서 사용) |
| `config/config.py` | `Config` 싱글톤. `config` 인스턴스를 import해서 사용 |
| `util/utils/db.py` | `DBConnect` — PyMySQL 연결 래퍼 (`charset=utf8` 고정) |

---

## 비자명한 설계 사항

### 장비 스펙의 출처
레거시 코드에는 `device_info.json`이 남아 있지만 **실제 실행 경로에서는 사용하지 않는다**. `main.py:fetch_device_info_from_db()`가 `TB_AL_SETTING` 테이블에서 Pole/RPM/FREQ/BPF 값을 읽어 런타임에 `device_info` 딕셔너리를 구성한다. `device_info.json`은 참고용이거나 DB 없이 실험할 때만 유효하다.

### 그룹(GRP_ID) 명명 규칙
`TB_AL_SETTING`의 그룹이 1개면 `motor_` → `motor_0`으로, 2개면 GRP_ID에 따라 `motor_o_`(1) 또는 `motor_n_`(2)로 치환된다 (`main.py:90-97`). 사이트별 분기 로직이 DB에서 읽은 문자열 변환에 숨어 있으므로, 새 사이트 지원 시 이 치환 규칙을 확인해야 한다.

### 진단 출력 튜플
- `motorDiagnosis.diagnose()` → 13-튜플: `(unbal_amp, unbal, misalign_amp, misalign, rotor_amp, rotor, bearing_amp, bpfo, bpfi, bsf, ftf, v_rms, rms_alarm)`
- `PumpDiagnosis.diagnose()` → 11-튜플: `(cav_amp, cavitation, impeller_amp, impeller, bearing_amp, bpfo, bpfi, bsf, ftf, v_rms, rms_alarm)`

호출부(`main.py`)와 반환부를 함께 수정해야 한다.

### 심각도 임계값과 민감도 매핑
```
amp ≥ 1.0 → Fault (적색)
amp ≥ 0.8 → Warning (황색)
amp <  0.8 → Normal/Check
```
민감도 `sensitivity ∈ [1,10]`은 `threshold = 1 - 0.04 × sensitivity` 로 변환된다. 사용자가 민감도 값을 조절하면 임계값이 선형으로 이동한다.

### 알고리즘 혼합 비율
- 불균형·오정렬: **SVM 확률 0.6 + RMS 규칙 0.4**
- 베어링 결함: **LR 확률 0.1 + 피크 규칙 0.9** (규칙 지배)
- 회전자 결함: 4개 로터 성분 중 **3개 이상 검출 시** 판정 (규칙 전용)

### 모터 vs 펌프 베어링 진단의 차이
`motor_class.py`는 원시 FFT 스펙트럼을, `pump_class.py`는 포락선 스펙트럼을 사용한다. 의도적 차이인지 미해결 불일치인지 불분명하므로 어느 한쪽을 수정하면 반드시 다른 쪽도 같이 검토한다.

### 데이터 압축 포맷
`TB_MOTOR.data_array`는 `float[] → JSON 문자열 → UTF-16 → gzip → Base64`순으로 압축되어 있다. 역변환은 `main.decompress()`. UTF-16 인코딩을 놓치면 디코드가 깨진다.

### 샘플링 레이트
`fs = 12800`이 `motor_class.py`, `pump_class.py`, `feature_extraction.py`, `preprocess.py`에 각각 하드코딩되어 있다. 장비 교체로 샘플링이 바뀌면 **4곳을 동시에 수정**해야 한다.

### IQR 임계값 재산정
`feature_extraction.get_iqr_threshold`는 Tukey fence n=2.25이며 Numba `@njit` JIT 컴파일 대상이라 첫 호출이 느리다. 이 임계값은 학습 데이터 분포 종속이므로 현장 데이터가 바뀌면 재산정해야 한다.

---

## 사이트 변형 파일

`main_2.py`, `main_3.py`, `main_20240910.py`, `main_hy_backup_20240904.py`, `main250219.py`, `main_test*.py`, `main.py_20250424` 등은 **특정 사이트·특정 시점의 실험적 포크**다. 신규 로직은 `main.py`에 통합하고 사이트별 분기는 `config/config.yaml` 또는 DB 설정으로 처리하는 것이 원칙이다. 기존 변형 파일을 무작정 삭제하지 말고, 각 파일이 어느 현장의 어떤 이슈에 대응했는지 git log로 확인한 뒤 정리한다.

`feature_extraction.py_org`, `merge_by_device.py_org`, `main.py_20250424`, `merge_by_device25.02.19.py` 등 `_org`·날짜 접미사 파일은 롤백용 스냅샷이다.

---

## DB 테이블 (주로 참조하는 것)

| 테이블 | 용도 |
| --- | --- |
| `TB_MOTOR` | 입력. 압축 파형, `proc_stat=0` 행만 처리 대상 |
| `TB_AL_SETTING` | 설비 파라미터 (Pole, RPM, FREQ, BPFO/BPFI/BSF/FTF 등) |
| `TB_THRESHOLD` | 민감도 임계값 (JSON) |
| `TB_PMS_ALR` | 알람 결과 (ALR_ID, MSG, FAC_NAME, DIAG_STUS, FLAG) |
| `TB_AI_DIAG_MOTOR` / `TB_AI_DIAG_PUMP` | 항목별 amp/alarm 진단 결과 |
| `TB_TIMEWAVE` / `TB_SPECTRUM` / `TB_FREQ` / `TB_RMS` | 1초 스냅샷, FFT, nX 주파수, 속도 RMS |

스키마 변경 시 `main.py`의 raw SQL과 `send_alarm()`을 동시에 손봐야 한다. 쿼리 빌더가 없으므로 f-string으로 SQL이 조립되어 있다 — 외부 입력이 들어오는 자리가 아닌지 확인 후 수정한다.

---

## 사전 학습 모델

- `ML_models/unbal_misalign_model_rbf_svm.pkl` — 불균형·오정렬 RBF SVM
- `ML_models/bearing_LR_model.pkl` — 베어링 결함 로지스틱 회귀
- `hours0819.pkl` — (루트 위치) 학습 시점 시간 지표 스냅샷. 용도 재확인 필요

`model_train/` 노트북은 상위 디렉토리(`algorithm/legacy/pms/model_train/`)에 있고, 학습 후 pkl 파일을 위 경로에 덮어쓰면 즉시 반영된다.

---

## 주의사항

- `main.py`는 `sys.path.append(os.getcwd())`를 해버리므로 **반드시 `pms/` 디렉토리에서 실행**해야 상대 import가 동작한다. 다른 디렉토리에서 `python pms/main.py`로 실행하면 import가 깨진다.
- `motor_status.py`가 matplotlib을 import하므로 헤드리스 서버에서는 백엔드를 `Agg`로 바꾸거나 해당 시각화 코드를 분리해야 한다.
- `requirements.txt`의 버전은 고정핀(`==`)이다. `numpy==1.20.3` / `scipy==1.7.1` / `numba==0.54.1` 조합은 Python 3.10+ 에서 휠이 없을 수 있으므로 **Python 3.9 환경 권장**.
- `._*` 로 시작하는 파일은 macOS 리소스 포크 찌꺼기다. 신경 쓰지 말 것.
- DB 접속은 `charset=utf8`(utf8mb3) 로 고정되어 있다. 이모지 등 4바이트 문자는 깨질 수 있다.
