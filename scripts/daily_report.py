#!/usr/bin/env python3
"""Daily report for FW-Engineering-AI-System.

Collects knowledge-base + system status, asks the local LLM for a short
analysis (graceful fallback to data-only if LLM is unavailable), writes a
Markdown report under DailyReport/, and records it to Redmine.

Redmine modes (env REPORT_REDMINE_MODE):
  - "append" (default): add today's report as a NOTE on a single long-lived
    issue (env REPORT_REDMINE_ISSUE_ID). Tidy, one issue accumulates history.
  - "new": open a fresh issue each day.

Env:
  REDMINE_URL, REDMINE_API_KEY        Redmine access (required to post)
  REPORT_REDMINE_PROJECT_ID           default 24 (FW-Engineering-AI-System)
  REPORT_REDMINE_MODE                 append | new   (default append)
  REPORT_REDMINE_ISSUE_ID             target issue id for append mode
"""

import os
import sys
import json
import sqlite3
import datetime
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "knowledge" / "index.db"
REPORT_DIR = PROJECT_ROOT / "DailyReport"
KNOWLEDGE = PROJECT_ROOT / "knowledge"

sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------------------------------
#  Data collection
# --------------------------------------------------------------------------
def collect_stats() -> dict:
    """Collect knowledge-base + system status. Never raises; returns partial."""
    stats = {"date": datetime.date.today().isoformat(), "errors": []}

    # DB stats
    try:
        c = sqlite3.connect(str(DB_PATH))
        stats["chunks_total"] = c.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        stats["by_source"] = dict(
            c.execute("SELECT source_type, COUNT(*) FROM chunks GROUP BY source_type").fetchall()
        )
        try:
            stats["vectors"] = c.execute("SELECT COUNT(*) FROM chunk_meta").fetchone()[0]
        except sqlite3.OperationalError:
            stats["vectors"] = 0
        c.close()
    except Exception as e:
        stats["errors"].append(f"db: {e}")
        stats.setdefault("chunks_total", None)

    # fingerprints in sync?
    try:
        cf = (KNOWLEDGE / ".chunks_fingerprint").read_text().strip()
        ef = (KNOWLEDGE / ".embeddings_fingerprint").read_text().strip()
        stats["fingerprint_in_sync"] = (cf == ef)
    except Exception as e:
        stats["fingerprint_in_sync"] = None
        stats["errors"].append(f"fingerprint: {e}")

    # md file count
    try:
        md = KNOWLEDGE / "md"
        stats["md_files"] = len([f for f in os.listdir(md) if f.endswith(".md")]) if md.is_dir() else 0
    except Exception as e:
        stats["errors"].append(f"md: {e}")

    # vector store health: vectors should equal chunks
    if stats.get("vectors") is not None and stats.get("chunks_total") is not None:
        stats["vector_healthy"] = (stats["vectors"] == stats["chunks_total"])

    # LLM connectivity
    try:
        from src.core.local_llm import LocalAIClient
        client = LocalAIClient.get_instance()
        stats["llm_ready"] = bool(client and client.is_ready)
        stats["llm_model"] = getattr(client, "model", None) if client else None
    except Exception as e:
        stats["llm_ready"] = False
        stats["errors"].append(f"llm: {e}")

    return stats


def load_prev_stats() -> dict | None:
    """Load yesterday's (or the most recent previous) report stats JSON sidecar."""
    if not REPORT_DIR.is_dir():
        return None
    today = datetime.date.today().isoformat()
    sidecars = sorted(
        [p for p in REPORT_DIR.glob("*.stats.json") if p.stem.replace(".stats", "") < today],
        reverse=True,
    )
    if not sidecars:
        return None
    try:
        return json.loads(sidecars[0].read_text())
    except Exception:
        return None


def _delta(cur, prev, key):
    if not prev or prev.get(key) is None or cur.get(key) is None:
        return ""
    d = cur[key] - prev[key]
    return f"（{'+' if d >= 0 else ''}{d}）" if d else "（無變化）"


