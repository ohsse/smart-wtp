# smart-wtp-backend

Gradle 멀티모듈 기반의 Spring Boot 백엔드 스켈레톤 프로젝트입니다.

## 목적

- `common`, `api`, `scheduler` 모듈로 역할을 분리한 기본 백엔드 구조를 제공합니다.
- 기본 패키지는 `com.mo.smartwtp`로 통일했습니다.
- PostgreSQL, JPA, MyBatis, Spring Batch 기반 개발을 바로 시작할 수 있도록 최소 설정을 포함합니다.

## 주요 변경 사항

- 루트 Gradle 멀티모듈 설정 추가
- `common` 공통 모듈 생성
- `api` 웹 애플리케이션 모듈 생성
- `scheduler` 배치/스케줄러 애플리케이션 모듈 생성
- Java 21 및 Spring Boot 4.0.5 기준 설정 추가

## 모듈 구성

- `common`: 공통 코드와 유틸리티
- `api`: Spring Web, JPA, MyBatis, PostgreSQL 기반 API 서버
- `scheduler`: Spring Batch, Scheduling, JPA, MyBatis, PostgreSQL 기반 배치 서버

## 사용 방법

1. JDK 21을 설치합니다.
2. PostgreSQL 연결 정보 환경 변수를 설정합니다.
3. Gradle wrapper를 추가하거나 로컬 Gradle 환경에서 빌드합니다.

예시 환경 변수:

- `DB_URL=jdbc:postgresql://localhost:5432/smartwtp`
- `DB_USERNAME=smartwtp`
- `DB_PASSWORD=smartwtp`

## 주의 사항 / 제한 사항

- 현재 작업 환경에는 `gradle` 실행 파일이 없어 Gradle wrapper 생성과 실제 빌드 검증은 수행하지 못했습니다.
- `api`, `scheduler` 모두 데이터베이스 연결 정보를 필요로 합니다.
- 샘플 컨트롤러, 엔티티, 매퍼, 배치 잡은 아직 포함하지 않았습니다.
