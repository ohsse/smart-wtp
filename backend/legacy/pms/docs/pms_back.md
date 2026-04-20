# PMS Back 프로젝트 분석

## 1. 프로젝트 개요

이 프로젝트는 `Spring Boot 2.5.5` 기반의 PMS(Pump/Motor Monitoring System) 백엔드다. 주 역할은 다음 두 가지다.

- 설비 상태/알람/진단 데이터를 조회하는 REST API 제공
- Kafka로 수집되는 SCADA 데이터를 가공해 MariaDB에 적재

애플리케이션 진입점은 `com.wapplab.pms.KwaterPmsServiceApplication`이며 `@EnableScheduling`이 활성화되어 있다.

기술 스택 요약:

- Java 11
- Spring Boot 2.5.5
- Spring Web, WebFlux, JDBC, AOP
- MyBatis
- MariaDB
- Spring Kafka
- Swagger 2 (`springfox`)
- Lombok

## 2. 빌드 및 실행 구조

### Gradle

`build.gradle` 기준 주요 의존성:

- `spring-boot-starter-web`
- `spring-boot-starter-webflux`
- `spring-boot-starter-jdbc`
- `spring-boot-starter-aop`
- `mybatis-spring-boot-starter:2.2.0`
- `mariadb-java-client`
- `spring-kafka:2.8.0`
- `springfox-swagger2`, `springfox-swagger-ui`

### 실행 프로파일

기본 설정 파일 `src/main/resources/application.yaml`에서 기본 활성 프로파일은 `dev`다.

지원 프로파일 파일:

- `application-dev.yaml`
- `application-gs.yaml`
- `application-gm.yaml`
- `application-gm2.yaml`
- `application-hy.yaml`

구성 특징:

- 공통 MyBatis 설정은 `application.yaml`에 존재
- DB/Kafka 연결 정보는 각 프로파일별 `application-*.yaml`에 분리
- `dev`는 로컬 MariaDB 중심 구성
- 현장 프로파일(`gs`, `gm`, `hy` 등)은 DB와 Kafka 접속 정보를 함께 가짐

### Docker

`Dockerfile`은 OpenJDK 11 기반이며, 기본 실행 프로파일을 `dev`로 고정한다.

```dockerfile
ENTRYPOINT ["java", "-Dspring.profiles.active=dev", "-jar", "/app.jar"]
```

즉, 별도 인자 없이 컨테이너를 띄우면 로컬 개발용 설정을 기준으로 동작한다.

## 3. 패키지 구조와 역할

### `web`

REST API 계층이다. 모든 응답은 공통적으로 `ResponseDTO`로 감싸서 반환한다.

주요 컨트롤러:

- `MainController`
- `MotorController`
- `DiagnosisController`
- `AlarmContoller`
- `ReportController`

공통 특징:

- base path는 `/api/v1/...`
- 대부분 조회성 API
- 입력 DTO는 `web.common` 패키지에 정의
- 예외는 `ControllerExceptionHandler`에서 일괄적으로 `400 Bad Request`로 변환

### `service`

비즈니스 로직 계층이다. 구조적으로는 “복잡한 도메인 객체”보다는 `Map<String, Object>` 조합 중심이다.

주요 책임:

- 조회 결과를 펌프/그룹 단위로 재조합
- 알람 데이터의 문자열 `True/False`를 boolean으로 보정
- 진단 데이터의 압축 해제 및 그래프용 구조 변환
- Kafka 수신 데이터를 `ScadaDto`로 누적 후 DB 저장

### `repository`

MyBatis Mapper 인터페이스 계층이다.

구성:

- Java 인터페이스: `src/main/java/com/wapplab/pms/repository`
- SQL XML: `src/main/resources/mapper/*.xml`

Mapper 목록:

- `MainMapper`
- `MotorMapper`
- `DiagnosisMapper`
- `AlarmMapper`
- `ReportControlMapper`
- `CommonMapper`

### `kafka`

Kafka Consumer 설정 및 수집 처리 로직이 있다.

주요 클래스:

- `KafkaConfig`
- `KafkaConsumerService`
- `KafkaProperties`
- `KafkaProducerTasks`
- `kafka/comsumer/KafkaConfig2`
- `kafka/comsumer/KafkaConsumerService2`

