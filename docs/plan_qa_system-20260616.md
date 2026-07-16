# Implementation Plan — 通用 QA 知識查詢系統

## Problem Statement

現有系統的 `/api/ask` 只是把 FTS5 整份文件搜尋結果丟給 AI，存在三個問題：
1. **搜尋粗糙** — OR + prefix 搜整份文件，常返回無關結果
2. **只能查版本** — 沒有段落級精準度，無法回答「為什麼重工」「PKI 流程是什麼」等問題
3. **無篩選機制** — 無法按型號或時間縮小範圍

## Requirements

1. 段落分段索引：只索引 Clean Content section，跳過 Full Content 避免重複 reply chain
2. 改善 FTS5 查詢：用 BM25 排序 + snippet() 提升精準度
3. 篩選：按型號 + 時間範圍限定搜尋
4. 來源引用：可展開的來源片段（顯示原文段落）
5. Fallback 模式：本地提取匹配段落組成重點列表
6. 全重建策略（force_reindex），不需增量
7. 前端篩選 UI 放在回答結果旁，先搜全部再 filter
8. AI 嚴格只根據搜到的 mail chunks 回答，找不到就回「資料中無相關記錄」

## New DB Schema

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
    filename,
    chunk_text,
    model,
    date_str
);
```

## API Changes

- `POST /api/ask` — 增加 optional model 和 date_from 參數，response 增加 sources
- `GET /api/search` — 增加 optional model 和 date_from 參數，返回 snippets
- `GET /api/models` — 新 endpoint，返回所有可篩選的型號列表

## Task Breakdown

### Task 1: database.py — 新增 chunks FTS5 table + search_chunks()

- `init_chunks_db()` — 建立 chunks FTS5 table
- `clear_chunks()` — 清空 chunks
- `insert_chunk(filename, chunk_text, model, date_str)` — 插入段落
- `search_chunks(query, model=None, date_from=None, limit=5)` — BM25 排序 + snippet

### Task 1b: parser.py — 新增 extract_chunks()

- 從 .md 提取 metadata (date, model) + Clean Content section
- 找 `## ✅ Clean Content` 到下一個 `## ✅` 或 EOF
- 用 model regex 從 filename + content 提取型號
- 回傳 {chunks: [str], model: str, date_str: str}

### Task 1c: tests/test_chunks.py

- 測試 extract_chunks() 正確切出 Clean Content
- 測試 search_chunks() BM25 排序
- 測試 model/date filter
- 測試空查詢 / 無結果

### Task 2: pipeline_service.py — 整合 _rebuild_chunks()

- run_pipeline() 最後呼叫 _rebuild_chunks()
- _rebuild_chunks(): 清空 → 掃描所有 .md → extract_chunks() → insert_chunk()
- 保留原本 docs table 不動

### Task 3: server.py — 改用 chunk 搜尋 + 篩選 + 來源引用 + fallback

- POST /api/ask: search_chunks() 取代 search_docs()，帶 model/date_from filter
- Response 新增 sources: [{filename, snippet}]
- Fallback: 從 chunks 提取含關鍵字的句子，按來源分組
- GET /api/search: 返回 [{filename, snippet, model, date_str}]
- GET /api/models: 查詢 chunks 中不重複 model 值

### Task 4: index.html — 前端篩選 UI + 來源展開

- fetch /api/models 填充型號下拉
- 回答結果旁：型號下拉 + 時間範圍選擇（全部/近一週/近一月/近三月）
- 來源區塊：accordion 展開顯示 snippet 片段
- askAI() 帶上 model 和 date_from 參數
