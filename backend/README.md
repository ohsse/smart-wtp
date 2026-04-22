# 스마트정수장 백엔드 (smart-wtp-backend)

스마트정수장(Smart WTP) 관리 시스템의 Spring Boot 기반 백엔드. Gradle 멀티모듈 구조로 구성된다.

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| 언어 / 플랫폼 | Java 21, Spring Boot 4.0.5 |
| 빌드 | Gradle Groovy DSL (JDK 21 toolchain 강제, 설정 캐시·병렬 빌드 활성화) |
| 데이터베이스 | PostgreSQL |
| ORM / 쿼리 | Spring Data JPA 4.0.4, Querydsl 5.1.0, MyBatis 4.0.0 |
| 배치 | Spring Batch (scheduler 모듈 전용) |
| API 문서 | springdoc-openapi 3.0.2 (api 모듈 전용) |
| 인증 | JWT (jjwt 0.12.7), Spring Security Crypto |
| SQL 로깅 | p6spy 3.9.1 + `CustomP6SpySqlFormatter` |

---

## 멀티모듈 구조

| 모듈 | 플러그인 | 책임 |
|------|----------|------|
| `common` | `java-library` | 도메인 엔티티, Querydsl QClass 단일 생성, 공통 응답·예외·JWT·p6spy·도메인 이벤트 인프라 |
| `api` | `org.springframework.boot` | HTTP API, 인증 필터, Swagger, JPA/MyBatis 설정 |
| `scheduler` | `org.springframework.boot` | Spring Batch·스케줄링 실행 (REST 계층 없음) |

> `legacy/`, `reference/` 디렉토리는 Gradle 모듈에 포함되지 않는 참고용 코드다.

---

## 빌드 & 실행

### 요구 사항

- JDK 21
- PostgreSQL (접속 정보는 `resources-env/{프로파일}/application.yml` 또는 환경 변수로 주입)

### 기본 빌드 / 테스트

```bash
./gradlew.bat build                  # 전체 빌드 + 테스트 (QClass 재생성 포함)
./gradlew.bat clean build            # 클린 빌드
./gradlew.bat test                   # 모든 모듈 테스트
./gradlew.bat :common:test           # common 모듈 테스트만
./gradlew.bat :api:test              # api 모듈 테스트만
./gradlew.bat :scheduler:test        # scheduler 모듈 테스트만
./gradlew.bat :api:bootRun           # api 로컬 실행
./gradlew.bat :scheduler:bootRun     # scheduler 로컬 실행
```

### 지자체 프로파일(멀티테넌트) 빌드

```bash
./gradlew.bat :api:bootJar -Pprofile=local
./gradlew.bat :scheduler:bootJar -Pprofile=local
```

`-Pprofile={지자체코드}`를 지정하면 `src/main/resources-env/{지자체코드}/` 파일이
기본 `src/main/resources/` 파일을 **오버라이드**한다. 프로파일 미지정 시 기본 파일만 사용된다.

현재 등록된 프로파일: `local`. 추가·확장 절차는 `.claude/rules/multi-tenant.md` 참조.

---

## 프로젝트 구조

```
backend/
├── common/                  # 공통 모듈 (도메인 엔티티, 인프라)
├── api/                     # REST API 실행 모듈
├── scheduler/               # Spring Batch 실행 모듈
├── docs/                    # 작업 산출물 (plan/tasks/results/reviews)
├── .claude/                 # 개발 워크플로우·규칙·훅
├── legacy/                  # 레거시 참고 코드 (빌드 제외)
├── reference/               # 타 프로젝트 참고 코드 (빌드 제외)
├── build.gradle
├── settings.gradle
├── gradlew
└── gradlew.bat
```

---

## 설정 파일 개요

| 파일 | 역할 |
|------|------|
| `{모듈}/src/main/resources/application.yml` | 공통 기본 설정 (`spring.profiles.include: common` 합성) |
| `{모듈}/src/main/resources/application-common.yml` | 공통 세부 설정 (MyBatis, JWT 등) |
| `{모듈}/src/main/resources-env/{프로파일}/application.yml` | 지자체별 오버라이드 (DB, SCADA 접속 정보 등) |
| `{모듈}/src/main/resources/spy.properties` | p6spy 슬로우 쿼리 임계값 (프로파일별 재정의 가능) |
| `api/src/main/resources/db/migration/*.sql` | DB 스키마 마이그레이션 |

> 민감 정보(DB 계정, JWT secret 등)는 환경 변수 또는 프로파일 yml로 주입하며 코드에 하드코딩하지 않는다.

---

## 개발 워크플로우 & 규칙 문서

개발은 `/dev {슬러그}` 커맨드 기반 7단계(요청→계획→분해→구현→결과→리뷰→커밋) 흐름을 따른다.
상세 절차는 `CLAUDE.md` 및 `.claude/commands/dev.md`, `.claude/commands/dev/*.md` 참조.

작업 산출물은 `docs/{plan|tasks|results|reviews}/YYYYMMDD/{슬러그}/` 경로로 축적된다.
pre-commit 훅이 미완료 TASK에 속한 파일을 자동 unstage 한다 (`.claude/hooks/check-task-unstage.sh`).

### 규칙 문서 인덱스

| 영역 | 문서 |
|------|------|
| 네이밍 컨벤션 | `.claude/rules/naming.md` |
| 엔티티 패턴 | `.claude/rules/entity-patterns.md` |
| API 패턴 | `.claude/rules/api-patterns.md` |
| 도메인 용어 사전 | `.claude/rules/domain-glossary.md` |
| DB 운영 패턴 | `.claude/rules/db-patterns.md` |
| 레거시 매핑 | `.claude/rules/legacy-mapping.md` |
| 멀티테넌트 배포 | `.claude/rules/multi-tenant.md` |
| OT 연동 가이드 | `.claude/rules/ot-integration.md` |
| 테스트 전략 | `.claude/rules/test-strategy.md` |
| 문서 하네스 | `.claude/rules/doc-harness.md` |

프로젝트 전역 규칙(언어, 코드 스타일, 커밋 컨벤션 등)은 루트 `CLAUDE.md`를 참조한다.
