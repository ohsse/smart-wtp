# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 개요

`legacy/` 디렉토리는 스마트 정수장 관련 두 개의 독립 레거시 백엔드 모듈을 포함한다.

| 모듈 | 역할 | 상세 문서 |
|------|------|-----------|
| `ems/` | 에너지 관리 시스템 — AI 펌프 제어, 피크 전력 예측, 에너지 절감량 계산 | [ems/CLAUDE.md](ems/CLAUDE.md) |
| `pms/` | 예측 유지보수 시스템 — 설비(펌프·모터) 상태 진단, 알람, 리포트 | [pms/CLAUDE.md](pms/CLAUDE.md) |

각 모듈은 독립 Gradle 프로젝트이며, **루트에서 일괄 빌드하는 방법은 없다**. 작업 모듈 디렉토리로 이동 후 실행한다.

## 공통 기술스택

- **언어**: Java 11
- **프레임워크**: Spring Boot 2.x
- **ORM**: MyBatis (JPA 미사용) — 파라미터/반환값이 `HashMap<String, Object>` 기반
- **데이터베이스**: MariaDB
- **메시지**: Spring Kafka (`spring-kafka:2.8.0`)
- **API 문서**: Springfox Swagger 2 / 3 (모듈별 상이)
- **빌드**: Gradle Groovy DSL

## 빌드 및 실행

```bash
# EMS
cd ems
./gradlew build          # WAR 생성
./gradlew bootRun        # 로컬 실행 (기본 프로파일: dev)
./gradlew test

# PMS
cd pms
./gradlew build
./gradlew bootRun
./gradlew test --tests "com.wapplab.pms.repository.MainMapperTest"
```

## 공통 아키텍처 패턴

### 멀티사이트 프로파일

두 모듈 모두 지자체 정수장별로 프로파일을 분리한다. 프로파일명(예: `gs`, `gm2`, `hy`)이 DB, Kafka, 펌프 설정을 결정하며, 코드 내부에서 사이트 식별자로 직접 비교하는 분기가 존재한다.

### Kafka SCADA 수집 흐름

```
[SCADA] → Kafka Topic → KafkaConsumerService → (가공) → MariaDB
                                                        ↓
                                               스케줄러가 주기적으로
                                               AI 예측·알람 처리
```

### Kafka 이중 클러스터

두 모듈 모두 특정 사이트(`gm2`)에서 두 개의 독립 Kafka 클러스터에 동시 연결하는 이중화 구성을 갖는다. 일반 사이트는 단일 클러스터 구성을 사용한다.

## docs/ 디렉토리

분석/재개발 참고용 원문 문서가 있다. 코드 수정 시 직접 편집하지 않는다.

| 폴더 | 내용 |
|------|------|
| `docs/algorithm/` | 최적 펌프 제어 알고리즘 설명서 |
| `docs/dictionary/` | 공통 표준 단어·용어·도메인 사전 |
| `docs/require/` | 요구사항 정의서 (고산 정수장 기준) |
| `docs/table/` | 테이블 정의서 (EMS, PMS) |
