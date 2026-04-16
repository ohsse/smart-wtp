# 스마트정수장 백엔드 프로젝트

## 프로젝트 개요
스마트정수장(Smart WTP) 관리 시스템의 백엔드 서비스입니다. Gradle 멀티모듈 구조로 구성되며, 각 모듈은 명확한 책임을 가집니다.

---

## 기술스택
- **언어**: Java 21
- **프레임워크**: Spring Boot 4.0.5
- **빌드도구**: Gradle Groovy DSL
- **데이터베이스**: PostgreSQL
- **ORM**: Spring Data JPA + Querydsl + MyBatis

---

## 멀티모듈 구조

| 모듈 | 역할 |
|------|------|
| `common` | 전체 도메인 엔티티, Querydsl QClass 생성, 공통 응답/예외/유틸리티 |
| `api` | HTTP 요청 처리, 인증, Swagger 문서화, 웹 계층 전반 |
| `scheduler` | Spring Batch 기반 스케줄링 및 배치 오케스트레이션 |

---

## 빌드 및 테스트 명령어

```bash
./gradlew.bat build              # 전체 빌드 및 테스트
./gradlew.bat test               # 테스트만 실행
./gradlew.bat :api:test          # api 모듈 테스트
./gradlew.bat :scheduler:test    # scheduler 모듈 테스트
./gradlew.bat :common:test       # common 모듈 테스트
./gradlew.bat clean build        # 클린 빌드 (QClass 재생성 포함)
./gradlew.bat :api:bootRun       # api 로컬 실행
./gradlew.bat :scheduler:bootRun # scheduler 로컬 실행
```

---

## 작업 흐름

### 작업 규모 분류

작업 규모에 따라 거쳐야 할 단계가 다르다.

| 규모 | 기준 | 단계 |
|------|------|------|
| **Small** | 단일 파일 수정, 버그 픽스, 간단한 리팩토링 | 1 → 4 → 7 (문서 생략 가능) |
| **Medium** | 단일 도메인 기능 추가/수정 | 1 → 2 → 3 → 4 → 7 |
| **Large** | 다중 도메인, 아키텍처 변경, 대규모 재개발 | 1 → 2 → 3 → 4 → 5 → 6 → 7 |

### 단계별 정의 및 전이 조건

1. **요청 구체화**: 불확실한 요청은 질문을 통해 구체화한 뒤 진행한다.

2. **계획 수립**: plan 모드로 계획을 수립하고, `docs/plan/YYYYMMDD/{작업목적}/PLAN1.md`에 작성한다.
   - 산출물: `PLAN1.md` ([템플릿](.claude/rules/doc-harness.md))
   - **전이 조건 → 3단계**: 사용자가 계획 문서를 확인하고 승인. 문서 상단 `status: approved`로 변경.

3. **작업 분해**: 계획이 승인되면 `docs/tasks/YYYYMMDD/{작업목적}/TASK1.md`에 Phase/Task 목록을 작성한다.
   - 산출물: `TASK1.md` ([템플릿](.claude/rules/doc-harness.md))
   - **전이 조건 → 4단계**: TASK 문서의 Phase별 Task 목록 확정.

4. **구현 및 검증**: 코드 작성 후 관련 모듈의 테스트를 실행하여 검증한다.
   - **전이 조건 → 5단계**: `./gradlew.bat :{module}:test` 통과.

5. **결과 정리**: `docs/results/YYYYMMDD/{작업목적}/RESULT1.md`에 변경 사항과 테스트 결과를 요약한다.
   - 산출물: `RESULT1.md` ([템플릿](.claude/rules/doc-harness.md))
   - **전이 조건 → 6단계**: RESULT 문서 작성 완료.

6. **리뷰**: 별도 Reviewer를 spawn하여 검증하고, `docs/reviews/YYYYMMDD/{작업목적}/REVIEW1.md`에 기록한다.
   - 산출물: `REVIEW1.md` ([템플릿](.claude/rules/doc-harness.md))
   - **전이 조건 → 7단계**: REVIEW 문서에서 블로커(심각도 높음) 없음 확인.

7. **커밋/PR**: 사용자 확인 없이 커밋하거나 PR을 생성하지 않는다.

> 문서 디렉토리 구조, 파일 네이밍, 템플릿 상세: [.claude/rules/doc-harness.md](.claude/rules/doc-harness.md)

### Claude Code 훅 (PreToolUse)

`.claude/settings.local.json`에 `PreToolUse` 훅이 설정되어 있다. Claude Code가 `git commit`을 실행하기 전에 자동으로 동작한다.

**동작**: `docs/tasks/` 하위의 미완료(`status != completed`) TASK 문서를 파싱하여, 해당 작업에 속한 파일이 staging에 있으면 자동으로 unstage한다. 남은 staged 파일이 없으면 커밋을 차단한다.

**훅 스크립트**: `.claude/hooks/check-task-unstage.sh`

**우회 방법**:
```bash
GIT_SKIP_DOC_CHECK=1 git commit -m "..."   # 검증 생략
```

**주의**: 이 훅은 Claude Code 세션 내에서만 동작한다. 터미널/IDE에서 직접 커밋할 때는 적용되지 않는다. TASK 문서의 파일 경로는 반드시 전체 상대 경로로 기록해야 훅이 정확히 동작한다. ([경로 기록 규칙](.claude/rules/doc-harness.md))

---

## 코드 작성 규칙

- Java 21, UTF-8, 들여쓰기 4칸
- SOLID 원칙 준수
- Lombok 적극 활용 (getter/setter/생성자 직접 구현 지양)
- 의존성 주입은 `@RequiredArgsConstructor` 기반 생성자 주입 사용
- 신규 작성 또는 수정한 클래스, 필드, 메서드에 Javadoc 형식 주석 작성
- Swagger를 이용하여 API 명세를 남긴다

> 네이밍 컨벤션 상세 (Java 클래스, DB 테이블/컬럼): [.claude/rules/naming.md](.claude/rules/naming.md)

---

## 패키지 규칙

- 최상위 구조는 기술 계층보다 **도메인 중심의 feature-based 패키지**를 사용한다.
- 공통 인프라: `com.mo.smartwtp.common.*`
- api/scheduler 도메인: `com.mo.smartwtp.{도메인명}`
- common 공통 기능: `com.mo.smartwtp.common.{기능패키지명}`

---

## 예외 및 응답 규칙

- 비즈니스 예외는 `RestApiException`으로 통일
- 에러 코드는 `ErrorCode` 인터페이스를 구현하는 enum으로 관리
- API 응답은 항상 `CommonResponseDto` 형태 사용
  - 성공: `code = "SUCCESS"`
  - 실패: `code = ErrorCode.name()`
- 컨트롤러/서비스에서 임의 문자열 에러 코드를 직접 만들지 않는다

---

## 커밋 규칙

```
feat:     새 기능
fix:      버그 수정
refactor: 코드 구조 개선
docs:     문서 변경
chore:    빌드/설정 변경
test:     테스트 추가/수정
```

- 커밋 메시지는 한국어로 작성한다.
- 예: `feat: 사용자 인증 JWT 필터 추가`

---

## 보안 및 설정

- JWT secret, DB 계정, 민감 설정은 코드에 하드코딩하지 않는다.
- 환경별 설정은 `application-{profile}.yml` 또는 환경 변수로 주입한다.
- 실제 자격 증명은 커밋하지 않는다.
