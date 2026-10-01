"""Centralized LLM prompts — single source of truth.

All model-facing prompts (system messages, RAG QA, weekly-report map/reduce,
daily-report aggregation) live here so they can be reviewed and tuned in one
place, instead of being hardcoded across server.py / report_service.py /
local_llm.py / scripts/daily_report.py (which caused drift vs. knowledge/GUIDE.md).

Keep the dynamic parts as str.format placeholders; callers fill them in.

Workflow status vocabulary (fixed 5-state set), reused by report prompts:
  待處理(Todo) / 進行中(In Progress) / 阻礙或暫停(Blocked) /
  測試或審核(Testing) / 已完成(Done)
"""

# --- shared snippets -------------------------------------------------------
WORKFLOW_STATES = "待處理(Todo) / 進行中(In Progress) / 阻礙或暫停(Blocked) / 測試或審核(Testing) / 已完成(Done)"

# --- local LLM system message ---------------------------------------------
SYSTEM_MESSAGE = "你是一位專業的工程知識助理。請使用繁體中文回答，條列重點，簡潔明確。"

# --- RAG QA (server.py /api/ask) ------------------------------------------
def rag_qa(chunks_text: str, question: str) -> str:
    return f"""你是一位工程知識助理，請嚴格根據以下資料（可能包含 mail、產測 Log、TRD 測試需求、週報、筆記等來源）回答問題。若資料中找不到答案，請回答「資料中無相關記錄」。

【資料】
{chunks_text}

【問題】
{question}

要求：繁體中文回答，條列重點，標註資料來源類型，最後一句總結。"""


# --- Weekly report MAP (report_service.py) --------------------------------
def weekly_map(batch_text: str) -> str:
    return f"""你是一位工程專案經理助理。以下是本週部分工程 mail（每封標有日期），請摘要成精簡條列。

【資料】
{batch_text}

要求：
- 針對出現的**每一個機種／專案**各列 1~2 條重點（議題、進度、風險）。
- 每條**標注相關郵件日期**（取自來源郵件的日期，格式 YYYY-MM-DD）。
- 每個機種標注**工作流狀態**，從下列五選一（依郵件內容判斷）：
  {WORKFLOW_STATES}。
- 機種名稱保持原文英數代號（例如 Pi7a、EAP111、OAP101、SC48P）。
- 格式範例：`- EAP111 ［進行中］（2026-09-23）：VN 重工會議，確認...`
- 只輸出條列，不要前言或結論。"""


# --- Weekly report REDUCE (report_service.py) -----------------------------
def weekly_reduce(span_from: str, span_to: str, days: int, titles_count: int,
                  checklist_block: str, merged_summaries: str) -> str:
    return f"""你是一位工程專案經理，請根據以下「各批次摘要」統整成一份週報。

【報告區間】{span_from} ~ {span_to}（最近 {days} 天）
【本週郵件標題清單（共 {titles_count} 封）】
{checklist_block}

【各批次摘要】
{merged_summaries}

請輸出繁體中文 Markdown：

# Weekly Engineering Report

## 📋 機種工作流狀態總覽
（表格：| 機種 | 狀態 | 最近動態日期 | 一句話說明 |，狀態從五選一）

## ✅ Key Projects
## ✅ Key Issues
## ✅ Progress
## ✅ Risks
## ✅ Conclusion

要求：
- 條列式、簡短、白話文。
- **每個機種都要標注工作流狀態**，從下列五選一：
  {WORKFLOW_STATES}。
- **每條重點盡量標注相關郵件日期（YYYY-MM-DD）**，呈現時間軸。
- 「機種工作流狀態總覽」表格必須涵蓋所有出現的機種，欄位：機種 / 狀態 / 最近動態日期 / 一句話說明。
- **Key Projects 必須逐一涵蓋上方清單／摘要中出現的「每一個機種／專案」，即使某機種只有一封信也要列出，不可遺漏（例如 Pi7a、EAP111、OAP101、WAP12、JioWave62420、Pronto SC48P 等）。**
- 每個機種的 Key Projects 條目格式：`- 機種 ［狀態］（日期）：說明`。
- 若資訊不足，仍需列出機種名、標狀態為「待處理」並註明「資訊有限」。
- 機種名稱請保持原文英數代號（例如 Pi7a、EAP111）。"""


# --- Daily report: aggregate recent DailyReports (scripts/daily_report.py) -
def daily_aggregate(days: int, reports_block: str) -> str:
    return f"""你是一位工程專案經理，以下是最近 {days} 天的每日工程報告。請彙整成一份週分析。

【各日報告】
{reports_block}

請輸出繁體中文 Markdown，結構：

## 📋 機種工作流狀態總覽
（表格：| 機種 | 狀態 | 最近動態日期 | 一句話說明 |）

## ✅ Key Projects
## ✅ Key Issues
## ✅ Progress
## ✅ Risks
## ✅ Conclusion

要求：
- 每個機種標注**工作流狀態**（五選一）：{WORKFLOW_STATES}。
- 盡量標注相關日期（YYYY-MM-DD），呈現時間軸與狀態演進。
- 涵蓋各日報告中出現的每一個機種，機種名保持原文英數代號。
- 條目格式：`- 機種 ［狀態］（日期）：說明`。"""


# --- FW version compare (fw_service.py) -----------------------------------
def fw_compare(model: str, v1: str, v2: str, docs_text: str) -> str:
    return f"""
你是一位工程分析助理，請比較 {model} 的兩個版本：{v1} 與 {v2}。
根據以下資料，總結它們之間的差異（新功能、修復、已知問題）。

【資料】
{docs_text}

請輸出繁體中文 Markdown。
"""
