# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

정수장(Water Treatment Plant) 에너지 관리 시스템(EMS)의 레거시 백엔드 모듈이다.
SCADA에서 수집한 실시간 센서 데이터(Kafka)를 기반으로 펌프 AI 제어, 피크 전력 예측, 에너지 절감량 계산 등을 수행한다.

- **Java 11**, Spring Boot 2.7.14, Gradle
- **데이터베이스**: MariaDB (MyBatis 기반, JPA는 미사용)
- **배포 형태**: WAR (외부 Tomcat) + standalone 실행 모두 지원
- **기본 패키지**: `kr.co.mindone.ems`

## 빌드 및 실행

```bash
./gradlew build          # 빌드 (WAR 생성)
./gradlew bootRun        # 로컬 실행 (기본 프로파일: dev)
./gradlew test           # 테스트 실행
./gradlew clean build    # 클린 빌드
```

로컬 실행 시 `application.properties`의 `spring.profiles.active=dev`가 기본 적용된다.

## 멀티사이트 프로파일 구조

각 프로파일은 특정 정수장 사이트에 대응한다. `application-{profile}.properties`에 해당 사이트의 DB, Kafka, 펌프 설정이 정의된다.

| 프로파일 | 사이트 |
|---------|--------|
| `dev` | 개발 환경 |
| `ba`, `gm2`, `gr`, `gr1`, `gs`, `gu`, `hp2`, `hy2`, `ji2`, `ss`, `wm` | 각 지자체 정수장 |

`wpp_code` 값(= 프로파일명)이 서비스 전체에서 분기 조건으로 광범위하게 사용된다.

## 패키지 구조

도메인별 Controller-Service-Mapper 3계층이 같은 패키지에 위치한다.

| 패키지 | 역할 |
|--------|------|
| `ems.ai` | AI 펌프 예측, 피크 제어, 에너지 예측 |
| `ems.alarm` | 알람 관리, 피크 경보 |
| `ems.common` | 공통 서비스 (Excel, 절감량, 스케줄러) |
| `ems.common.holiday` | 공휴일 판별 (`HolidayChecker`) |
| `ems.config` | CORS(`WebConfig`), Swagger(`SwaggerConfig`) |
| `ems.config.base` | `BaseController` — 공통 응답 생성 |
| `ems.config.response` | `ResponseObject<T>`, `ResponseMessage` |
| `ems.drvn` | 운전현황 (펌프 조합, 성능곡선, Excel) |
| `ems.energy` | 에너지 소비, 피크 모니터링, 요금 정보 |
| `ems.epa` | 수도관망 분석(EPA) |
| `ems.kafka.consumer` | Kafka 소비자 (이중화, 활성) |
| `ems.kafka.producer` | Kafka 생산자 (이중화, 활성) |
| `ems.kafka` | 단일 클러스터 구버전 — `@Profile`로 비활성화됨 |
| `ems.login` | JWT 인증, Spring Security, 로그인 |
| `ems.pump` | 펌프 스케줄러 (AI 제어, 상태 확인) |
| `ems.setting` | 시스템 설정 관리 |

## 주요 코드 패턴

### API 응답
모든 컨트롤러는 `BaseController`를 상속하고 `makeSuccessObj(message, data)`로 `ResponseObject<T>`를 반환한다.

```java
return makeSuccessObj(ResponseMessage.RESPONSE_SUCCESS_MSG, result);
```

### 데이터 접근
MyBatis를 사용하며, 파라미터·반환 타입 대부분이 `HashMap<String, Object>`다.
Mapper XML은 `src/main/resources/sqlmapper/mysql/` 에 위치한다. 파일명에 `_mssql`이 붙지만 실제 MariaDB를 대상으로 한다.

### Kafka 이중화
`kafka.consumer.KafkaConfig` / `kafka.producer.KafkaProducerTasks`가 활성 구현체다.
두 Kafka 클러스터(`bootstrap-servers-1`, `bootstrap-servers-2`)에 동시에 연결하며,
SCADA 토픽(`{SiteCode}1_data`, `{SiteCode}2_data`)에서 데이터를 수신한다.
타임스탬프 단위(`sec` / `min` / `hour` / `all`)에 따라 DB 저장 로직이 분기된다.

### 스케줄러
- `SchedulerService`: 30초 절감량 계산, 자정 오래된 데이터 삭제, CO2·전력 예측 등 (`!dev` 프로파일 활성)
- `PumpScheduler`: 매분 AI 펌프 제어 명령 확인 및 실행 (일부 사이트 제외)

### 보안
- `SecurityConfig`에서 현재 모든 엔드포인트 `permitAll()` 처리 중 (인증 미적용 상태)
- JWT는 `JwtTokenProvider`에서 HS512로 발급하며, 관리자(usrAuth=0)는 1년, 일반 사용자는 `usrTi`분 만큼 유효

## REST API 엔드포인트 구조

| 접두사 | 컨트롤러 |
|--------|----------|
| `/login` | `LoginController` |
| `/ai` | `AiController` |
| `/cm` | `CommonController` |
| `/dr` | `DrvnController` |
| `/es` | `EnerSpendController` |
| `/epa` | `EpaController` |
| `/setting` | `SettingController` |

Swagger UI: `http://localhost:9000/swagger-ui/` (dev 기준)

## 주의 사항

- 동일 기능의 사이트별 분기가 `wpp_code.equals("gs")` 형태의 조건문으로 흩어져 있어, 특정 사이트 로직 수정 시 해당 조건을 모두 확인해야 한다.
- `ems.kafka` (루트 패키지)의 구버전 Kafka 클래스는 `@Profile`로 비활성화되어 있으므로 수정하지 않는다.
- 민감 정보(JWT secret, DB 계정)가 소스코드에 하드코딩되어 있다. 신규 작성 시 환경변수 또는 외부 설정으로 주입한다.