실제 핵심 로직은 `KafkaConsumerService`에 집중되어 있다.

### `config`

애플리케이션 부가 설정:

- `SwaggerConfig`: Swagger 2 문서화
- `CorsConfiguration`: CORS 설정
- `LogConfig`: 로그 설정

### `web.common`

API 공통 요청/응답 모델 보관 위치다.

주요 클래스:

- `ResponseDTO`
- `Message`
- `RequestForm`
- `DateForm`
- `RMSForm`
- `ChannelForm`
- `SettingForm`
- `PumpForm`
- `ScadaDto`

## 4. 공통 응답 및 예외 처리

### 응답 형식

모든 API는 기본적으로 아래 형식으로 반환된다.

```json
{
  "status": 200,
  "message": "success",
  "datas": {}
}
```

`ResponseDTO` 구조:

- `status`: HTTP 상태 코드 숫자
- `message`: `"success"` 또는 `"error"`
- `datas`: 실제 payload

### 예외 처리

`ControllerExceptionHandler`는 `com.wapplab.pms.web` 패키지 전체에 대해 전역 예외 처리를 적용한다.

동작 방식:

- 모든 `Exception`을 catch
- `400 Bad Request`로 응답
- `ResponseDTO.badRequest(e.getMessage(), Message.ERROR.getMessage())` 반환

주의할 점:

- 예외 유형별 세분화 처리 없이 광범위하게 묶여 있다
- 서버 내부 오류도 일괄 `400`으로 내려갈 수 있다

## 5. 주요 API 정리

아래는 컨트롤러 기준 기능군 요약이다.

### 5.1 Main API

base path: `/api/v1/main`

주요 엔드포인트:

- `GET /motorDataAll`
  - 펌프 그룹별 모터 진동/상태성 데이터 조회
- `GET /pumpBearingAll`
  - 펌프 베어링 온도 조회
- `GET /motorAlarm`
  - 그룹별 모터 알람 상태 조회
- `GET /getPumpInf`
  - 펌프 메타 정보 조회
- `GET /getAllFacStats`
  - 전체 설비 집계 수치 조회
- `GET /kafkaTagList`
  - Kafka 태그 매핑 정보 조회

서비스 특징:

- `MainService`는 `getPumpInf()`로 그룹 목록을 먼저 가져온 뒤
- 각 그룹에 대해 Mapper를 반복 호출해 2차원 리스트 형태로 재구성한다

### 5.2 Motor API

base path: `/api/v1/motor`

주요 엔드포인트:

- `POST /alarm`
  - 요청: `RequestForm`
  - 모터 알람 + 온도 알람 정보를 합쳐 반환
- `GET /alarmTemp`
  - 그룹별 온도 알람 조회
- `GET /runningInfo`
  - 운전 정보 조회
- `POST /distribution`
  - 요청: `DateForm`
  - 기간별 분포 데이터 조회
- `POST /vibrationGraph`
  - 요청: `DateForm`
  - 진동 그래프 데이터 조회
- `GET /flowPressure`
  - 유량/압력 조회
- `POST /motorDetails`
  - 요청: `RequestForm`
  - 모터 상세 진단 조회
- `POST /bearingTempInfo`
  - 요청: `RequestForm`
  - 베어링 온도 조회
- `POST /windingTempInfo`
  - 요청: `RequestForm`
  - 권선 온도 조회
- `GET /dstrbChart`
  - 분포도 JSON 조회
- `POST /selectPumpDstrb/{pump_id}`
  - 펌프별 분포 데이터 조회
- `GET /selectGraphThreshold`
  - 그래프 임계값 조회

서비스 특징:

- `MotorService`는 `MainMapper.getPumpInf()` 결과를 기준으로 전체 펌프를 순회한다
- 일부 API는 `DateForm`을 `PumpForm`으로 변환해 Mapper에 전달한다
- 알람 API는 문자열 `"True"`, `"False"`를 boolean으로 변환하는 후처리를 수행한다
- 온도 조회는 `bearingTempInfo`, `windingTempInfo` 대신 SCADA 기반 Mapper 메서드를 실제 사용한다

