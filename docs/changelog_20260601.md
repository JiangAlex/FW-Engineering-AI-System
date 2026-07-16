# Changelog 2026-06-01

## 1. AI QA Fallback 模式
**檔案:** `src/server.py`

- `/api/ask` 當 API Key 無效 (401) 或未設定時，自動切換 fallback 模式
- Fallback 回傳相關文件摘要（前 10 行），不再只顯示錯誤訊息

## 2. 資料脫敏層
**檔案:** `src/core/ai_client.py`

送出 AI 前自動移除敏感資訊：
- Email → `[EMAIL]`
- 電話 → `[PHONE]`
- 中文人名 → `[NAME]`
- From/To/Cc/Sent 行 → 移除
- 簽名檔 (Regards + name) → 移除
- Cell/Email/Phone 行 → 移除
- Sender metadata → `[REDACTED]`

技術內容（型號、FW 版本、專案編號）保留不動。

## 3. Conversation History（對話記憶）
**檔案:** `src/server.py`, `src/core/ai_client.py`

- 保留最近 5 輪 Q&A 作為上下文
- AI 可理解追問（如「那它跟上一版差在哪？」）
- Fallback 模式不存歷史
- Server 重啟自動清除

## 資料外洩風險總結

| 功能 | 是否對外傳輸 | 防護 |
|------|-------------|------|
| AI QA (`/api/ask`) | ✅ 送 MiniMax API | 脫敏層移除個資 |
| FW Summary / Timeline | ❌ 純本地 | N/A |
| Search | ❌ 純本地 SQLite FTS5 | N/A |
| Fallback 模式 | ❌ 不發任何請求 | N/A |

## 架構決策

- **不採用向量資料庫** — 44 篇文件 + 精確關鍵字查詢，FTS5 已是最佳解；向量 DB 需要 embedding 模型，違反「不用 AI」原則
- **完全離線方案** — 不設 API Key 即可全離線運作，所有核心功能（summary、timeline、search）不依賴外部 AI
