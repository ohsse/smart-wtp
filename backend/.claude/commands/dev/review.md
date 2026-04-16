# 6단계: 코드 리뷰 (REVIEW 문서 작성)

목적 슬러그: $ARGUMENTS

---

## 전제조건 검증
1. `$ARGUMENTS`가 비어 있으면 "목적 슬러그를 인자로 전달하세요. 예: `/dev:review jwt_인증_추가`" 안내 후 중단
2. RESULT 문서 탐색 (`docs/results/` 하위에서 슬러그 일치):
   - 같은 날짜 디렉토리 내에서 **가장 큰 번호**의 RESULT 문서를 찾는다.
   - RESULT 문서가 없으면 → "결과 문서가 없습니다. `/dev:result $ARGUMENTS`를 먼저 실행하세요." 경고 후 중단
3. 기준 날짜: RESULT 문서의 날짜를 재사용
4. 현재 RESULT 번호가 N이면 REVIEW{N}을 생성한다 (RESULT1→REVIEW1, RESULT2→REVIEW2)
5. `docs/reviews/{날짜}/$ARGUMENTS/` 탐색:
   - 기존 REVIEW 문서가 있으면 내용을 확인하여 블로커 해소 여부 재검토
   - Fix cycle 진행 중이면 "관련 결과"에 이전 REVIEW 링크도 추가

## 코드 리뷰 수행

**`feature-dev:code-reviewer` 서브에이전트를 spawn하여 자동 리뷰를 수행한다.**

서브에이전트에게 다음 컨텍스트를 제공한다:
- 변경된 파일 목록 (`git diff --name-only HEAD`)
- PLAN 문서 경로 및 내용
- RESULT 문서 경로 및 내용
- 프로젝트 규칙 파일 경로:
  - `CLAUDE.md` (코딩 규칙, 예외/응답 규칙, 보안 규칙)
  - `.claude/rules/naming.md`
  - `.claude/rules/api-patterns.md`
  - `.claude/rules/entity-patterns.md`

**리뷰 체크리스트:**
- [ ] Lombok 사용 (`@Getter`, `@RequiredArgsConstructor`, `@Setter` 금지)
- [ ] 생성자 주입 사용 (`@Autowired` 필드 주입 금지)
- [ ] Javadoc 주석 (신규/수정 클래스, 메서드)
- [ ] Swagger 어노테이션 (`@Tag`, `@Operation`, `@ApiResponses`)
- [ ] `CommonResponseDto` 응답 형태
- [ ] `RestApiException` + `ErrorCode` enum 사용
- [ ] 민감 정보 하드코딩 여부
- [ ] 네이밍 컨벤션 준수
- [ ] 패키지 구조 (feature-based 도메인 중심)
- [ ] 엔티티 패턴 (`@Setter` 금지, 정적 팩토리, 변경 메서드)

## REVIEW 문서 작성

발견 사항을 심각도별로 분류하여 문서를 작성한다:

| 심각도 | 기준 |
|--------|------|
| **높음 (블로커)** | 보안 취약점, 규칙 위반, 명백한 버그 |
| **중간** | 코드 품질 문제, 가독성 저하 |
| **낮음** | 개선 제안, 스타일 의견 |

**REVIEW 문서 템플릿** (`.claude/rules/doc-harness.md` 참조):
```markdown
---
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# {제목}
## 관련 결과
- [결과](../../../results/{YYYYMMDD}/$ARGUMENTS/RESULT1.md)
## 리뷰 범위
## 발견 사항
## 개선 제안
## 결론
```

## 완료 후 안내

리뷰 완료 후:
- **블로커(높음) 발견 시**: `status: draft` 유지
  → "블로커 N건 발견. 수정 사이클을 시작하려면 `/dev $ARGUMENTS`를 실행하세요." 안내
  → (fix cycle을 통해 PLAN{n+1}→TASK{n+1}→impl→RESULT{n+1}→REVIEW{n+1} 전체 흐름 수행)
- **블로커 없음**: `status: approved`로 설정
  → "리뷰 완료, 블로커 없음. `/dev:commit $ARGUMENTS`를 실행하세요." 안내