### 5.3 Diagnosis API

base path: `/api/v1/diagnosis`

주요 엔드포인트:

- `GET /pumpList`
  - 펌프/채널 목록 조회
- `POST /rms`
  - 요청: `RMSForm`
  - RMS 그래프 데이터 조회
- `POST /timewave`
  - 요청: `ChannelForm`
  - TimeWave 데이터 조회
- `POST /spectrum`
  - 요청: `ChannelForm`
  - Spectrum 데이터 조회
- `POST /spectrumFreq`
  - 요청: `ChannelForm`
  - Spectrum 주파수 계열 조회
- `POST /setting`
  - 요청: `SettingForm`
  - 진단 설정값 조회
- `POST /updateSettingParm`
  - 요청: `List<HashMap<String, String>>`
  - 설정값 수정

서비스 특징:

- `DiagnosisService`는 일부 진단 원본 데이터를 압축 해제 후 다시 그래프용 배열로 변환한다
- `DATA_ARRAY`는 Base64 + GZIP + UTF-16 형태의 데이터일 가능성을 전제로 처리한다
- `TimeWave`는 x축 step `1.0`, `Spectrum`은 x축 step `0.5`로 계산한다
- 설정값 수정은 리스트를 순차 업데이트하며, 하나라도 실패하면 비정상 결과를 반환한다

### 5.4 Alarm API

base path: `/api/v1/alarm`

주요 엔드포인트:

- `GET /alarmStatusDefect`
  - 요청: query parameter map
  - 기간 기준 결함/경보 상태 카운트 조회
- `GET /weeklyAlarmTrend`
  - 요청: query parameter map
  - 주간 알람 추이 조회
- `GET /alarmList`
  - 요청: query parameter map
  - 알람 목록 조회

특징:

- DTO 대신 `HashMap`으로 직접 파라미터를 수신한다
- 파라미터 스키마가 코드 레벨에서 강하게 고정되어 있지 않다

### 5.5 Report API

base path: `/api/v1/reportControl`

주요 엔드포인트:

- `GET /alarmCount/{dateType}`
  - `dateType`: `all`, `week`
  - 알람 통계 조회
- `POST /alarmList`
  - 요청: `DateForm`
  - 기간별 알람 목록 조회

## 6. 요청 DTO 정리

### `RequestForm`

- `id`
- `startDate`
- `endDate`

주로 모터/펌프 상세 조회에 사용된다.

### `DateForm`

- `startDate`
- `endDate`

기간 기반 조회에 사용된다.

### `RMSForm`

- `motor_id`
- `channel_nm`
- `startDate`
- `endDate`

### `ChannelForm`

- `motor_id`
- `channel_nm`
- `acq_date`

### `SettingForm`

- `grp_id`
- `channel_nm`
- `parm_nm`
- `parm_value`

## 7. 데이터 접근 방식

이 프로젝트는 전형적인 `Controller -> Service -> Mapper(XML SQL)` 흐름을 가진다.

특징:

- JPA 엔티티 기반이 아니라 MyBatis SQL 매핑 기반
- 반환 타입이 대부분 `Map<String, Object>` 또는 `HashMap<String, Object>`
- 도메인 모델보다 조회 결과 가공 위주의 구조
- SQL 복잡도와 실제 비즈니스 규칙 상당 부분이 XML Mapper에 있을 가능성이 높다

따라서 기능 분석 시 Java 코드만 보는 것으로는 충분하지 않고, 반드시 `src/main/resources/mapper/*.xml`도 함께 봐야 한다.

## 8. Kafka 수집 파이프라인

이 프로젝트의 중요한 축은 REST API뿐 아니라 Kafka 기반 SCADA 데이터 수집이다.

### 활성 조건

`KafkaConfig`와 `KafkaConsumerService`는 다음 프로파일 조건에서만 활성화된다.

```java
@Profile("!dev & !gm2")
```

의미:

- `dev` 프로파일에서는 Kafka consumer 비활성
- `gm2` 프로파일에서도 비활성
- 그 외 프로파일에서만 활성

### 처리 흐름

