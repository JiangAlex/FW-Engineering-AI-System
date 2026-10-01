#!/usr/bin/env python3
"""Daily mail-content report for FW-Engineering-AI-System.

Analyzes the **last 7 days of engineering mail** (per-model progress / issues /
risks), NOT the system's own health. Reuses report_service.generate_weekly_report
(Map-Reduce over recent mail via the local LLM), writes the result under
DailyReport/, and records it to Redmine.

Redmine modes (env REPORT_REDMINE_MODE):
  - "append" (default): add today's report as a NOTE on a single long-lived
    issue (env REPORT_REDMINE_ISSUE_ID).
  - "new": open a fresh issue each day.

Env:
  REDMINE_URL, REDMINE_API_KEY        Redmine access (required to post)
  REPORT_REDMINE_PROJECT_ID           default 24 (FW-Engineering-AI-System)
  REPORT_REDMINE_MODE                 append | new   (default append)
  REPORT_REDMINE_ISSUE_ID             target issue id for append mode
  REPORT_DAYS                         analysis window in days (default 7)
"""

import os
import sys
import json
import datetime
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "DailyReport"

sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------------------------------
#  Mail-content analysis (reuses the weekly report engine over recent mail)
# --------------------------------------------------------------------------
def _recent_dailyreports(days: int):
    """Return list of (date_str, path) for DailyReport/*.md within the last `days`
    days (excluding today's own file), newest first. Only real daily reports
    (YYYY-MM-DD.md), not stats sidecars.
    """
    import re
    out = []
    if not REPORT_DIR.is_dir():
        return out
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=days)
    for p in REPORT_DIR.glob("*.md"):
        m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})", p.stem)
        if not m:
            continue
        d = datetime.date.fromisoformat(m.group(1))
        if cutoff <= d < today:  # exclude today (being generated now)
            out.append((m.group(1), p))
    out.sort(reverse=True)
    return out


def build_week_report(days: int) -> tuple[str, bool, str]:
    """Produce the weekly analysis. Prefer aggregating the last `days` days of
    existing DailyReports; if those don't cover a full week, fall back to
    analyzing the last `days` days of mail directly.

    Returns (markdown_body, ok, source_label).
    """
    reports = _recent_dailyreports(days)
    # "covers a full week" = at least `days` distinct daily reports present.
    if len(reports) >= days:
        return _aggregate_dailyreports(reports, days)
    # Fallback: analyze mail directly.
    body, ok = build_mail_report(days)
    return body, ok, f"最近 {days} 天 mail（DailyReport 不足一週，僅 {len(reports)} 份）"


def _aggregate_dailyreports(reports, days: int) -> tuple[str, bool, str]:
    """LLM-aggregate the last `days` DailyReports into one weekly analysis."""
    try:
        from src.core.local_llm import LocalAIClient
    except Exception as e:
        return f"❌ 無法載入 LLM 模組：{e}", False, "DailyReport 彙整"
    client = LocalAIClient.get_instance()
    if client is None or not client.is_ready:
        return "❌ 本地 LLM 無法連線，無法彙整 DailyReport。", False, "DailyReport 彙整"

    blocks = []
    for d, p in reports:
        try:
            blocks.append(f"### {d}\n{p.read_text(encoding='utf-8')[:3000]}")
        except Exception:
            continue
    from src.core.prompts import daily_aggregate
    prompt = daily_aggregate(days, chr(10).join(blocks))
    ans = client.ask(prompt)
    if ans and not ans.startswith(("❌", "⚠️")):
        return ans.strip(), True, f"彙整最近 {len(reports)} 份 DailyReport"
    return (ans or "❌ 彙整產生空內容。"), False, "DailyReport 彙整"


def build_mail_report(days: int) -> tuple[str, bool]:
    """Return (markdown_report, ok). Analyzes the last `days` days of mail.

    ok=False means the analysis could not be produced (no mail / LLM down);
    the returned string then explains why.
    """
    try:
        from src.core.local_llm import LocalAIClient
        from src.services.report_service import ReportService
    except Exception as e:
        return f"❌ 無法載入分析模組：{e}", False

    client = LocalAIClient.get_instance()
    if client is None or not client.is_ready:
        return "❌ 本地 LLM（Ollama）無法連線，無法產生郵件分析。", False

    result = ReportService.generate_weekly_report(client, days=days)
    # generate_weekly_report returns (content, filename) on success, or an
    # error string (e.g. no mail in window).
    if isinstance(result, tuple):
        content, _fname = result
        if content and not content.startswith(("❌", "⚠️")):
            return content, True
        return (content or "❌ 分析產生空內容。"), False
    return str(result), False


def build_report(date_str: str, days: int, body: str, ok: bool, source: str) -> str:
    wd = "一二三四五六日"[datetime.date.today().weekday()]
    status = "" if ok else "\n> ⚠️ 本日分析未成功，詳見內文。\n"
    return f"""# FW 工程週分析（每日產出）— {date_str}（週{wd}）

> 範圍：最近 {days} 天的工程進展分析（含工作流狀態與時間）。
> 資料來源：{source}。
{status}
{body}
"""


# --------------------------------------------------------------------------
#  Redmine
# --------------------------------------------------------------------------
def _redmine_request(method: str, path: str, payload: dict | None):
    base = os.getenv("REDMINE_URL", "").rstrip("/")
    key = os.getenv("REDMINE_API_KEY", "")
    if not base or not key:
        return None, "REDMINE_URL / REDMINE_API_KEY 未設"
    url = f"{base}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"X-Redmine-API-Key": key,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return (json.loads(raw) if raw else {}), None
    except Exception as e:
        return None, str(e)


def post_to_redmine(report_md: str, date_str: str) -> str:
    mode = os.getenv("REPORT_REDMINE_MODE", "append").lower()
    project_id = int(os.getenv("REPORT_REDMINE_PROJECT_ID", "24"))

    if mode == "append":
        issue_id = os.getenv("REPORT_REDMINE_ISSUE_ID", "")
        if not issue_id:
            return "append 模式需設 REPORT_REDMINE_ISSUE_ID"
        _, err = _redmine_request("PUT", f"/issues/{issue_id}.json",
                                  {"issue": {"notes": report_md}})
        return f"appended to issue #{issue_id}" if not err else f"append 失敗: {err}"
    else:  # new
        payload = {"issue": {"project_id": project_id, "tracker_id": 4,
                             "subject": f"[daily] FW 工程郵件分析日報 {date_str}",
                             "description": report_md}}
        res, err = _redmine_request("POST", "/issues.json", payload)
        if err:
            return f"new issue 失敗: {err}"
        return f"created issue #{res['issue']['id']}"


# --------------------------------------------------------------------------
#  Main
# --------------------------------------------------------------------------
def main() -> int:
    date_str = datetime.date.today().isoformat()
    days = int(os.getenv("REPORT_DAYS", "7"))

    body, ok, source = build_week_report(days)
    report = build_report(date_str, days, body, ok, source)

    REPORT_DIR.mkdir(exist_ok=True)
    md_path = REPORT_DIR / f"{date_str}.md"
    md_path.write_text(report, encoding="utf-8")

    redmine_result = post_to_redmine(report, date_str) if ok else "skipped (分析未成功)"
    print(json.dumps({"ok": ok, "report": str(md_path), "redmine": redmine_result,
                      "days": days, "source": source}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
