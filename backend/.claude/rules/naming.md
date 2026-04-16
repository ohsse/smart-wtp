# 네이밍 컨벤션

## 기본 규칙

| 대상 | 규칙 |
|------|------|
| 클래스 | `PascalCase` |
| 메서드/필드 | `camelCase` |
| 상수 | `UPPER_SNAKE_CASE` |
| 패키지 | 소문자 |

## Java 클래스 네이밍

| 역할 | 패턴 |
|------|------|
| 엔티티 | `{도메인명}` |
| 컨트롤러 | `{도메인명}Controller` |
| 서비스 | `{도메인명}Service` |
| 리포지토리 | `{도메인명}Repository` |
| 커스텀 리포지토리 | `{도메인명}CustomRepository` |
| 커스텀 리포지토리 구현체 | `{도메인명}CustomRepositoryImpl` |
| 조회/응답 DTO | `{도메인명}Dto` |
| 생성/수정 요청 DTO | `{도메인명}UpsertDto` |
| 검색 조건 DTO | `{도메인명}SearchDto` |
| 이벤트 | `{도메인명}{동작}Event` |
| 이벤트 발행기 | `{도메인명}EventPublisher` |
| 검증기/보조 컴포넌트 | `{도메인명}Validator`, `{도메인명}FileManager`, `{도메인명}Comp` |
| 에러 코드 | `{도메인명}ErrorCode` |
| 테스트 클래스 | `{대상클래스명}Test` |

## DB 테이블 / 컬럼 네이밍

- 약어 기반 스네이크케이스
- PK 컬럼: `{도메인약어}_id`
- 테이블명: `{도메인약어}_{suffix}`

| 역할  | suffix |
|-----|--------|
| 마스터 | `m` |
| 내역  | `l` |
| 상세  | `d` |
| 이력  | `h` |
| 코드  | `c` |
| 명세  | `p`|
