# Must 기능 3회 검증 결과 (턴 16)

- 관련 이슈: [#35](https://github.com/jjjoy1114/ai-skinscope/issues/35)
- 담당: 조민경
- 대상: https://ai-skinscope-team.vercel.app
- 판정 기준: [`기능요구명세서.md`](../기능요구명세서.md) 10장 "구현 현황" 표의 **확인 방법·기대 결과**. 3회 시도 중 2회 이상 기대 결과가 나오면 **충족**
- 개인정보: 명세서 4장 규칙에 따라 캡처·영상 속 얼굴과 휴대폰 앨범·파일 목록은 흐림 처리함

## 1. 시도 기록

| 회차 | 일시 | 환경 | 입력 | 사진 | 결과 | 이력 |
|---|---|---|---|---|---|---|
| 1회 | 10/16 16:30 | Android · 삼성 인터넷 | 나이·성별 미입력 | 사진 A (갤러리 업로드) | 73점 | SCAN 001 |
| 2회 | 10/16 16:33 | 〃 | 39세 · 여성 | 사진 B (갤러리 업로드) | 82점, 피부나이 31세 | SCAN 002 |
| 3회 | 10/16 16:35 | 〃 | 30세 · 여성 | 사진 B (화면에 남아 있던 사진 재분석) | 83점, 피부나이 22세 | SCAN 003 |
| 추가 (V2) | 10/17 10:44 | Android · 홈 화면 앱(PWA), 갱신된 화면 | 나이(비공개) · 여성 | 사진 C (카메라 촬영) | 75점 | 새 ID |
| 추가 (V3) | 10/17 업로드 영상 | Android · 크롬(동의 기록이 없는 브라우저) | - | - | 동의 절차만 검증 | - |

- 1~3회는 같은 ID, 같은 배포 버전에서 진행함
- 추가 V2·V3은 화면 테마가 바뀐 이후 버전에서 진행함

## 2. 판정 요약

| FR | 기능 | 1회 | 2회 | 3회 | 추가 | 판정 |
|---|---|---|---|---|---|---|
| FR-01 | 사진 촬영/업로드 | ✅ | ✅ | ➖ | ✅ (V2 촬영) | **충족** |
| FR-02 | 촬영 전 동의 | ✅ | ➖ | ➖ | ✅ (V3) | **충족** |
| FR-03 | AI 이미지 분석 | ✅ | ✅ | ✅ | ✅ (V2) | **충족** |
| FR-04 | 피부 건강 점수 | ✅ | ✅ | ✅ | ✅ (V2) | **충족** |
| FR-05 | 유사 증상 패턴 안내 | ✅ | ❌ | ❌ | ✅ (V2) | **확인 필요** |
| FR-06 | 전문의 상담 권장·병원 검색 | ❌ | ❌ | ❌ | ❌ (V2) | **미충족 (조건 미발생)** |
| FR-07 | 관리 코칭 메시지 | ✅ | ✅ | ✅ | ✅ (V2) | **충족** |
| FR-08 | 이력 저장 | ✅ | ✅ | ✅ | - | **충족** |
| FR-09 | 변화 추적 | ➖ | ✅ | ✅ | - | **충족** |
| FR-10 | 사용자 피드백 수집 | ✅ | ➖ | ➖ | - | **추가 검증 필요** |

✅ 기대 결과 확인 / ❌ 기대 결과와 다름 / ➖ 해당 회차에서 동작을 수행하지 않음(성공 횟수에 포함하지 않음)

**충족 7개 · 확인 필요 1개(FR-05) · 추가 검증 필요 1개(FR-10) · 미충족 1개(FR-06)**

FR-05·FR-06은 이슈 #35 기준(X 2회 이상)에 해당해 단톡방 공유 대상임.

## 3. 항목별 상세

### FR-01 사진 촬영/업로드 — 충족
- 확인 방법: '스캔' 화면에서 동의 후 촬영하거나 '갤러리에서 사진 선택' → '이 사진으로 분석하기'
- 기대 결과: '분석 중...' 표시 후 결과 화면으로 이동
- 1·2회: 갤러리 업로드 → 분석 → 결과 이동 확인
- 3회: 새 사진을 올리지 않고 화면에 남아 있던 2회 사진으로 분석해 성공 횟수에서 제외 (아래 5장 결함 후보 4)
- 추가 V2: 카메라 촬영 → 미리보기 → 분석 → 결과 이동 확인 (촬영 경로)

### FR-02 촬영 전 동의 — 충족
- 확인 방법: 동의하지 않은 상태에서 '촬영' 또는 '갤러리에서 사진 선택' 누르기
- 기대 결과: 촬영·파일 선택을 진행하지 않고 '동의해 주셔야 분석할 수 있어요' 안내 표시
- 1회: 갤러리 버튼 → 진행되지 않고 안내 표시 확인
- 2·3회: 동의 화면이 다시 나오지 않음(1회 동의 상태가 저장된 것으로 보임) → 제외
- 추가 V3: 동의 기록이 없는 크롬에서 촬영 버튼을 여러 번 눌러도 촬영되지 않고 안내 표시 확인

### FR-03 AI 이미지 분석 — 충족
- 기대 결과: 모공·탄력·수분·주름·색소침착·붉은기 6개 항목 점수 표시

| 회차 | 모공 | 탄력 | 수분 | 주름 | 색소침착 | 붉은기 |
|---|---|---|---|---|---|---|
| 1회 | 70 | 61 | 79 | 69 | 78 | 70 |
| 2회 | 78 | 72 | 80 | 85 | 82 | 82 |
| 3회 | 80 | 78 | 82 | 85 | 82 | 80 |
| V2 | 68 | 50 | 83 | 83 | 73 | 70 |

### FR-04 피부 건강 점수 — 충족
- 기대 결과: 종합 점수(0~100점)와 등급 배지 표시
- 73 / 82 / 83 / 75점과 등급 배지 확인: 73·75점은 "매우양호", 82·83점은 "백옥 피부 미녀(미남)"
- 배지 구간이 코드 기준(`frontend/app.js` `overallScoreTier`: 71~80점 매우양호, 81점 이상 백옥 피부 미녀)과 일치함

### FR-05 유사 증상 패턴 안내 — 확인 필요
- 기대 결과: 'SKIN 패턴 분석' 카드에 패턴 이름·유사도(%)와 진단이 아니라는 고지
- 1회: "아토피피부염 유사도 35%" + 진단 아님 고지 → 기대 결과와 일치
- 2·3회: "사진에서 특별히 두드러진 질환 패턴은 발견되지 않았습니다"만 표시되고 패턴 이름·유사도 없음
- V2: "지루피부염 유사도 45%" 표시
- 판단: 패턴이 없을 때의 안내를 정상 동작으로 볼지에 따라 판정이 달라짐 → 팀 결정 필요

### FR-06 전문의 상담 권장·병원 검색 — 미충족 (조건 미발생)
- 확인 방법: 위치 접근을 허용하고 분석. 종합 점수 40점 이하 또는 AI가 상담 필요로 판단하는 결과 확인
- 기대 결과: 전문의 상담 권장 문구, 위치가 있으면 '근처 피부과' 목록
- 결과: 4번 모두 73~83점이고 AI도 상담 필요로 판단하지 않아 상담 권장·병원 목록이 나오지 않음 (`agent_service.py`의 40점 규칙과 일치하는 정상 동작)
- 참고: 결과 하단의 "정확한 의학적 진단은 반드시 피부과 전문의와 상담하시기 바랍니다"는 모든 결과에 나오는 고정 안내문이라 FR-06 증거로 세지 않음
- 후속: Render 카카오 키 설정 확인(서경환) 후, 조건을 충족하는 테스트 사진으로 재검증 필요

### FR-07 관리 코칭 메시지 — 충족
- 기대 결과: '맞춤 스킨케어 팁' 카드에 분석 결과에 맞는 관리 팁 표시
- 4번 모두 표시. 결과에 따라 소견과 팁 내용이 달라짐(예: 1회·V2 소견 "모공 관리에 집중해보세요", 2회 "꾸준한 수분 보습과 자외선 차단 케어", 3회 "데일리 보습 관리")

### FR-08 이력 저장 — 충족
- 기대 결과: 하단 '이력' 탭에 방금 기록이 날짜·점수와 함께 표시
- 2회 후 SCAN 001(73)·002(82), 3회 후 SCAN 001~003(73·82·83) 확인 → 3번 분석 모두 저장됨

### FR-09 변화 추적 — 충족
- 기대 결과: 같은 ID로 2회 이상 분석 후 '이력' 탭 TREND 배너에 직전 기록 대비 점수 변화 표시
- 1회: 비교할 이전 기록 없음
- 2회: TREND +9 (73 → 82) 확인
- 3회: TREND +1 (82 → 83) 확인
- 참고: 3회는 2회와 같은 사진이라 "실제 피부 변화"를 보여주는 사례는 아님 (화면 기능 자체는 정상)

### FR-10 사용자 피드백 수집 — 추가 검증 필요
- 확인 방법: 결과 화면 '이 결과가 도움이 되었나요?'에서 1~5 선택 → '피드백 보내기'
- 기대 결과: "소중한 의견 감사합니다!" 표시
- 1회: 5점 선택 → 전송 → 감사 메시지 확인
- 2·3회: 피드백을 보내지 않아 기록 없음 (실패가 아님)
- 후속: 결과 화면에서 2회 추가 전송 후 이 문서에 반영

## 4. 증빙 자료

사진은 [`docs/screenshots/process/`](../screenshots/process/)의 `T16-MK-1` ~ `T16-MK-17`이며 **기대 결과가 나온 성공 화면만** 담았습니다. 영상은 `must_evidence` 폴더에 있으며, 폴더 안 README에 사진·영상별 검증 내용을 정리했습니다. 사진으로 결과가 보이는 항목은 사진으로, 누르는 순서가 증거인 항목(FR-01, FR-02)과 결함 후보 4는 영상으로 남겼습니다.

| FR | 사진 | 영상 (`must_evidence` 폴더) |
|---|---|---|
| FR-01 | <img src="../screenshots/process/T16-MK-1.png" width="110"> <img src="../screenshots/process/T16-MK-2.png" width="110"> <img src="../screenshots/process/T16-MK-3.png" width="110"> <img src="../screenshots/process/T16-MK-4.png" width="110"> | `T1_FR01_upload_result.mp4`, `C5_FR01_T2_upload.mp4`, `V2_FR01_camera_result.mp4` |
| FR-02 | <img src="../screenshots/process/T16-MK-5.png" width="110"> <img src="../screenshots/process/T16-MK-6.png" width="110"> | `C1_FR02_consent_block.mp4`, `V3_FR02_consent_retest.mp4` |
| FR-03·04 | <img src="../screenshots/process/T16-MK-7.png" width="110"> <img src="../screenshots/process/T16-MK-8.png" width="110"> <img src="../screenshots/process/T16-MK-9.png" width="110"> <img src="../screenshots/process/T16-MK-10.png" width="110"> | - |
| FR-05 | <img src="../screenshots/process/T16-MK-11.png" width="110"> <img src="../screenshots/process/T16-MK-12.png" width="110"> | - |
| FR-06 | 성공 화면 없음 (조건 미발생, 3장 참고) | - |
| FR-07 | <img src="../screenshots/process/T16-MK-11.png" width="110"> <img src="../screenshots/process/T16-MK-13.png" width="110"> <img src="../screenshots/process/T16-MK-14.png" width="110"> <img src="../screenshots/process/T16-MK-12.png" width="110"> | - |
| FR-08·09 | <img src="../screenshots/process/T16-MK-15.png" width="110"> <img src="../screenshots/process/T16-MK-16.png" width="110"> | - |
| FR-10 | <img src="../screenshots/process/T16-MK-17.png" width="110"> | - |
| 결함 후보 4 | - | `D5_photo_retained.mp4` |

## 5. 검증 중 발견한 사항

| # | 내용 | 관련 | 비고 |
|---|---|---|---|
| 1 | 이력 시각이 한국 시간이 아닌 UTC로 표시됨 (실제 16:30 → 화면 07:30) | FR-08 | 결함 후보 |
| 2 | 같은 사진(2·3회)인데 점수가 82 → 83, 탄력 72 → 78 등으로 달라져 "1점 개선"으로 안내됨 | FR-03·04·09, NFR-07 | 배포 점검 로그(턴 7)의 "같은 사진 반복 시 76~83점 변동"과 같은 기존 한계 |
| 3 | 3회 이력 화면에서 TREND(+1)는 직전 기록 대비, 항목별 변화(모공 +10 등)는 첫 기록 대비로 계산되어 비교 기준이 섞임 | FR-09 | 의도 확인 필요 |
| 4 | 이력 탭에 다녀와도 직전 사진이 스캔 화면에 남아 있어, 새 사진 없이 같은 사진이 다시 분석·저장될 수 있음 | FR-01·08·09 | 결함 후보, 영상 `D5_photo_retained.mp4` |
| 5 | 나이 미입력 시 피부나이 자리에 "실제 나이가 입력되지 않아 분석할 수 없습니다"가 표시됨 (명세 FR-13은 "표시하지 않음") | FR-13 (Should) | 턴 7 배포 점검(3번)에서는 정상으로 판정됨. 명세 문구와의 차이만 기록, Must 판정과 무관 |

## 제출 증빙 파일 링크

### 사진 증빙 (17장)
- [FR01_T1_upload.jpg](captures/FR01_T1_upload.jpg)
- [FR01_T2_upload.jpg](captures/FR01_T2_upload.jpg)
- [FR01_V2_camera_live.jpg](captures/FR01_V2_camera_live.jpg)
- [FR01_V2_camera_preview.jpg](captures/FR01_V2_camera_preview.jpg)
- [FR02_T1_block_unchecked.jpg](captures/FR02_T1_block_unchecked.jpg)
- [FR02_T1_consent.jpg](captures/FR02_T1_consent.jpg)
- [FR03-04_T1_score_6items.jpg](captures/FR03-04_T1_score_6items.jpg)
- [FR03-04_T2_score_6items.jpg](captures/FR03-04_T2_score_6items.jpg)
- [FR03-04_T3_score_6items.jpg](captures/FR03-04_T3_score_6items.jpg)
- [FR03-04_V2_score_6items.jpg](captures/FR03-04_V2_score_6items.jpg)
- [FR05-07_T1_pattern_tips.jpg](captures/FR05-07_T1_pattern_tips.jpg)
- [FR05-07_V2_pattern_tips.jpg](captures/FR05-07_V2_pattern_tips.jpg)
- [FR07_T2_tips.jpg](captures/FR07_T2_tips.jpg)
- [FR07_T3_tips.jpg](captures/FR07_T3_tips.jpg)
- [FR08-09_after_T2_history.jpg](captures/FR08-09_after_T2_history.jpg)
- [FR08-09_after_T3_history.jpg](captures/FR08-09_after_T3_history.jpg)
- [FR10_T1_feedback_sent.jpg](captures/FR10_T1_feedback_sent.jpg)

### 영상 증빙 (6개)
- [C1_FR02_consent_block.mp4](must_evidence/C1_FR02_consent_block.mp4)
- [C5_FR01_T2_upload.mp4](must_evidence/C5_FR01_T2_upload.mp4)
- [D5_photo_retained.mp4](must_evidence/D5_photo_retained.mp4)
- [T1_FR01_upload_result.mp4](must_evidence/T1_FR01_upload_result.mp4)
- [V2_FR01_camera_result.mp4](must_evidence/V2_FR01_camera_result.mp4)
- [V3_FR02_consent_retest.mp4](must_evidence/V3_FR02_consent_retest.mp4)
