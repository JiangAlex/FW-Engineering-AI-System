import os
import re
import email.utils
from datetime import datetime, timedelta

# Define absolute paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(PROJECT_ROOT, "knowledge/md")
REPORT_DIR = os.path.join(PROJECT_ROOT, "knowledge/report")


def _parse_mail_date(md_content):
    """Extract the mail's real sent date (YYYY-MM-DD) from a .md's '- Date:' line.

    Uses the same parsing strategy as parser.extract_chunks (RFC 2822 →
    ISO → regex fallback). Returns None if no parseable date is found.

    This is the mail's actual timestamp, NOT the file's mtime — the pipeline
    batch-writes many .md files at once, so mtime does not reflect mail order.
    """
    m = re.search(r"^- Date:\s*(.+)$", md_content, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1).strip()
    try:
        return email.utils.parsedate_to_datetime(raw).strftime("%Y-%m-%d")
    except Exception:
        pass
    try:
        return datetime.fromisoformat(raw).strftime("%Y-%m-%d")
    except Exception:
        pass
    iso = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    return iso.group(1) if iso else None


class ReportService:
    @staticmethod
    def generate_weekly_report(ai_client=None, days=7, limit=40):
        """Generates a weekly engineering report from mail within the last `days`.

        Args:
            ai_client: AI client used to synthesize the report.
            days: Time window in days (default 7 = one week). Mails whose real
                sent date is on/after (today - days) are included.
            limit: Safety cap on number of mails fed into the prompt, to avoid
                overflowing the context window when a week is very busy. The
                most recent mails within the window are kept.

        Returns:
            (report_content, filename) tuple, or an error string on failure.
        """
        if not os.path.exists(MD_DIR):
            return "❌ Source directory not found"

        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Collect (date_str, filename, content) for mails within the window,
        # filtering on the mail's REAL sent date (not the file mtime).
        entries = []
        undated = 0
        for f in os.listdir(MD_DIR):
            if not f.endswith(".md"):
                continue
            with open(os.path.join(MD_DIR, f), "r", encoding="utf-8") as file:
                content = file.read()
            mail_date = _parse_mail_date(content)
            if mail_date is None:
                undated += 1
                continue
            if mail_date >= cutoff:
                entries.append((mail_date, f, content))

        if not entries:
            return (f"❌ 最近 {days} 天內無郵件記錄（自 {cutoff} 起）。"
                    f"（另有 {undated} 封無法解析日期的郵件未納入）")

        # Newest first by real mail date, then cap to `limit`.
        entries.sort(key=lambda e: e[0], reverse=True)
        entries = entries[:limit]

        # Actual date span covered by the selected mails.
        span_from = entries[-1][0]
        span_to = entries[0][0]

        titles = [os.path.splitext(f)[0] for _, f, _ in entries]
        checklist_block = "\n".join(f"- {t}" for t in titles)

        if ai_client is None:
            return "⚠️ AI Client not provided for report generation."

        # --- Map-Reduce to stay within a small context on CPU ---------------
        # A week can hold dozens of long mails (50k+ tokens total) which blows
        # past the LLM context and is unusably slow on CPU. Instead:
        #   MAP    : split mails into char-budgeted batches; summarize each
        #            batch into compact per-model bullet points.
        #   REDUCE : merge the (small) batch summaries into the final report.
        # Each LLM call thus sees only a small prompt -> fast, no overflow.
        MAP_BATCH_CHARS = int(os.getenv("REPORT_MAP_BATCH_CHARS", "3000"))
        PER_MAIL_CHARS = int(os.getenv("REPORT_PER_MAIL_CHARS", "1500"))

        # Build batches of labeled docs under the char budget.
        batches = []
        cur, cur_len = [], 0
        for mail_date, f, content in entries:
            title = os.path.splitext(f)[0]
            body = content[:PER_MAIL_CHARS]
            doc = f"### 來源郵件：{title}（{mail_date}）\n{body}"
            if cur and cur_len + len(doc) > MAP_BATCH_CHARS:
                batches.append(cur)
                cur, cur_len = [], 0
            cur.append(doc)
            cur_len += len(doc)
        if cur:
            batches.append(cur)

        # MAP: summarize each batch.
        batch_summaries = []
        for idx, batch in enumerate(batches, 1):
            from src.core.prompts import weekly_map
            map_prompt = weekly_map(chr(10).join(batch))
            s = ai_client.ask(map_prompt)
            batch_summaries.append(f"# 批次 {idx} 摘要\n{s}")

        merged_summaries = "\n\n".join(batch_summaries)

        # REDUCE: merge batch summaries into the final weekly report.
        from src.core.prompts import weekly_reduce
        reduce_prompt = weekly_reduce(span_from, span_to, days, len(titles),
                                      checklist_block, merged_summaries)
        report_content = ai_client.ask(reduce_prompt)

        # Save report
        os.makedirs(REPORT_DIR, exist_ok=True)
        filename = datetime.now().strftime("weekly_report_%Y%m%d.md")
        path = os.path.join(REPORT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(report_content)

        return report_content, filename
