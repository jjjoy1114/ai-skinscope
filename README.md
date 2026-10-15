# AI-SkinScope

AI 피부 상태 스크리닝 & 코칭 서비스 — 스마트폰 카메라로 얼굴을 촬영하면 AI가 피부 상태를 분석해 점수와 참고용 관리 가이드를 제공하고, 시간에 따른 변화를 추적해주는 개인 피부 코칭 웹앱입니다.

> ⚠️ 본 서비스는 **AI 참고용 스크리닝**이며 의료 진단이 아닙니다. 정확한 진단은 피부과 전문의와 상담하세요.

🔗 배포 주소: **<https://ai-skinscope-team.vercel.app>**

경남 코디세이(Gyeongnam Codyssey) AI 네이티브 과정 Final Project(팀미션 3-3) 산출물입니다. 2026년 8~9월에 사전 구성한 팀이 프로토타입을 만들고 사용자 테스트를 수행하며 개선 과정을 준비했고, 그 결과를 바탕으로 10월에 3명이 팀 저장소에서 역할을 나눠 다시 구성했습니다.

---

## 1. 프로젝트 소개

피부에 트러블(여드름, 붉은기, 각질, 건조 등)이 생겼을 때 병원에 갈 정도인지 스스로 판단하기 어렵다는 문제에서 출발했습니다. 인터넷 검색은 정보가 파편적이고, 병원은 매번 가기엔 시간·비용 부담이 있습니다. AI-SkinScope는 사진 한 장으로 즉시 참고용 스크리닝 결과와 관리 가이드를 제공하고, 촬영 이력을 누적해 변화를 추적할 수 있게 합니다.

자세한 문제 정의·페르소나·요구사항은 [`docs/Service기획서.md`](docs/Service기획서.md), 확장 기능 설계는 [`docs/개선 과정 작업지시서/PRODUCT_ROADMAP_V2.md`](<docs/개선 과정 작업지시서/PRODUCT_ROADMAP_V2.md>)를 참고하세요.

## 2. 주요 기능

| 기능 | 설명 |
| --- | --- |
| 사진 촬영/업로드 | 폰 카메라 즉시 촬영 또는 갤러리 업로드, 전면 카메라 미러링·촬영 가이드 오버레이 제공 |
| 얼굴 자동 정렬 감지 | 브라우저 `FaceDetector` 또는 `@mediapipe/tasks-vision` 폴백으로 얼굴 위치를 인식해 조건 충족 시 자동 촬영 |
| AI 피부 분석 | Gemini Vision으로 모공·탄력·수분·주름·색소침착·붉은기 6개 항목과 종합 점수(overall_score) 산출 |
| 부위별 분석 | 이마·코·양볼·턱 5개 구역별 모공·유분·트러블 상태를 별도로 제공 |
| 나이·동년배 비교, 피부나이 | 나이·성별(선택 입력) 기반으로 동년배 평균과 비교하고, 실측 데이터 기반 "피부나이"를 제시(신뢰도 낮은 경우 안내 문구로 대체) |
| 유사 증상 패턴 안내 | 건선/아토피/여드름/지루피부염/주사 5종 패턴과의 유사도 안내(진단 아님 고지 포함) |
| 전문의 상담 권장 + 병원 검색 | 심각도 임계값 초과 시 카카오맵 API로 인근 피부과 검색 |
| 맞춤 성분 추천 | 취약 항목 기준 성분을 특이도(specificity) 스코어링으로 추천, 쇼핑 검색 링크 제공 |
| 퍼스널컬러 추천 | 분석 사진 기반 피부 톤에 어울리는 컬러 팔레트 제안 |
| 자외선 지수 연동 | 현재 위치 기준 UV 지수·행동 요령 안내(OpenWeatherMap) |
| 피부지식 챗봇 | 분석 결과에 대해 자유롭게 질문하면 RAG 기반으로 답변(의료 진단성 질문은 전문의 상담 권유로 안내) |
| 결과 공유 | Web Share API 또는 클립보드 복사로 점수·요약 공유(원본 사진 미포함) |
| 이력 관리 (Long-term Memory) | 사용자별 촬영 기록 저장, 개별 기록 삭제, 만족도/의견 피드백 수집 |
| 이력 분석 리포트 | "이력분석" 버튼 클릭 시 모공·탄력·수분·주름·색소침착·붉은기 6개 항목 + 종합점수의 전체 기간 변화 그래프와, 그 추세에 따른 AI 생성 관리 피드백 제공 |
| PWA 설치 | iOS/Android 홈 화면 설치, 오프라인 캐싱(분석·이력·공유 API는 항상 네트워크 우선) |

