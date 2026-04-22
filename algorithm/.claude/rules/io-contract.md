# Java ↔ Python I/O 계약 규칙

Python 모듈은 **stateless CLI** 형태로 호출된다. 이 문서는 CLI 인자·config 네임스페이스·종료 코드·로깅 규칙을 정의한다.

## CLI 인자 계약

모든 `alg/<module>` 은 아래 세 인자를 **필수**로 지원해야 한다. 추가 CLI 인자는 도입하지 않는다.

```bash
python -m alg.<module> \
  --input  <입력파일경로>   \  # Java가 생성한 입력 파일
  --output <출력파일경로>   \  # Python이 결과를 저장할 파일
  --config <설정파일경로>      # Java가 직렬화한 네임스페이스 JSON
```

| 인자 | 타입 | 의미 |
|------|------|------|
| `--input` | 파일 경로 | 시계열 데이터(JSON 또는 CSV). 존재하지 않으면 exit(1). |
| `--output` | 파일 경로 | 결과 JSON 저장 경로. 부모 디렉토리가 없으면 exit(1). |
| `--config` | 파일 경로 | 네임스페이스 분리 JSON. 필수 섹션 누락 시 exit(1). |

> 로깅·모델 경로 등 모든 실행 파라미터는 `--config` 네임스페이스로 흡수한다. 환경변수·추가 CLI 인자 사용하지 않는다.

## --config JSON 네임스페이스 구조

config는 최상위 네임스페이스로 분리하여 책임을 명확히 한다.

```json
{
  "runtime": {
    "log_dir": "C:/logs/alg",
    "log_level": "INFO"
  },
  "site": {
    "site_id": "701-367-FRI",
    "sampling_freq": 12800
  },
  "equipment": {
    "pole": 4,
    "rpm": 1780,
    "bpf": 8.2
  },
  "model": {
    "model_dir": "alg/pms/saved_model",
    "scaler_dir": "alg/pms/saved_scaler"
  }
}
```

| 네임스페이스 | 책임 | 검증 담당 |
|-------------|------|----------|
| `runtime` | 로깅·실행 인프라 | `io_contract.py` (공통) |
| `site` | 정수장 식별자·공통 파라미터 | 모듈별 `core/` |
| `equipment` | 장비(펌프·모터) 파라미터 (Pole/RPM/FREQ/BPF 등) | 모듈별 `core/` |
| `model` | 모델·스케일러 아티팩트 경로 (모델 트리플 규약) | 모듈별 `core/` |

**원칙:**
- 모듈은 **자신이 사용하는 섹션만** 읽는다. 관계없는 섹션이 있어도 무시.
- 필수 섹션이 누락되면 `raise KeyError("config 섹션 '<name>' 누락")` → `sys.exit(1)`.
- 섹션 내 필드는 **모듈별 스키마**로 확정 (`alg/<module>/schemas/config.schema.json`).

### 섹션별 확정 시점 (점진적 확장)

| Phase | 확정 범위 | 스키마 위치 |
|-------|----------|------------|
| **P1 (현재)** | `runtime` 최소 필드 (`log_dir`, `log_level`) | 본 문서에 고정 |
| **P2** | `site` 공통 필드 | 첫 모듈(`pms`) 이관 시 `alg/pms/schemas/config.schema.json` 에 확정 |
| **P3** | 모듈별 `equipment`·`model` 섹션 | 각 모듈 이관 시 해당 모듈 스키마에 추가 |

> Phase 1에서는 `runtime` 섹션만 모든 모듈이 공유하는 규약으로 굳히고, 나머지는 실제 데이터를 본 뒤 확정한다.

## 파일 포맷

| 파일 | 포맷 | 비고 |
|------|------|------|
| `--input` | JSON 또는 CSV | 시계열 원시 데이터는 CSV 허용 |
| `--output` | JSON | 결과는 반드시 JSON |
| `--config` | JSON | 네임스페이스 분리 구조 |
| 모델 아티팩트 | `.keras` / `.pkl` | 모델 트리플 규약 유지 (CLAUDE.md 참조) |

### JSON 스키마 파일 위치

