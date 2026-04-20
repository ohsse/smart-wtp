# OT(Operational Technology) 연동 가이드

현재 OT 연동(SCADA 수신, PLC 제어)은 **미구현** 상태다.
이 문서는 향후 도입 시 지켜야 할 구조·패턴·안전 기준을 사전 확립한다.

---

## 참조 문서 관계

| 문서 | 이 문서와의 관계 |
|------|----------------|
| [`domain-glossary.md`](domain-glossary.md) | SCADA·HMI·Tag·Quality 용어 원천 (§1·§3) |
| [`db-patterns.md`](db-patterns.md) | 수집 데이터 보존 기간·파티션 정책 (§3) |
| [`legacy-mapping.md`](legacy-mapping.md) | 레거시 `TB_RAWDATA`, Kafka 연동 선례 (§1) |
| [`domain-glossary.md §5`](domain-glossary.md) | 알람 4단계 — 장애 시 동작 기준 (§5) |
| `legacy/ems/src/main/java/kr/co/mindone/ems/kafka/` | Kafka 기반 SCADA 수집 레거시 참고 |

---

## 1. 인바운드 어댑터 (SCADA → Spring)

### 지원 채널

| 채널 | 사용 시점 | 레거시 선례 |
|------|----------|------------|
| **Apache Kafka** | 기존 SCADA 미들웨어가 Kafka 브로커에 발행하는 경우 | `ems/kafka/KafkaConsumerService` |
| **MQTT** | 경량 IoT 브로커(Mosquitto·EMQ X) 직접 연동 시 | 신규 도입 |
| **OPC-UA Subscribe** | OPC-UA 서버를 운영하는 SCADA 연동 시 | 신규 도입 |

### 패키지 구조

```
com.mo.smartwtp.scada
├── inbound
│   ├── kafka
│   │   ├── ScadaKafkaConsumer.java          ← @KafkaListener, raw 메시지 수신
│   │   └── ScadaKafkaConsumerConfig.java
│   ├── mqtt
│   │   └── ScadaMqttInboundAdapter.java
│   └── dto
│       └── ScadaRawMessageDto.java          ← 수신 원시 메시지 매핑
├── processor
│   └── ScadaMessageProcessor.java          ← 품질 검사 → 저장 파이프라인
└── outbound
    └── ...
```

### 수신 파이프라인

```java
// 원시 수신 → 품질 검사 → 정규화 → rawdata_1m_h 저장
@KafkaListener(topics = "${scada.kafka.topic}")
public void consume(ScadaRawMessageDto msg) {
    ScadaQualityResult qr = qualityChecker.check(msg);
    if (qr.isRejected()) return;          // 이상치 기각
    ScadaNormalizedDto normalized = normalizer.normalize(msg, qr);
    rawDataRepository.save(normalized);
}
```

> 저장 대상 테이블: `rawdata_1m_h` (`acq_dtm` 파티션 키, `db-patterns.md §1` 참조).

---

## 2. 아웃바운드 어댑터 (Spring → PLC)

### 지원 채널

| 채널 | 사용 시점 |
|------|----------|
| **Modbus TCP** | PLC가 Modbus 레지스터를 노출하는 경우 |
| **OPC-UA Write** | OPC-UA 서버가 Write 노드를 허용하는 경우 |

### 패키지 구조

```
com.mo.smartwtp.scada.outbound
├── modbus
│   ├── ModbusTcpOutboundAdapter.java
│   └── ModbusTcpConfig.java
├── opcua
│   └── OpcUaWriteAdapter.java
└── dto
    └── ControlCommandDto.java             ← 제어 명령 모델
```

### 인터록 선행조건 의무 체크

아웃바운드 제어 명령 발행 전 **반드시** 인터록 선행조건을 검사해야 한다.

```java
public void sendControlCommand(ControlCommandDto cmd) {
    // 1. 인터록 선행조건 검사 (pump_interlock_p 테이블 기준)
    interlockValidator.validateOrThrow(cmd.getEquipmentId(), cmd.getCommandType());
    // 2. 회복성 래퍼를 통한 송신
    circuitBreaker.executeRunnable(() -> plcAdapter.send(cmd));
}
```

> 인터록 규칙 테이블: `pump_interlock_p` (`legacy-mapping.md §3` 참조)

---

## 3. 센서 품질 관리