## 3. AI 활용 방식

Final Project 요구 기술 요소(5종 중 2개 이상) 중 4개를 충족합니다.

| 기술 요소 | 적용 내용 |
| --- | --- |
| 멀티모달 AI | Gemini Vision으로 얼굴 사진에서 구조화된 피부 특징을 직접 추출 |
| RAG (Retrieval-Augmented Generation) | ① 질환 유사사례 임베딩 검색, ② 인구 통계 실측 프로필 검색 — 두 인덱스를 top-5 코사인 유사도로 조회해 프롬프트 근거로 주입. ③ 피부지식 챗봇은 별도 지식베이스(FAQ+성분 매핑)를 RAG로 검색해 답변 |
| AI Agent | 분석 결과를 바탕으로 점수 산출 → 전문의 상담 필요 여부 판단 → 필요 시 카카오맵 병원 검색 "도구"를 자율 호출 |
| Long-term Memory | 사용자별 촬영 이력을 DB에 누적해 변화 추적과 동년배 비교에 활용 |

## 4. 기술 스택

| 구분 | 기술 |
| --- | --- |
| Backend | FastAPI, SQLAlchemy, SQLite(개발) / PostgreSQL(배포) |
| AI | Google Gemini Vision(`gemini-3.6-flash`, fallback `gemini-3.5-flash-lite`), `gemini-embedding-2`(768차원, RAG용) |
| Frontend | Vanilla JS/HTML/CSS 기반 PWA (프레임워크·번들러 없음) |
| 외부 API | 카카오맵 로컬 검색(병원 검색), OpenWeatherMap(자외선 지수) |
| 배포 | 프론트엔드 Vercel, 백엔드 Render |
| 데이터 | AI Hub "한국인 피부상태 측정 데이터", "안면부 피부질환 이미지 합성 데이터" (자세한 사용 범위는 `docs/Service기획서.md` 4장 참고) |

시스템 아키텍처는 [`docs/기능요구명세서.md`](docs/기능요구명세서.md) 7장, 기술 스택 선정 이유는 같은 문서 8장에 있습니다.

AI Hub 세 데이터셋의 분석·추출 과정과 결과 수치는 [`docs/AI_HUB_데이터분석.md`](docs/AI_HUB_데이터분석.md)에 있습니다.

## 5. 폴더 구조

```text
AI-SkinScope/
├── app/                      # FastAPI 백엔드
│   ├── core/                 # 설정(config.py)
│   ├── models/                # SQLAlchemy 모델
│   ├── routers/                # API 라우터 (analyze, history, share, uv, chat)
│   ├── schemas/                # Pydantic 스키마
│   ├── services/                # 비전 분석, RAG, 에이전트, 챗봇, 성분추천 등 핵심 로직
│   └── data/                    # 사전 계산된 참고 인덱스(JSON)
├── frontend/                  # PWA (index.html, app.js, styles.css, manifest, service-worker)
├── scripts/                    # 참고 데이터 빌드 스크립트, 로컬 HTTPS 서버, 재현성 테스트
├── docs/                        # 기획서·로드맵·스펙·테스트 로그
└── requirements.txt
```

## 6. 실행 방법

### 사전 준비

```bash
python -m venv venv
```

```bash
venv\Scripts\activate   (Windows) 또는 source venv/bin/activate (macOS/Linux)
```

```bash
pip install -r requirements.txt
```