각 모듈의 스키마 정의는 `alg/<module>/schemas/` 에 보관한다.

```
alg/<module>/schemas/
  input.schema.json     # --input 파일 스키마
  output.schema.json    # --output 파일 스키마
  config.schema.json    # --config 파일 스키마 (해당 모듈이 읽는 섹션만 정의)
```

## 종료 코드

| 코드 | 의미 | 발생 조건 |
|------|------|----------|
| `0` | 정상 완료 | 추론·진단 완료, 결과 파일 저장 성공 |
| `1` | 입력 오류 | 파일 미존재, 스키마 불일치, 필수 config 섹션·필드 누락 |
| `2` | 런타임 오류 | 예기치 못한 예외, 연산 중 실패 |
| `3` | 모델 오류 | 모델 파일 로드 실패, 스케일러 불일치 |

Java(`ProcessBuilder`)는 `exitValue()`로 이 코드를 수신하여 재시도·알람 여부를 결정한다.

```python
# 올바른 종료 패턴
import sys

try:
    config = load_config(args.config)             # runtime 섹션 공통 검증
    setup_logging(config["runtime"])              # runtime 섹션으로 로깅 초기화
    result = run_inference(args.input, config)    # 모듈별 섹션 검증
    write_output(result, args.output)
    sys.exit(0)
except (FileNotFoundError, KeyError, ValueError) as e:
    print(f"[ERROR] 입력 오류: {e}", file=sys.stderr)
    sys.exit(1)
except ModelLoadError as e:
    print(f"[ERROR] 모델 오류: {e}", file=sys.stderr)
    sys.exit(3)
except Exception as e:
    print(f"[ERROR] 런타임 오류: {e}", file=sys.stderr)
    sys.exit(2)
```

## 로깅 규칙 (runtime 섹션)

로깅은 **config의 `runtime` 섹션**으로만 제어한다. 환경변수·CLI 인자 사용하지 않는다.

| 채널 | 용도 | 형식 |
|------|------|------|
| `stdout` | 진행 상황·추론 결과 요약 | JSON-lines 또는 평문 |
| `stderr` | 오류·경고 | `[WARN]` / `[ERROR]` 접두사 |

### `runtime` 섹션 필드 (Phase 1 확정)

| 필드 | 필수 | 기본값 | 의미 |
|------|------|--------|------|
| `log_dir` | 선택 | 없음 | 파일 로그 저장 디렉토리. 없으면 파일 로깅 생략(stdout/stderr만). |
| `log_level` | 선택 | `"INFO"` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

```python
# 권장 로그 패턴
import sys
import json
import logging
from pathlib import Path

def setup_logging(runtime: dict) -> None:
    """config['runtime'] 섹션으로 로깅 초기화."""
    level = getattr(logging, runtime.get("log_level", "INFO"))
    handlers = [logging.StreamHandler(sys.stdout)]
    log_dir = runtime.get("log_dir")
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(f"{log_dir}/alg.log"))
    logging.basicConfig(level=level, handlers=handlers)

# 진행 상황 stdout (JSON-lines)
print(json.dumps({"step": "inference", "status": "started"}), flush=True)

# 경고 stderr
print("[WARN] 입력 신호가 짧습니다. 결과 신뢰도가 낮을 수 있습니다.", file=sys.stderr)
```

## Java 호출 측 책임

`../backend/scheduler` 는 아래를 수행하여 config 파일을 생성·전달한다.

1. DB에서 사이트·장비 파라미터 스냅샷 조회 → `site`·`equipment` 섹션 생성
2. `application.yml` 의 로그 경로·레벨 → `runtime` 섹션 생성
3. 모델 아티팩트 경로 규약(`saved_model/<name>.keras` 등) → `model` 섹션 생성
4. 네임스페이스 JSON으로 직렬화 → 임시 파일 저장
5. `ProcessBuilder` 로 `python -m alg.<module> --input ... --output ... --config <임시파일>` 실행
6. 종료 코드 확인 → 결과 JSON 파싱 → DB 적재

> Java 호출 측 상세 규약은 `../backend/scheduler/CLAUDE.md` 에 기재한다.