SCADA 수신 데이터는 QUALITY 필드를 기준으로 3단계 처리를 거친다.

### QUALITY 코드

| 코드 | 의미 | 처리 |
|------|------|------|
| `GOOD` (0) | 정상 측정값 | 그대로 저장 |
| `BAD` (1) | 센서·통신 장애 | 결측 처리, 대체값 적용 |
| `UNCERTAIN` (2) | 신뢰도 낮음 (전환 중·범위 경계) | 로그 기록 후 저장 (집계 시 가중치 0.5) |

### 결측 대체값 기준

| 측정 항목 | 결측 대체값 | 근거 |
|-----------|-----------|------|
| 유량 (FRI) | 직전 Good 값 (Hold Last Value) | 순간 중단 시 운전에 영향 없음 |
| 압력 (PRI) | 직전 Good 값 | 동일 |
| 수위 (LEI) | 직전 Good 값 | 동일 |
| 전력 (PWI) | `null` 저장 + 집계 제외 | 전력 집계 오염 방지 |
| 진동 (RMS) | `null` 저장 | PMS 진단 모델에 미수신 전파 |

> Hold Last Value 지속 시간 한계: 5분 초과 시 BAD로 격상 처리.

### 이상치 기각 기준

물리적 불가능값 또는 설비 정격 ±30% 초과값은 이상치로 기각한다.

```java
boolean isOutlier(String tagNm, double value) {
    TagRangeConfig range = tagRangeConfigRepo.findByTagNm(tagNm);
    return value < range.getPhysicalMin() || value > range.getPhysicalMax();
}
```

이상치 기각 시 `alarm_h`에 `UNCERTAIN` 알람을 기록한다 (`domain-glossary.md §5` 알람 1단계).

---

## 4. 회복성 패턴

### 의존성 도입

OT 연동 모듈 구현 시 다음 의존성을 추가한다.

```groovy
// build.gradle (common 또는 신규 scada 모듈)
implementation 'io.github.resilience4j:resilience4j-spring-boot3:2.2.0'
implementation 'io.github.resilience4j:resilience4j-circuitbreaker:2.2.0'
implementation 'io.github.resilience4j:resilience4j-retry:2.2.0'
```

### 적용 계층

| 패턴 | 적용 위치 | 설정 권장값 |
|------|----------|-----------|
| **Retry** | 아웃바운드 어댑터 (PLC 송신) | maxAttempts=3, waitDuration=500ms |
| **CircuitBreaker** | 아웃바운드 어댑터 (PLC 송신) | failureRateThreshold=50%, waitDurationInOpenState=30s |
| **Bulkhead** | 인바운드 처리 스레드 풀 | maxConcurrentCalls=20 |
| **TimeLimiter** | OPC-UA Write (응답 대기) | timeoutDuration=3s |

### 설정 예시

```yaml
# application.yml
resilience4j:
  circuitbreaker:
    instances:
      plcOutbound:
        failureRateThreshold: 50
        waitDurationInOpenState: 30s
        slidingWindowSize: 10
  retry:
    instances:
      plcOutbound:
        maxAttempts: 3
        waitDuration: 500ms
```

---

## 5. 장애 시 동작 기준

### 인바운드 중단 (SCADA 수신 불가)

| 지속 시간 | 처리 |
|----------|------|
| < 1분 | Hold Last Value, 정상 운전 유지 |
| 1분 ~ 5분 | UNCERTAIN 알람 발생 (알람 1단계), HMI 경고 표시 |
| > 5분 | BAD 알람 격상 (알람 2단계), AI 자동 운전 → 반자동 강제 전환 |

알람 4단계 정의: `domain-glossary.md §5` 참조.

### 아웃바운드 실패 (PLC 제어 불가)

1. CircuitBreaker OPEN 상태에서 제어 명령 수신 시 즉시 `RestApiException` 반환 (사용자에게 에러 응답)
2. 진행 중인 AI 자동 운전 세션은 **안전 정지(Safe Stop)** 시퀀스 실행 후 수동 모드 전환
3. 장애 이벤트를 `ctrl_log_h`에 기록 (`db-patterns.md §6` 제어 로그 2년 보존)

> **⚠️ 절대 금지**: 인터록 검사를 건너뛴 채 재시도하는 로직. 장애 복구 후에도 인터록 선행조건을 반드시 재검사해야 한다.
