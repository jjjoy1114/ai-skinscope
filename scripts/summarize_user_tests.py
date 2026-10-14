"""docs/user_test_results.csv를 요약해 docs/test/user_test_summary.md로 저장한다.
실행: python scripts/summarize_user_tests.py  (표준 라이브러리만 사용)"""
import csv
from collections import Counter
from pathlib import Path

SRC = Path("docs/user_test_results.csv")
OUT = Path("docs/test/user_test_summary.md")

rows = [
    {k: (v or "") for k, v in r.items() if k}
    for r in csv.DictReader(SRC.open(encoding="utf-8-sig"))
    if (r.get("created_at") or "").strip()
]
users = {r["user_id"] for r in rows}
scores = [int(r["overall_score"]) for r in rows if r["overall_score"]]
valid = [s for s in scores if s > 0]
ratings = [int(r["satisfaction_rating"]) for r in rows if r["satisfaction_rating"]]
comments = [r for r in rows if r["feedback_comment"].strip()]
derm = sum(r["needs_dermatologist"] == "True" for r in rows)
fb_users = {r["user_id"] for r in rows if r["satisfaction_rating"] or r["feedback_comment"].strip()}
dates = sorted(r["created_at"][:10] for r in rows)

lines = [
    "# 실사용자 테스트 요약",
    "",
    f"- 집계 기간: {dates[0]} ~ {dates[-1]}",
    f"- 총 분석 건수: **{len(rows)}건**, 참여자 **{len(users)}명**",
    f"- 피드백(만족도 또는 의견)을 남긴 참여자: **{len(fb_users)}명**",
    f"- overall_score: 최저 {min(scores)} ~ 최고 {max(scores)}, 평균 {sum(valid) / len(valid):.1f} (0점 {len(scores) - len(valid)}건 제외)",
    f"- needs_dermatologist=True: **{derm}건 ({derm / len(rows) * 100:.0f}%)**",
    f"- 만족도 응답: {len(ratings)}건, 평균 **{sum(ratings) / len(ratings):.1f} / 5**",
    f"- 서술형 피드백: {len(comments)}건",
    "",
    "## 데이터 출처",
    "",
    "- 사전 프로토타입 운영 DB의 `skin_records`를 `scripts/export_feedback.py`로 추출한 `docs/user_test_results.csv` 기준입니다.",
    "- 팀 저장소 배포본(2026-10)은 무료 DB가 만료되어 운영 기록이 남아 있지 않아 이 집계에 포함하지 않았습니다. 배포 후 점검에서 등록한 이슈는 `docs/user_test_round2_issues.csv`에 있습니다.",
]
lines += [
    "",
    "## 만족도 분포",
    "",
    "| 점수 | 건수 |",
    "| --- | --- |",
]
dist = Counter(ratings)
lines += [f"| {k} | {dist.get(k, 0)} |" for k in (5, 4, 3, 2, 1)]
lines += ["", "## 서술형 피드백 원문", "", "| 날짜 | 사용자 | 의견 |", "| --- | --- | --- |"]
for r in comments:
    text = r["feedback_comment"].replace("\n", " ").replace("|", "/")
    lines.append(f"| {r['created_at'][:10]} | {r['user_id']} | {text} |")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:16]))
print(f"\n저장 완료: {OUT}")
