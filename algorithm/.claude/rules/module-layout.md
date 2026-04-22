# alg/ 모듈 레이아웃 규칙

`alg/` 하위 각 모듈은 아래 표준 레이아웃을 따른다.
모든 모듈은 **stateless CLI** 형태여야 한다 (5대 원칙 #2 참조).

## 표준 디렉토리 구조

```
alg/<module>/
  __init__.py          # 빈 파일 또는 공개 API 재export만
  __main__.py          # python -m alg.<module> 진입점. argparse 래퍼만.
  cli.py               # --input / --output / --config 파싱 및 유효성 검사
  io_contract.py       # 입출력 JSON/CSV 스키마 검증 함수
  core/                # 순수 연산 로직 (신호처리·특징추출·추론·진단)
    __init__.py
    ...
  config/              # 기본 설정 샘플 및 설정 로더
    __init__.py
    loader.py          # JSON config 파일 읽기·검증
    sample.json        # 최소 동작 설정 예시 (하드코딩 대체 참조용)
  schemas/             # JSON 스키마 정의 (io-contract.md 참조)
    input.schema.json
    output.schema.json
    config.schema.json
  tests/               # pytest 테스트
    __init__.py
    fixtures/          # 스냅샷·픽스처 데이터
    test_cli.py
    test_core_*.py
```

## 파일별 역할 및 강제 규칙

### `__main__.py` — 진입점
- `argparse` 파싱 + `cli.run()` 호출만 담당
- 비즈니스 로직 금지
- `sys.exit(종료코드)` 로 끝나야 함

```python
# 올바른 예
import sys
from alg.<module>.cli import run

if __name__ == "__main__":
    sys.exit(run())
```

### `cli.py` — CLI 레이어
- `--input`, `--output`, `--config` 세 인자 필수 (io-contract.md 참조)
- 인자 유효성 실패 시 `sys.exit(1)`
- `core/` 함수를 호출하고 결과를 `--output` 경로에 저장
- stdout은 구조화 로그만, stderr는 오류·경고만

### `io_contract.py` — 스키마 검증
- 입력 JSON/CSV의 필수 키·타입 검증
- 검증 실패 시 명확한 메시지와 함께 `raise ValueError`
- `schemas/` 디렉토리의 JSON Schema 파일을 읽어 검증 권장

### `core/` — 순수 연산
- DB 드라이버 import 금지: `pymysql`, `sqlalchemy`, `psycopg2`, `pymssql`
- 스케줄러 import 금지: `schedule`, `apscheduler`
- 무한 루프 금지: `while True:`, `ThreadPoolExecutor`
- 파일 경로 하드코딩 금지: `/home/app/`, `C:\\`
- 사이트 식별자·장비 상수 하드코딩 금지 → `--config` JSON으로 주입

### `config/loader.py` — 설정 로더
- CLI로 전달된 `--config` JSON 파일을 읽어 **네임스페이스 dict** 반환
- 반환 구조: `{"runtime": {...}, "site": {...}, "equipment": {...}, "model": {...}}` (io-contract.md "--config JSON 네임스페이스 구조" 참조)
- 모듈이 사용하는 섹션이 누락되면 `raise KeyError("config 섹션 '<name>' 누락")`
- 모듈이 사용하지 않는 섹션은 무시 (예: `runtime`+`site`만 쓰는 모듈은 `equipment` 검증 안 함)
- `runtime` 섹션은 모든 모듈 공통 — `io_contract.py` 가 공통 검증 담당
- 기본값은 `config/sample.json` 을 참조용으로만 사용 (코드 내 하드코딩 금지)

## 레거시 함수 이관 원칙

레거시(`legacy/<module>/`)의 비즈니스 로직 함수를 이관할 때:

1. **함수 단위로 이관** — 파일 전체 복사 금지
2. **I/O 경계만 교체** — 함수 본체(신호처리·알고리즘)는 그대로 유지
3. **DB 호출 제거** — `open_db()`, `get_db_config()`, `to_sql()` 등을 호출하는 부분만 제거하고 파일 입출력으로 대체
4. **스케줄러 코드 제거** — `schedule.every()`, `while True:` 블록 제거
5. **하드코딩 → 파라미터화** — 경로·사이트ID·장비상수를 `config` dict 인자로 교체

## 명명 규칙 (네이밍)

| 구분 | 규칙 | 예시 |
|------|------|------|
| 모듈·파일 | `snake_case` | `feature_extraction.py` |
| 함수·변수 | `snake_case` | `extract_features()` |
| 클래스 | `PascalCase` | `DiagnosisResult` |
| 상수 | `UPPER_SNAKE_CASE` | `SAMPLING_FREQ` |
| 테스트 파일 | `test_<대상>.py` | `test_core_diagnosis.py` |

> 사이트 식별자·장비 파라미터를 상수로 두는 경우, `UPPER_SNAKE_CASE`를 쓰되 반드시 `--config` 주입으로 대체해야 함. `sample.json`에 예시 값을 두고 코드 내 상수는 제거한다.

## 금지 패턴 요약

```python
# ❌ DB 드라이버 import (원칙 1 위반)
import pymysql
import sqlalchemy
from pandas import read_sql, to_sql

# ❌ 스케줄러·무한루프 (원칙 2 위반)
import schedule
while True:
    ...
from concurrent.futures import ThreadPoolExecutor

# ❌ 하드코딩 경로·식별자 (원칙 4 위반)
INPUT_PATH = "/home/app/power/data.csv"
SITE_ID = "701-367-FRI:..."
fs = 12800  # 코드에 직접 → config JSON으로 이동

# ❌ 환경변수·CLI 인자로 로그 경로 수신 (io-contract.md 위반)
log_dir = os.environ.get("LOG_DIR")       # env 사용 금지
parser.add_argument("--log-dir")          # 추가 CLI 인자 금지

# ✅ 올바른 패턴 (네임스페이스 접근)
def run(input_path: str, output_path: str, config: dict) -> int:
    setup_logging(config["runtime"])          # runtime 섹션으로 로깅 초기화
    fs = config["site"]["sampling_freq"]      # site 섹션
    model_dir = config["model"]["model_dir"]  # model 섹션
    ...
```
