# 4단계: 구현 및 검증

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:impl pms_이관`" 안내 후 중단

2. **문서 존재 여부 검증** — `docs/` 하위에서 슬러그 `$ARGUMENTS`와 일치하는 디렉토리를 탐색한다:

   **PLAN 문서 검증:**
   - `docs/plan/` 하위에서 슬러그 일치 디렉토리 탐색 (날짜 불문)
   - PLAN 문서가 존재하면 → Medium 이상 작업으로 판단
   - PLAN 문서가 없으면:
     - TASK 문서도 없으면 → Small 작업으로 간주하고 자유롭게 구현
     - TASK 문서만 있으면 → **"PLAN 문서가 없습니다. `/dev:plan $ARGUMENTS`를 먼저 실행하세요." 경고 후 중단**

   **TASK 문서 검증 (PLAN이 존재하는 경우):**
   - `docs/tasks/` 하위에서 슬러그 일치 디렉토리 탐색
   - TASK 문서가 있으면: `status: approved` 여부 확인. 미승인이면 경고 표시 후 계속 진행할지 확인
   - TASK 문서가 없으면: **"TASK 문서가 없습니다. `/dev:task $ARGUMENTS`를 먼저 실행하세요." 경고 후 중단**

3. 기준 날짜 결정:
   - TASK/PLAN 문서가 있으면 해당 날짜 사용
   - 없으면 오늘 날짜 사용

## 구현

TASK 파일이 있는 경우 미완료 항목(`- [ ]`)을 순서대로 구현한다.

**반드시 준수해야 할 코딩 규칙 (CLAUDE.md + .claude/rules 기반):**

### 모듈 구조
- `.claude/rules/module-layout.md` 레이아웃 준수
- `__main__.py`: argparse + 호출만. 비즈니스 로직 금지.
- `cli.py`: `--input`/`--output`/`--config` 파싱 및 검증
- `core/`: 순수 연산 함수만. 부작용 금지.

### 코드 스타일
- Python, UTF-8, 들여쓰기 4칸 (PEP8)
- Type hint 권장 (mypy 통과 목표)
- ruff 린트 준수

### I/O 계약 (`.claude/rules/io-contract.md` 참조)
- `--input`/`--output`/`--config` 세 인자 필수
- 종료 코드: `0`=OK, `1`=입력오류, `2`=런타임오류, `3`=모델오류
- stdout은 구조화 로그만. stderr는 오류·경고만.

### 5대 원칙 강제
- **원칙 1 (DB 금지)**: `pymysql`, `sqlalchemy`, `pandas.read_sql/to_sql` import 금지
- **원칙 2 (스케줄러 금지)**: `schedule`, `while True:`, `ThreadPoolExecutor` 금지
- **원칙 3 (파일 I/O)**: 결과는 반드시 `--output` 경로의 JSON으로 저장
- **원칙 4 (하드코딩 금지)**: 경로·사이트ID·장비상수를 `config` dict에서 읽기
- **원칙 5 (설정 파일)**: `--config` JSON으로 주입. `sample.json` 참조용으로 유지.

### 레거시 이관 시 보존 항목
- `custom_loss` (`y_true == 10` 마스킹): **3개 모듈 공유 계약. 로직 변경 금지. 변경 시 `predict_power`, `predict_flow_pressure`, `model_train` 3곳 동시 수정.**
- Keras/pkl 모델 아티팩트: 경로 규약 유지 (`saved_model/<name>.keras` ↔ `saved_scaler/<name>/*.pkl`)
- 신호처리·특징추출·진단 알고리즘 본체: I/O 경계만 교체, 함수 로직은 그대로

### 예외 처리
- `sys.exit(1)`: 파일 미존재, 스키마 오류, 필수 config 키 누락
- `sys.exit(2)`: 예기치 못한 런타임 오류
- `sys.exit(3)`: 모델 파일 로드 실패

### 보안
- DB 자격증명 하드코딩 절대 금지 (원칙 1로 인해 애초에 수신하지 않도록 설계)
- 환경별 설정은 env var 또는 `--config` JSON으로 주입

## TASK 체크박스 자동 업데이트

각 Task 구현이 완료될 때마다 TASK 문서의 해당 체크박스를 업데이트한다:
- `- [ ] Task 내용` → `- [x] Task 내용`
- `updated` 날짜도 갱신

## 테스트 실행

구현 완료 후 아래 순서로 검증한다:

```bash
# 1. 린트·포맷 검사
ruff check alg/<module>/
ruff format --check alg/<module>/

# 2. 단위·스냅샷 테스트
python -m pytest alg/<module>/ -v

# 3. CLI 스모크 테스트 (실제 파일 경로로 대체)
python -m alg.<module> \
  --input alg/<module>/tests/fixtures/sample_input.json \
  --output /tmp/alg_out.json \
  --config alg/<module>/config/sample.json
echo "종료 코드: $?"
```

테스트 결과를 사용자에게 보고한다.

## 완료 후 안내 및 자동 전이

테스트 통과 시:
- TASK 파일이 있으면 `status: completed`로 변경
- 작업 규모에 따라 다음 단계 처리:
  - **Small/Medium**: 사용자에게 "구현 완료. `/dev:commit $ARGUMENTS`를 실행하세요." 안내
  - **Large**: `/dev:result $ARGUMENTS`를 **자동 실행**한다

> 작업 규모는 PLAN/TASK 문서가 존재하는지, RESULT 단계가 필요한지로 판단한다.
> PLAN과 TASK가 없으면 Small, PLAN/TASK가 있고 RESULT가 예상 산출물에 포함되면 Large로 간주한다.
