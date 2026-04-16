# Repository Guidelines

## Project Structure & Module Organization
이 저장소는 `ems`라는 이름의 단일 Gradle 기반 Spring Boot 백엔드입니다.

- `src/main/java/kr/co/mindone/ems`: 애플리케이션 코드
- `src/main/java/kr/co/mindone/ems/{alarm, ai, common, drvn, drvn2, energy, epa, kafka, login, pump, setting}`: 도메인별 패키지
- `src/main/resources`: `application*.properties`, Log4j 설정, MyBatis 매퍼 XML
- `src/main/resources/sqlmapper`: SQL 매퍼와 MyBatis 설정
- `src/test/java`: 테스트 코드. 현재 기본 스모크 테스트는 `EmsApplicationTests`


## Build, Test, and Development Commands
루트에서 Gradle Wrapper 또는 로컬 Gradle로 실행합니다.

- `gradlew.bat build`: 전체 빌드와 테스트 실행
- `gradlew.bat test`: JUnit 5 테스트만 실행
- `gradlew.bat bootRun`: 로컬 애플리케이션 실행

배포 산출물 확인이 필요하면 `gradlew.bat clean build`를 사용합니다. 로컬 실행 전 `application*.properties`에 맞는 DB, Kafka, JWT 설정을 점검해야 합니다.

## Coding Style & Naming Conventions
현재 기준은 Java 11, Spring Boot 2.7.x, 들여쓰기 4칸, UTF-8입니다.

- 클래스: `PascalCase`
- 메서드/필드: `camelCase`
- 상수: `UPPER_SNAKE_CASE`
- 컨트롤러, 서비스, 매퍼는 `*Controller`, `*Service`, `*Mapper` 접미사를 사용

공통 응답 형식은 `config.response`와 `config.base`를 우선 재사용하고, SQL은 Java 코드에 직접 작성하지 말고 `sqlmapper` XML에 둡니다.

## Testing Guidelines
테스트는 JUnit 5와 `spring-boot-starter-test`를 사용합니다.

- 테스트 클래스명: 대상 클래스명 + `Test`
- 위치: 운영 코드와 같은 패키지 구조 유지
- 최소 기준: 정상 흐름과 실패 흐름 모두 검증

실행은 `gradlew.bat test`를 사용합니다. DB, Kafka, 보안 설정이 얽힌 로직은 단위 테스트와 통합 테스트 범위를 분리해서 작성합니다.

## Commit & Pull Request Guidelines
최근 이력은 `docs:`와 `chore:` 접두사를 사용합니다. 기능 작업은 `feat:`, 버그 수정은 `fix:`, 구조 개선은 `refactor:` 형식을 따릅니다.

PR에는 목적, 주요 변경점, 테스트 결과를 포함합니다. API나 매퍼 변경 시 영향 범위, 요청/응답 예시, 필요한 설정 변경을 함께 적습니다.

## Security & Configuration Tips
실제 비밀값은 커밋하지 말고 환경별 `application-*.properties` 또는 외부 주입으로 관리합니다. JWT 키, DB 계정, Kafka 접속 정보는 코드에 하드코딩하지 않습니다.