`.env.example`을 `.env`로 복사한 뒤 아래 값을 채웁니다.

```bash
GEMINI_API_KEY=...       # Google AI Studio에서 발급
KAKAO_MAP_API_KEY=...    # 병원 검색용 (선택 — 없으면 병원 검색 기능만 비활성화)
UV_API_KEY=...           # OpenWeatherMap 무료 티어 (선택 — 없으면 자외선 지수 기능만 비활성화)
DATABASE_URL=sqlite:///./skinscope.db
```

### 서버 실행

```bash
uvicorn app.main:app --reload
```

카메라 접근은 브라우저 보안 정책상 HTTPS(또는 localhost)에서만 허용됩니다. 로컬 네트워크의 다른 기기(휴대폰)로 테스트하려면 `scripts/serve_https.py`로 자체 서명 인증서(`certs/`) 기반 HTTPS 서버를 띄워 사용합니다.

```bash
python scripts/serve_https.py
```

### 참고 데이터 재생성 (필요 시)

`app/data/*.json`은 사전에 계산된 참고 인덱스입니다. AI Hub 원본 데이터를 다시 받아 처음부터 빌드하려면 `scripts/build_*.py` 스크립트들을 참고하세요(원본 데이터셋 접근 방법은 `docs/Service기획서.md` 4장 참고).

## 7. 팀 구성과 기여

