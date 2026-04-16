# 4단계: 구현 및 검증

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:impl jwt_인증_추가`" 안내 후 중단

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

**반드시 준수해야 할 코딩 규칙 (CLAUDE.md 기반):**

### 패키지 구조
- feature-based 도메인 중심 패키지 사용
- `com.mo.smartwtp.{도메인명}` (api/scheduler)
- `com.mo.smartwtp.common.{기능}` (공통)

### 코드 스타일
- Java 21, UTF-8, 들여쓰기 4칸
- Lombok 적극 활용: `@Getter`, `@RequiredArgsConstructor`, `@Builder` 등
- `@Setter` 사용 금지 (엔티티)
- 의존성 주입: `@RequiredArgsConstructor` 생성자 주입
- 신규/수정 클래스·메서드에 Javadoc 주석 작성

### 계층별 규칙
- **엔티티**: `.claude/rules/entity-patterns.md` 패턴 준수
- **서비스/리포지토리**: `.claude/rules/api-patterns.md` 패턴 준수
- **네이밍**: `.claude/rules/naming.md` 컨벤션 준수
- **API**: Swagger `@Tag`, `@Operation`, `@ApiResponses` 어노테이션 작성

### 예외/응답 처리
- 비즈니스 예외: `RestApiException` 사용
- 에러 코드: `ErrorCode` 인터페이스를 구현하는 enum으로 관리
- 응답: `CommonResponseDto` 형태 사용

### 보안
- JWT secret, DB 계정 등 민감 정보 절대 하드코딩 금지
- 환경별 설정은 `application-{profile}.yml` 또는 환경변수로 주입

## TASK 체크박스 자동 업데이트

각 Task 구현이 완료될 때마다 TASK 문서의 해당 체크박스를 업데이트한다:
- `- [ ] Task 내용` → `- [x] Task 내용`
- `updated` 날짜도 갱신

## 테스트 실행

구현 완료 후 영향받은 모듈의 테스트를 실행한다:
```bash
# 변경된 모듈에 따라 선택적 실행
./gradlew.bat :common:test
./gradlew.bat :api:test
./gradlew.bat :scheduler:test
# 또는 전체
./gradlew.bat test
```

테스트 결과를 사용자에게 보고한다.

## 완료 후 안내 및 자동 전이

테스트 통과 시:
- TASK 파일이 있으면 `status: completed`로 변경
- 작업 규모에 따라 다음 단계 처리:
  - **Small/Medium**: 사용자에게 "구현 완료. `/dev:commit $ARGUMENTS`를 실행하세요." 안내 (커밋은 항상 사용자 요청 필요)
  - **Large**: `/dev:result $ARGUMENTS`를 **자동 실행**한다

> 작업 규모는 PLAN/TASK 문서가 존재하는지, RESULT 단계가 필요한지로 판단한다.
> PLAN과 TASK가 없으면 Small, PLAN/TASK가 있고 RESULT가 예상 산출물에 포함되면 Large로 간주한다.