# --------------------------------------------------------------------------
#  Report building
# --------------------------------------------------------------------------
def build_data_section(stats: dict, prev: dict | None) -> str:
    by_src = stats.get("by_source", {}) or {}
    src_lines = "\n".join(f"| {k} | {v} |" for k, v in sorted(by_src.items(), key=lambda x: -x[1]))
    sync = stats.get("fingerprint_in_sync")
    sync_txt = "✅ 同步" if sync else ("⚠️ 不同步" if sync is False else "❓ 未知")
    vh = stats.get("vector_healthy")
    vh_txt = "✅ 一致" if vh else ("⚠️ 不一致" if vh is False else "❓")
    llm_txt = f"✅ {stats.get('llm_model')}" if stats.get("llm_ready") else "⚠️ 無法連線"

    return f"""## 📊 知識庫狀態

| 項目 | 值 |
|------|------|
| Chunks 總數 | {stats.get('chunks_total')} {_delta(stats, prev, 'chunks_total')} |
| 向量庫 (chunk_meta) | {stats.get('vectors')} {_delta(stats, prev, 'vectors')} |
| 向量/chunks 一致性 | {vh_txt} |
| Fingerprint 同步 | {sync_txt} |
| md 郵件檔數 | {stats.get('md_files')} {_delta(stats, prev, 'md_files')} |
| 本地 LLM | {llm_txt} |

### 來源分佈
| 來源 | chunks |
|------|--------|
{src_lines}
""" + (f"\n> ⚠️ 收集時發生問題：{'; '.join(stats['errors'])}\n" if stats.get("errors") else "")


def build_llm_analysis(stats: dict, prev: dict | None) -> str:
    """Ask the local LLM for a short analysis; fallback to a canned line."""
    if not stats.get("llm_ready"):
        return "_（本地 LLM 無法連線，本日略過 AI 分析，僅提供數據。）_"
    try:
        from src.core.local_llm import LocalAIClient
        client = LocalAIClient.get_instance()
        prompt = f"""你是韌體工程知識系統的維運助理。以下是今日與昨日的系統數據，請用繁體中文寫 3-5 條精簡的重點分析與建議（條列），聚焦變化、異常、健康度。不要重複原始數字表格。

今日: {json.dumps(stats, ensure_ascii=False)}
昨日: {json.dumps(prev, ensure_ascii=False) if prev else '無'}
"""
        ans = client.ask(prompt)
        if ans and not ans.startswith("⚠️") and not ans.startswith("❌"):
            return ans.strip()
        return "_（LLM 回應異常，本日僅提供數據。）_"
    except Exception as e:
        return f"_（LLM 分析失敗：{e}，本日僅提供數據。）_"


def build_report(stats: dict, prev: dict | None, analysis: str) -> str:
    wd = "一二三四五六日"[datetime.date.today().weekday()]
    return f"""# FW-Engineering-AI-System 每日報告 — {stats['date']}（週{wd}）

> 資料來源：`knowledge/index.db`、fingerprint 檔、本地 LLM 連線探測。
> 對比基線：{prev['date'] if prev else '無（首份報告）'}。

{build_data_section(stats, prev)}

## 🤖 AI 分析

{analysis}
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
            body = r.read().decode()
            return (json.loads(body) if body else {}), None
    except Exception as e:
        return None, str(e)


def post_to_redmine(report_md: str, stats: dict) -> str:
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
                             "subject": f"[daily] FW-Engineering-AI-System 每日報告 {stats['date']}",
                             "description": report_md}}
        res, err = _redmine_request("POST", "/issues.json", payload)
        if err:
            return f"new issue 失敗: {err}"
        return f"created issue #{res['issue']['id']}"


# --------------------------------------------------------------------------
#  Main
# --------------------------------------------------------------------------
def main() -> int:
    stats = collect_stats()
    prev = load_prev_stats()
    analysis = build_llm_analysis(stats, prev)
    report = build_report(stats, prev, analysis)

    REPORT_DIR.mkdir(exist_ok=True)
    md_path = REPORT_DIR / f"{stats['date']}.md"
    md_path.write_text(report, encoding="utf-8")
    (REPORT_DIR / f"{stats['date']}.stats.json").write_text(
        json.dumps(stats, ensure_ascii=False), encoding="utf-8")

    redmine_result = post_to_redmine(report, stats)
    print(json.dumps({"ok": True, "report": str(md_path),
                      "redmine": redmine_result,
                      "chunks": stats.get("chunks_total"),
                      "llm_ready": stats.get("llm_ready")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