| 이름 | 역할 | 본인 기여 요약 (본인 작성) | 대표 커밋·PR·문서 |
| --- | --- | --- | --- |
| 오주연 | 팀장, 데이터·QA | 팀 저장소를 만들고 턴 방식(브랜치 → PR → 리뷰 → Merge)으로 진행을 이끌었습니다. 기능 요구 명세서와 AI Hub 데이터 분석 문서를 쓰고, 배포본을 점검해 이슈 5건(#16~#20)을 등록했습니다. 팀원 PR을 리뷰·Merge하고 결과 보고서와 README를 정리했으며, 1차 평가 후 사용자 피드백 기록과 제출물 보완을 맡았습니다. | [명세서](docs/기능요구명세서.md) · [데이터 분석](docs/AI_HUB_데이터분석.md) · [결과 보고서](docs/Result.md) · [피드백 기록](docs/test/user_feedback.md) · [PR #11](https://github.com/jjjoy1114/ai-skinscope/pull/11) · [PR #26](https://github.com/jjjoy1114/ai-skinscope/pull/26) · [PR #38](https://github.com/jjjoy1114/ai-skinscope/pull/38) |
| 서경환 | Backend/AI | 서비스 기획서를 쓰고, Gemini Vision 분석·RAG 3종·Agent·이력 기반 피드백·챗봇으로 이어지는 백엔드와 AI 파이프라인을 구현했습니다. 프로토타입 단계에서 AI Hub 원본 데이터를 추출하고 Render에 백엔드를 배포했으며, 배포 후 백엔드 이슈 3건(#16~#18)을 수정하고 기술적용 매뉴얼을 정리했습니다. 1차 평가 후에는 실사용자 테스트 데이터의 팀원 기록 제외·가명 처리와 명세서 AI 활용 코드 위치·구현 현황 표를 맡았습니다. | [기획서](docs/Service기획서.md) · [기술적용 매뉴얼](docs/AI_Skin_Scope_기술적용_매뉴얼.md) · [PR #13](https://github.com/jjjoy1114/ai-skinscope/pull/13) · [PR #22](https://github.com/jjjoy1114/ai-skinscope/pull/22) · [PR #37](https://github.com/jjjoy1114/ai-skinscope/pull/37) |
| 조민경 | Frontend | 프론트엔드 화면과 PWA 기능의 구현 및 검증 작업에 참여했습니다. 촬영 전 동의와 AI 생성 고지 등 사용자 화면을 점검하고, 백엔드 주소 변경에 대응했으며 배포 후 프론트엔드 이슈 2건(#19, #20)을 수정했습니다. 브라우저와 스마트폰 실기기에서 주요 화면을 검증하고 테스트 증빙을 정리했습니다. 1차 평가 후에는 기능요구명세서의 프론트엔드 구현 현황을 검토하고, 이력 조회(FR-11), 근거 설명(FR-17), 자동 촬영(FR-18)의 실제 검증 결과를 반영했습니다. |[PR #14](https://github.com/jjjoy1114/ai-skinscope/pull/14) · [PR #15](https://github.com/jjjoy1114/ai-skinscope/pull/15) · [PR #24](https://github.com/jjjoy1114/ai-skinscope/pull/24) · [PR #39](https://github.com/jjjoy1114/ai-skinscope/pull/39)|
> 커밋 수(Merge 커밋 제외, 최종): 오주연 __ · 서경환 __ · 조민경 __ (`git shortlog -sn --no-merges team-start..main`)

턴 방식(한 번에 한 명 작업 → PR → 리뷰 → Merge)으로 진행했습니다. 턴별 작업 내용과 PR 기록은 [`docs/Result.md`](docs/Result.md) 6절에 있습니다.

브랜치 전략(GitHub Flow: `main` 보호, 작업 브랜치 → PR → 리뷰 → merge commit, 태그로 제출본 표시), 코드 컨벤션(black·ruff, 설정은 [`pyproject.toml`](pyproject.toml)), 리팩토링 가이드는 [`docs/CODE_CONVENTION.md`](docs/CODE_CONVENTION.md)에 정리했습니다.

## 8. AI 윤리 및 개인정보

- 모든 분석 결과 화면에 "AI 참고용 스크리닝이며 의료 진단이 아님"을 상시 고지합니다.
- 건강 점수, 유사 증상 카테고리, 챗봇 답변은 모두 AI 생성 콘텐츠임을 화면에 표기합니다(`is_ai_generated` 배지 등).
- 피부 사진·건강 정보는 민감정보로 간주해 촬영 전 명시적 동의를 받습니다(동의 전에는 촬영·갤러리 선택 차단).
- 얼굴 사진은 분석에만 사용하고 서버에 저장하지 않습니다. 이력에는 익명 ID와 분석 결과만 남으며, 사용자가 기록을 직접 삭제할 수 있습니다.
- 실사용자 테스트에는 AI Hub 원본 이미지가 아닌, 동의를 받은 실제 테스터 본인 사진만 사용했습니다.

자세한 결과와 알려진 한계는 [`docs/Result.md`](docs/Result.md), 서비스 기획 전체 내용은 [`docs/Service기획서.md`](docs/Service기획서.md), 기능/비기능 요구사항과 AI 활용 명세는 [`docs/기능요구명세서.md`](docs/기능요구명세서.md)를 참고하세요.

## 9. 사용자 테스트 결과

실사용자 40명(팀원 제외)이 154건을 분석했고 만족도는 평균 4.3/5였습니다. 의견 9개 요지 중 7개를 기능으로 반영하고 1개를 일부 반영했으며, 팀 배포 후 점검에서 찾은 이슈 5건(#16~#20)도 모두 수정했습니다.

통계와 피드백 원문은 [`docs/test/user_test_summary.md`](docs/test/user_test_summary.md), 반영 결과와 배포 후 수정 내역은 [`docs/Result.md`](docs/Result.md) 4절을 참고하세요.

## 10. 링크

- 배포: <https://ai-skinscope-team.vercel.app>
- 결과 보고서: [`docs/Result.md`](docs/Result.md)
- 기술적용 매뉴얼: [`docs/AI_Skin_Scope_기술적용_매뉴얼.md`](docs/AI_Skin_Scope_기술적용_매뉴얼.md)
- 코드 컨벤션·브랜치 전략·리팩토링 가이드: [`docs/CODE_CONVENTION.md`](docs/CODE_CONVENTION.md)
- 운영 가이드(서버 깨우기 계획·정기 점검·DB 백업·장애 대응): [`docs/OPERATIONS.md`](docs/OPERATIONS.md)
