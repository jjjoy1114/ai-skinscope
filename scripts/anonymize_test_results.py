"""실사용자 테스트 원본에서 팀원 기록을 제외하고 사용자 ID를 가명(T1, T2…)으로 바꾼다.

- 입력: docs/user_test_results.csv (원본, user_id 포함)
- 출력: 같은 파일을 덮어씀 (user_id 열 → tester 열)
- 팀원 ID는 TEAM_IDS에 넣는다. ID 목록 자체는 저장소에 남기지 않도록
  실행할 때 환경변수 TEAM_IDS="id1,id2"로 전달한다.
"""
import csv
import os
from pathlib import Path

SRC = Path("docs/user_test_results.csv")
team_ids = {x.strip() for x in os.environ.get("TEAM_IDS", "").split(",") if x.strip()}

rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
if "user_id" not in rows[0]:
    raise SystemExit("이미 가명 처리된 파일입니다 (user_id 열 없음).")

kept = [r for r in rows if r["user_id"] not in team_ids]
kept.sort(key=lambda r: r["created_at"])
alias = {}
for r in kept:
    alias.setdefault(r["user_id"], f"T{len(alias) + 1}")

fields = ["id", "tester"] + [f for f in rows[0].keys() if f not in ("id", "user_id")]
with SRC.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in kept:
        r = dict(r)
        r["tester"] = alias[r["user_id"]]
        del r["user_id"]
        w.writerow({k: r[k] for k in fields})

print(f"원본 {len(rows)}건 → 팀원 제외 {len(rows) - len(kept)}건 → 남은 {len(kept)}건, 참여자 {len(alias)}명")