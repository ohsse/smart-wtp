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

개발 작업은 `/dev {슬러그}` 커맨드로 시작한다. 규모 분류(Small/Medium/Large), 단계별 정의(요청→계획→분해→구현→결과→리뷰→커밋), Fix Cycle 처리 등 상세는 `.claude/commands/dev.md`와 `.claude/commands/dev/*.md`를 참조한다.

pre-commit 훅은 `.claude/settings.local.json`에 설정되어 있으며, 미완료 TASK에 속한 파일을 자동 unstage한다. 동작 상세·우회 방법은 `.claude/hooks/check-task-unstage.sh` 상단 주석을 참조한다.

---

## 코드 작성 규칙

- Java 21, UTF-8, 들여쓰기 4칸
- SOLID 원칙 준수
- Lombok 적극 활용 (getter/setter/생성자 직접 구현 지양)
- 의존성 주입은 `@RequiredArgsConstructor` 기반 생성자 주입 사용
- 신규 작성 또는 수정한 클래스, 필드, 메서드에 Javadoc 형식 주석 작성
- Swagger를 이용하여 API 명세를 남긴다

---

## 규칙 문서 인덱스

| 영역 | 문서 | 참조 시점 |
|------|------|----------|
| 네이밍 컨벤션 | `.claude/rules/naming.md` | 클래스·DB 컬럼 명명 전 |
| 엔티티 패턴 | `.claude/rules/entity-patterns.md` | 엔티티 설계·수정 전 |
| API 패턴 | `.claude/rules/api-patterns.md` | Service·Repository·DTO·Swagger 작성 전 |
| 도메인 용어 사전 | `.claude/rules/domain-glossary.md` | 엔티티·컬럼·필드 명명 전 |
| DB 운영 패턴 | `.claude/rules/db-patterns.md` | DB 스키마 설계·마이그레이션·쿼리 작성 전 |
| 레거시 매핑 규칙 | `.claude/rules/legacy-mapping.md` | 레거시 EMS/PMS 대응 신규 설계 전 |
| 멀티테넌트 배포 | `.claude/rules/multi-tenant.md` | 지자체별 배포 구조 설계, resources-env 파일 추가 전 |
| OT 연동 가이드 | `.claude/rules/ot-integration.md` | SCADA 수신·PLC 제어 어댑터 설계 전 |
| 테스트 전략 | `.claude/rules/test-strategy.md` | 테스트 작성·TestContainers·시계열 픽스처 설계 전 |
| 문서 하네스 | `.claude/rules/doc-harness.md` | PLAN/TASK/RESULT/REVIEW 문서 작성 전 |
| 예외·에러 코드 패턴 | `.claude/rules/exception-patterns.md` | ErrorCode 설계·수정 전 |

> **필수**: 엔티티·DTO·DB 테이블을 신규 설계하거나 수정할 때는 `domain-glossary.md`, `db-patterns.md`, `legacy-mapping.md` 세 문서를 먼저 확인한다. 용어 사전에 없는 신규 용어는 `domain-glossary.md`에 먼저 추가한다.

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

커밋 메시지는 한국어로 작성한다.

---

## 보안 및 설정

- JWT secret, DB 계정, 민감 설정은 코드에 하드코딩하지 않는다.
- 환경별 설정은 `application-{profile}.yml` 또는 환경 변수로 주입한다.
- 실제 자격 증명은 커밋하지 않는다.
