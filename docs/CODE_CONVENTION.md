# 코드 컨벤션 · 브랜치 전략 · 리팩토링 가이드

AI-SkinScope 팀 저장소에서 코드를 작성하고 합칠 때 따르는 규칙입니다. 설정 파일은 저장소 루트의 [`pyproject.toml`](../pyproject.toml)입니다.

## 1. 적용 원칙

- **새로 작성하거나 수정하는 코드부터** 아래 규칙을 적용합니다.
- 기존 코드는 기능을 바꾸지 않는 별도 PR(`refactor:`)로 조금씩 정리합니다. 기능 수정과 스타일 정리를 한 PR에 섞지 않습니다.
- 2026-10-15 기준선: `ruff check .` 지적 165건 중 150건은 자동 수정이 가능한 표기 차이(`Optional[X]` → `X | None`, 파일 끝 줄바꿈 등)입니다. 남은 15건(예: `zip()`에 `strict` 누락, 반복문 변수 참조)은 동작 확인이 필요해 리팩토링 대상으로 남겨 둡니다(5절).

## 2. Python (백엔드 `app/`, 스크립트 `scripts/`)

| 항목 | 규칙 |
| --- | --- |
| 포맷 | `black` (줄 길이 120) |
| 정적 분석 | `ruff` (규칙: E, W, F, I, B, UP) |
| 버전 | Python 3.10 이상 |
| 이름 | 변수·함수 `snake_case`, 클래스 `PascalCase`, 상수 `UPPER_SNAKE_CASE`, 모듈 내부용 함수는 `_`로 시작 |
| 타입 힌트 | 함수 인자와 반환값에 작성 (Pydantic 스키마는 `app/schemas/`) |
| 계층 | `routers/`(요청·응답) → `services/`(로직) → `models/`(DB). 라우터에 로직을 길게 쓰지 않음 |
| 설정·비밀값 | `app/core/config.py`의 `Settings`로만 읽음. API 키를 코드나 커밋에 넣지 않음(`.env`는 `.gitignore`) |
| 오류 처리 | 외부 API(Gemini, 카카오) 실패 시 기능만 건너뛰고 로그를 남김. 사용자에게는 쉬운 문구로 안내 |
| 주석 | 한국어로 "왜 이렇게 했는지"를 적음 |

실행 명령:

```bash
pip install ruff black
ruff check .          # 문제 찾기
ruff check . --fix    # 자동 수정 가능한 항목 고치기
black .               # 포맷 맞추기
```

## 3. 프론트엔드 (`frontend/`)

| 항목 | 규칙 |
| --- | --- |
| 구성 | 프레임워크 없는 Vanilla JS·HTML·CSS (PWA) |
| 이름 | JS 변수·함수 `camelCase`, HTML `id`는 `camelCase`, CSS 클래스는 `kebab-case` |
| 들여쓰기 | 2칸 |
| 백엔드 주소 | `app.js`·`share.js` 상단 상수에서만 관리 |
| 사용자 문구 | 기술 용어 대신 쉬운 한국어. AI 생성 결과에는 "AI 생성" 표시, 의료 진단 아님 고지 유지 |

## 4. Git 규칙과 브랜치 전략

**브랜치 전략: 단순화한 GitHub Flow(trunk 기반)**

| 브랜치 | 용도 | 예시 |
| --- | --- | --- |
| `main` | 배포되는 기준 브랜치. 직접 push 금지(저장소 개설 턴만 예외) | — |
| `feat/…` | 기능 추가 | `feat/backend`, `feat/frontend` |
| `fix/…` | 버그 수정 | `fix/qa-backend`, `fix/backend-url` |
| `docs/…` | 문서 | `docs/result`, `docs/final` |
| `test/…`, `data/…` | 테스트 기록, 데이터 추출 | `test/round2`, `data/user-test-round2` |

**진행 순서**: 브랜치 생성 → 커밋 → push → PR → 다른 팀원 리뷰(Approve) → **Create a merge commit**으로 Merge

- Squash·Rebase merge는 쓰지 않습니다. 팀원별 커밋 기록(기여 증빙)을 보존하기 위해서입니다.
- 팀원의 PR은 팀장이, 팀장의 PR은 다른 팀원이 리뷰합니다.
- release·hotfix 브랜치는 따로 두지 않습니다. 소규모 팀·단일 배포 환경이라 `main`이 곧 배포본이고, 제출·배포 시점은 **태그**로 표시합니다(`team-start`: 팀 작업 시작, `v-final`: 제출본).
- 긴급 수정도 `fix/…` 브랜치 → PR → 리뷰 순서를 지킵니다.

**커밋 메시지**: `[이름] type: 내용`

- type: `feat` / `fix` / `docs` / `test` / `data` / `refactor`
- 예: `[오주연] docs: 결과 보고서 작성`

**PR 작성**: 제목에 턴 또는 작업 요약, 본문에 변경 내용·확인 방법·연결 Issue(`Closes #번호`)를 적습니다.

## 5. 리팩토링 가이드

**원칙**

1. **동작을 바꾸지 않습니다.** 리팩토링 PR에는 기능 변경을 넣지 않습니다.
2. **작게 나눕니다.** 파일 하나 또는 주제 하나(예: 타입 힌트 표기 통일)씩 PR을 올립니다.
3. **전후를 확인합니다.** 수정 전후로 같은 사진 분석·챗봇·이력 조회를 해 보고 결과가 같은지 PR에 적습니다. 점수 재현성은 `scripts/test_score_reproducibility.py`로 확인합니다.
4. **배포 후 확인합니다.** Merge 후 `GET /health`와 배포 주소 접속을 확인합니다.

**우선순위 (현재 코드 기준)**

| 순위 | 대상 | 이유 |
| --- | --- | --- |
| 1 | CORS 전체 허용(`allow_origins=["*"]`) → 배포 주소만 허용 | 보안 |
| 2 | 분석 실패 시 오류 문구 분리(네트워크 오류와 파일 형식 오류) | 사용성 |
| 3 | ruff B계열 지적(`zip()` strict, 반복문 변수 참조) 확인·수정 | 잠재 버그 |
| 4 | 타입 힌트 표기 통일(`ruff check . --fix`) | 가독성 |
| 5 | 분석 단계 병렬화·캐시 | 성능(NFR-01) |

## 6. 리뷰 체크리스트

- [ ] 커밋 작성자가 본인 GitHub 계정으로 표시되는가
- [ ] 변경 파일이 PR 범위와 맞는가
- [ ] 비밀값(API 키 등)이나 개인정보(얼굴 사진, 이메일)가 포함되지 않았는가
- [ ] Python 변경이 있으면 `ruff check`에서 새 지적이 늘지 않았는가
- [ ] 사용자 화면 문구가 쉬운 한국어이고 AI 생성·의료 진단 아님 고지가 유지되는가
