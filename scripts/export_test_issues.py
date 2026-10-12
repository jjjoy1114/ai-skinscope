"""2차 실사용자 테스트에서 등록한 이슈([버그]/[개선])를 CSV로 추출한다.

GitHub 공개 API로 팀 저장소 이슈를 읽어 docs/user_test_round2_issues.csv를 만든다.
DB 재설정 전 2차 테스트 기록이 유실되어, 테스트 중 발견·등록된 이슈를
2차 테스트의 정성 결과 자료로 사용하기 위함이다.
"""
import csv
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

REPO = "jjjoy1114/ai-skinscope"
OUT = Path("docs/user_test_round2_issues.csv")
TITLE_RE = re.compile(r"^\[(버그|개선)\]\s*(.+)$")


def fetch_issues():
    issues, page = [], 1
    while True:
        url = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=30) as res:
            batch = json.load(res)
        if not batch:
            return issues
        issues += [i for i in batch if "pull_request" not in i]
        page += 1


def main():
    rows = []
    for issue in fetch_issues():
        m = TITLE_RE.match(issue["title"])
        if not m:
            continue
        labels = [l["name"] for l in issue["labels"]]
        area = "backend" if "backend" in labels else "frontend" if "frontend" in labels else "기타"
        rows.append({
            "issue_no": issue["number"],
            "type": m.group(1),
            "area": area,
            "title": m.group(2),
            "state": "해결" if issue["state"] == "closed" else "진행 중",
            "opened_at": issue["created_at"][:10],
            "closed_at": (issue["closed_at"] or "")[:10],
            "url": issue["html_url"],
        })
    rows.sort(key=lambda r: r["issue_no"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["issue_no"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"추출 완료: {OUT} ({len(rows)}건)")
    for key in ("type", "area", "state"):
        print(f"- {key}별:", dict(Counter(r[key] for r in rows)))
    for r in rows:
        print(f"  #{r['issue_no']} [{r['type']}/{r['area']}/{r['state']}] {r['title']}")


if __name__ == "__main__":
    sys.exit(main())
