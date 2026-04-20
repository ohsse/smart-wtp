# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

K-Water PMS(Predictive Maintenance System) — 수처리장 설비(펌프, 모터, 변압기, VCB 등)의 예측 유지보수 시스템 레거시 백엔드. SCADA 데이터를 Kafka로 수집하여 MariaDB에 저장하고, REST API로 대시보드·진단·알람·리포트 기능을 제공한다.

## 기술스택

- **언어**: Java 11
- **프레임워크**: Spring Boot 2.5.5
- **데이터베이스**: MariaDB (`org.mariadb.jdbc.Driver`)
- **ORM**: MyBatis 2.2.0 (JPA 미사용)
- **메시지**: Spring Kafka 2.8.0
- **API 문서**: Springfox Swagger 2 (`springfox-swagger-ui/swagger2:2.9.2`)
- **빌드**: Gradle Groovy DSL

## 빌드 및 테스트 명령어

```bash
# 빌드
./gradlew build

# 전체 테스트 실행
./gradlew test

# 특정 테스트 클래스 실행
./gradlew test --tests "com.wapplab.pms.repository.MainMapperTest"

# 로컬 실행 (dev 프로필 기본)
./gradlew bootRun

# 특정 프로필로 실행
./gradlew bootRun --args='--spring.profiles.active=gs'
```

> **주의**: 매퍼 테스트(`MainMapperTest`, `MotorMapperTest`)는 `@AutoConfigureTestDatabase(replace = Replace.NONE)` 설정으로 실제 DB에 연결하므로, `application-dev.yaml`의 DB가 필요하다.

## 환경 프로필

| 프로필 | 사이트 | 서버 포트 | Kafka |
|--------|--------|-----------|-------|
| `dev`  | 개발   | 4040      | 없음  |
| `gm`   | 구미   | 10016     | 단일 클러스터 |
| `gm2`  | 구미v2 | 10016     | 이중 클러스터 |
| `gs`   | 고산   | 10016     | 단일 클러스터 |
| `hy`   | 학야   | 10016     | 단일 클러스터 |

기본 활성 프로필: `dev` (`application.yaml`에서 지정)

## 아키텍처

### 레이어 구조

```
[Kafka Topics] ──> [KafkaConsumerService] ──> CommonService ──> CommonMapper
[REST 요청]   ──> [Controller (web/)]    ──> [Service]      ──> [Mapper (repository/)] ──> MariaDB
```

모든 계층 간 데이터는 `HashMap<String, Object>` 또는 `List<Map<String, Object>>`로 전달된다. 도메인 엔티티 클래스는 없다.

### 도메인 영역별 역할

| 도메인 | Controller 경로 | 역할 |
|--------|----------------|------|
| Main   | `/api/v1/main` | 대시보드: 모터 현황, 베어링 온도, 알람, 펌프 정보, 설비 통계 |
| Motor  | `/api/v1/motor` | 모터 상세: 알람, 진동, 분포, 유량/압력, 온도 |
| Diagnosis | `/api/v1/diagnosis` | 정밀 진단: RMS 추이, TimeWave, Spectrum, 파라미터 설정 |
| Alarm  | `/api/v1/alarm` | 알람 집계 및 목록 |
| Report | `/api/v1/reportControl` | 알람 리포트 건수/목록 |

### Kafka 이중 구성

`gm2` 프로필을 제외한 모든 사이트는 `kafka/` 패키지의 단일 클러스터 구성을 사용한다. `gm2`는 `kafka/comsumer/`(typo) + `kafka/producer/` 패키지의 이중 클러스터 구성(`KafkaConfig2`, `KafkaConsumerService2`, `KafkaProducerTasks2`)을 사용한다.

**Kafka 토픽 용도:**
- `scada1`, `scada2`: SCADA 원시 태그 데이터 → `ScadaDto`로 누적 후 `TB_PUMP_SCADA` 저장
- `scada3`: 모터 진동 데이터 → `TB_MOTOR` 직접 저장
- `pms_result` (발행): 분 단위 스케줄러가 모터/알람 데이터를 JSON으로 발행

### Diagnosis 데이터 처리

`DiagnosisService`는 센서 장비에서 오는 TimeWave/Spectrum 데이터를 처리한다: Base64 디코딩 → GZIP 압축 해제 → UTF-16 디코딩 → x/y 좌표 리스트 파싱.

## 코드 패턴

### 응답 형식

```java
// 성공
ResponseEntity.ok(ResponseDTO.ok(SUCCESS.getMessage(), data))
// 실패 (ControllerExceptionHandler 자동 처리)
ResponseDTO.badRequest(e.getMessage(), Message.ERROR.getMessage())
```

모든 예외는 HTTP 400으로 반환된다 (`ControllerExceptionHandler`).

### 펌프 그룹 반복 패턴

`MainService`와 `MotorService` 전반에 걸쳐 반복되는 패턴:

```java
List<Map<String, Object>> pumpInfList = mainMapper.getPumpInf(); // 그룹별 대표 펌프 1개씩
List<List<Map<String, Object>>> result = new ArrayList<>();
for (Map<String, Object> pump : pumpInfList) {
    int grpIdx = (int) pump.get("grp_idx");
    result.add(motorMapper.someQuery(grpIdx));
}
```

### MyBatis 매퍼 위치

- Java 인터페이스: `com.wapplab.pms.repository.*Mapper`
- XML 파일: `src/main/resources/mapper/*.xml`
- 모든 반환 타입은 `java.util.HashMap` (타입 안전 DTO 없음)

## 레거시 특이사항

- `AlarmContoller.java` — 클래스명 오타 (`Contoller`, `Controller`가 아님)
- `kafka/comsumer/` — 패키지명 오타 (`comsumer`, `consumer`가 아님)
- `ScadaDto.CENTER_ID` — `"gosan"` 하드코딩 (현재 운영 사이트 기준)
- `KafkaConsumerService.isScadaDtoComplete()` — 사이트별/펌프 ID별 분기 로직이 내장됨
- `LogAspect` — AOP 로깅 코드가 주석 처리되어 현재 비활성 상태
- 일부 컨트롤러는 `@Autowired` 필드 주입, 일부는 `@RequiredArgsConstructor` 생성자 주입이 혼재됨
- DTO 필드명이 camelCase(`startDate`)와 snake_case(`motor_id`, `channel_nm`) 혼용됨
