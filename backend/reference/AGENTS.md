# Repository Guidelines

## Project Structure & Module Organization
이 저장소는 Gradle 멀티 모듈 백엔드입니다. 루트에서 공통 빌드 설정을 관리하고, 실행 코드는 모듈별로 분리합니다.

- `api/src/main/java`: Spring Boot API 애플리케이션
- `batch/src/main/java`: 배치 및 스케줄링 작업
- `common/src/main/java`: 공통 DTO, 유틸리티, 보안, 재사용 로직
- `*/src/test/java`: 모듈별 테스트 코드
- `*/src/main/resources-env/{profile}`: 프로필별 리소스
- `libs/`: 로컬 JAR 의존성
- `doc/`, `docs/`: 설계/분석 문서

새 기능은 먼저 모듈 책임에 맞는 위치를 선택하고, 공통화가 가능할 때만 `common`으로 올립니다.

## Build, Test, and Development Commands
루트에서 Gradle Wrapper를 사용합니다.

- `gradlew.bat build`: 전체 모듈 컴파일, 테스트, 패키징 실행
- `gradlew.bat test`: 전체 JUnit 테스트 실행
- `gradlew.bat :api:bootRun -Pprofile=local`: API 로컬 실행
- `gradlew.bat :batch:bootRun -Pprofile=local`: 배치 애플리케이션 실행
- `gradlew.bat clean`: 생성된 산출물과 Querydsl generated 소스 정리

`api`와 `batch`는 `src/main/resources-env/{profile}`를 읽으므로 `-Pprofile=local` 같은 프로필 지정이 중요합니다.

## Coding Style & Naming Conventions
Java 21, UTF-8, 들여쓰기 4칸을 기준으로 합니다. 클래스는 `PascalCase`, 메서드/필드는 `camelCase`, 상수는 `UPPER_SNAKE_CASE`를 사용합니다. 패키지는 소문자 기준으로 유지하고, 모듈 경계를 넘는 중복 로직은 피합니다.

Lombok, Querydsl, Spring Boot를 사용하므로 수동 보일러플레이트보다 기존 패턴을 따르십시오. 생성 코드는 `src/main/generated`에 두고 직접 수정하지 않습니다.

## Testing Guidelines
테스트는 JUnit 5 기반입니다. 단위 테스트는 운영 코드와 동일한 패키지 구조를 따르고, 클래스명은 `대상클래스명Test` 형식을 사용합니다. 정상 흐름과 실패 흐름을 함께 검증하고, DB/MyBatis/Spring 컨텍스트가 필요한 경우에만 통합 테스트를 추가합니다.

## Commit & Pull Request Guidelines
최근 이력은 `docs:`와 `chore:` 접두사를 사용합니다. 동일한 규칙으로 `feat:`, `fix:`, `refactor:`를 짧은 명령형 제목과 함께 사용하십시오. 예: `fix: validate batch job parameter`.

PR에는 목적, 주요 변경점, 테스트 결과를 포함합니다. API나 배치 동작이 바뀌면 요청/응답 예시, 실행 방법, 필요한 프로필 또는 환경 변수 변경 사항까지 함께 적습니다.

## Security & Configuration Tips
실제 자격 증명은 커밋하지 말고 환경 변수나 프로필별 설정으로 주입합니다. 로컬 JAR은 `libs/` 기준으로 관리하고, `resources-env` 아래 설정 차이를 문서화해 실행 환경 불일치를 줄이십시오.