`KafkaConsumerService` 기준 처리 순서:

1. Kafka topic(`scada1`, `scada2`, `scada3`) 메시지 수신
2. JSON 문자열을 `HashMap<String, Object>`로 파싱
3. DB에서 가져온 태그 매핑 정보(`commonService.kafkaTagList()`)와 대조
4. 태그별 값을 `ScadaDto`에 누적
5. 펌프별 데이터가 충분히 채워지면 `commonService.insertScadaDto()`로 저장
6. 일부 raw message는 `msgInsert`, `insertRawData`로 별도 적재

### `ScadaDto` 역할

`ScadaDto`는 펌프 1건의 수집 시점을 나타내는 누적 버퍼 역할을 한다.

포함 필드 예:

- `PUMP_SCADA_ID`
- `CENTER_ID`
- `ACQ_DATE`
- `EQ_ON`
- `FREQUENCY`
- `FLOW_RATE`
- `PRESSURE`
- `R_TEMP`, `S_TEMP`, `T_TEMP`
- 모터/펌프 DE, NDE 베어링 온도
- `DISCHARGE_PRESSURE`
- `SUCTION_PRESSURE`

구현 특징:

- 초기값은 `-1`
- 완성되지 않은 필드는 저장 직전 `0`으로 치환
- `tryCount`를 두어 일정 횟수 이상 누적되면 강제로 저장 가능

### 데이터 완성 조건

`isScadaDtoComplete()`에서 센터(`centerId`)와 펌프 ID에 따라 완성 조건이 달라진다.

즉, Kafka 적재 로직은 단순 insert가 아니라:

- 센터별 필드 조합 규칙
- 펌프별 예외 규칙
- timestamp 기준 누적/flush 로직

을 포함한 상태 기반 처리다.

## 9. 테스트 구조

테스트 코드는 많지 않으며, 주로 Mapper 검증 중심이다.

확인된 테스트:

- `KwaterPmsServiceApplicationTests`
- `MainMapperTest`
- `MotorMapperTest`
- `config/MybatisAndDb`

특징:

- 서비스/컨트롤러 레벨 테스트는 거의 없음
- DB 연결 전제가 있는 Mapper 테스트 중심
- 일부 테스트는 주석 처리되어 있음

즉, 자동화 테스트보다 실제 DB 질의가 정상 동작하는지 확인하는 성격이 강하다.

## 10. 운영 및 유지보수 관점 포인트

### 장점

- 기능군별 패키지 분리가 비교적 명확함
- API 계층과 DB 접근 계층이 분리됨
- Kafka 수집과 REST 조회가 한 프로젝트 안에서 연결됨
- Swagger 설정이 있어 API 노출 지점 확인이 쉬움

### 주의사항

- `Map<String, Object>` 중심 구조라 타입 안정성이 낮다
- 문자열 기반 key 오타가 런타임 오류로 이어질 수 있다
- 예외 응답이 모두 `400`으로 수렴해 장애 원인 추적이 불편할 수 있다
- 설정 파일에 DB 계정/비밀번호 등 민감 정보가 직접 포함되어 있다
- Swagger 설명과 일부 주석에 인코딩이 깨진 문자열이 섞여 있다
- Kafka/진단 로직에 현장별 예외 규칙이 코드에 하드코딩되어 있다

### 분석 시 우선 확인 대상

이 프로젝트를 추가 분석하거나 수정할 때는 아래 순서가 효율적이다.

1. 컨트롤러에서 엔드포인트와 입력 DTO 확인
2. 서비스에서 결과 조합/후처리 로직 확인
3. Mapper XML에서 실제 SQL과 컬럼명 확인
4. 프로파일별 설정에서 DB/Kafka 연결 환경 확인
5. Kafka consumer에서 수집 및 적재 규칙 확인

## 11. 한 줄 요약

이 저장소는 “설비 진단/상태 조회 API”와 “Kafka 기반 SCADA 적재 로직”이 결합된 Spring Boot + MyBatis + MariaDB 백엔드이며, 비즈니스 로직 상당 부분은 `Map` 기반 후처리와 Mapper SQL, 그리고 Kafka 누적 적재 규칙에 들어 있다.
