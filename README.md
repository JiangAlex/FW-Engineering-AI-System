# FW Engineering AI System

韌體工程知識管理與 AI 問答系統。自動將 Outlook `.msg` 郵件轉換為結構化 Markdown，建立全文搜尋索引，並透過 AI 回答工程相關問題。

## 功能

- **郵件解析**：自動轉換 `.msg` → `.md`，移除個資、清理雜訊
- **全文搜尋**：FTS5 索引，支援多來源（mail / TRD / log / note）
- **AI 問答**：基於檢索增強生成 (RAG)，繁體中文條列式回答
- **TRD 索引**：自動解析 `.docx` 測試需求文件
- **產測 Log 索引**：解析 `.cap` / `.txt` 產測記錄
- **筆記系統**：新增/編輯/刪除筆記，支援附檔上傳
- **FW 摘要報告**：自動生成韌體版本摘要

## 系統架構

```
src/
├── server.py              # FastAPI 主程式 (port 8010)
├── core/
│   ├── parser.py          # MSG/DOCX/LOG 解析器
│   ├── database.py        # SQLite + FTS5 資料庫
│   └── ai_client.py       # MiniMax AI API 客戶端
├── services/
│   ├── pipeline_service.py  # 資料管線（MSG→MD→Chunks）
│   ├── fw_service.py       # FW 版本摘要服務
│   └── report_service.py   # 週報產生器
└── templates/
    └── index.html          # 前端 UI

knowledge/
├── raw_msg/          # 放入 .msg 檔案（處理後自動刪除）
├── md/               # 轉換後的 Markdown 文件
├── TRD/              # 測試需求文件 (.docx)
├── ProductLogFiles/  # 產測 Log (.cap/.txt)
├── notes/            # 使用者筆記
├── output/           # 摘要輸出
└── index.db          # SQLite 資料庫（自動生成）
```

## 安裝

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 設定

複製環境變數範本並填入 API Key：

```bash
cp .env.example .env
# 編輯 .env，設定 MINIMAX_API_KEY
```

## 啟動

```bash
python -m src.server
```

伺服器啟動於 `http://localhost:8010`

## 使用流程

1. 將 Outlook `.msg` 郵件放入 `knowledge/raw_msg/`
2. 啟動 server 或呼叫 `GET /api/pipeline/sync`
3. 系統自動轉換、索引、建立 chunks
4. 透過前端 UI 或 API 搜尋/問答

## API

| Endpoint | Method | 說明 |
|----------|--------|------|
| `/` | GET | 前端 UI |
| `/api/search?q=` | GET | 全文搜尋 |
| `/api/ask` | POST | AI 問答 |
| `/api/models` | GET | 取得所有機種列表 |
| `/api/fw/summary` | GET | FW 版本摘要 |
| `/api/pipeline/sync` | GET | 手動觸發同步 |
| `/api/notes` | GET/POST | 筆記列表/新增 |
| `/api/notes/{id}` | PUT/DELETE | 編輯/刪除筆記 |

## 測試

```bash
pytest tests/
```

## 技術棧

- Python 3.12
- FastAPI + Uvicorn
- SQLite + FTS5（全文搜尋）
- extract-msg（.msg 解析）
- BeautifulSoup4（HTML 清理）
- MiniMax AI API（RAG 問答）
