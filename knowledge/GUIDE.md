# Knowledge Base 說明

## AI QA Prompt

AI 問答時使用的 prompt 模板：

```
你是一位工程知識助理，請嚴格根據以下 mail 記錄回答問題。若資料中找不到答案，請回答「資料中無相關記錄」。

【資料】
{搜尋到的 chunks（最多 5 筆）}

【問題】
{使用者的問題}

要求：繁體中文回答，條列重點，最後一句總結。
```

### 資料來源優先順序

1. `chunks` FTS5 搜尋結果（BM25 排名）
2. 可依 **型號**（model）和 **時間**（date_from）篩選

### AI 回應讀取的 .md 檔案

- AI **不直接讀取** .md 檔案
- 系統預先將 `knowledge/md/*.md` 中的 `## ✅ Clean Content` 或 `## ✅ Full Content` 切成 chunks（每 20 行一段）存入 SQLite FTS5
- 問答時從 FTS5 搜尋最相關的 chunks 組成 context 送給 AI
- 回應中的 `📎 來源` 會顯示該 chunk 來自哪個 .md 檔案

---

## .msg 檔案注意事項

### 放置位置

將 Outlook `.msg` 檔案放入 `knowledge/raw_msg/`，系統啟動或呼叫同步 API 時自動處理。

### 處理流程

1. `.msg` → 解析（subject / sender / date / body）
2. 產出 `.md` 存入 `knowledge/md/`
3. 索引至 SQLite FTS5（docs + chunks 表）
4. 原始 `.msg` **處理成功後自動刪除**

### 已知限制與注意事項

| 項目 | 說明 |
|------|------|
| **編碼問題** | 部分郵件 sender 使用 GBK 字元但宣告 gb2312，系統已加入 fallback（自動用 olefile 直接讀取 OLE stream 並正確解碼） |
| **回覆鏈截斷** | `remove_reply_chain()` 會在遇到 `From:` / `Sent:` 時截斷，可能丟失重要技術內容。已加入 fallback：當 Clean Content < 100 字元時，自動改用 Full Content |
| **檔名限制** | subject 中的特殊字元 `\/:*?"<>|` 會被移除，最長 80 字元 |
| **重複處理** | 若 `knowledge/md/` 已有同名 .md 且時間較新，會跳過不重新轉換 |
| **附件** | `.msg` 中的附件目前不會被提取或索引 |
| **大量檔案** | 一次放入太多 .msg 會使 pipeline 執行較久，建議分批（每次 < 50 封） |
| **HTML 郵件** | 系統優先讀取 HTML body 再用 BeautifulSoup 轉純文字；純文字郵件直接使用 body |
| **個資清理** | 兩階段清理：(1) msg→md 時移除 To/Cc、email、電話、分機、WeChat/LINE ID；(2) 送 AI 前再次脫敏，將殘留 email→`[EMAIL]`、電話→`[PHONE]`、人名→`[NAME]`、Sender→`[REDACTED]` |

### ⚠️ 編號識別重點（msg→md 及 AI QA 皆須注意）

> 以下同時適用於 `knowledge/image/`、`knowledge/ProductLogFiles/`、`knowledge/TRD/` 的檔名解析。

#### knowledge/image/ — FW Binary Image

- 放置 FW binary 檔案（如 `EAP111_V5.0.5.5.bin`）
- 系統只索引**檔名**（不解析 binary 內容）
- 從檔名自動提取 model 和 version 資訊
- 索引為 `source_type="image"`，AI QA 可搜尋 FW 版本

以下編號常出現在郵件中，**非機種型號**，解析時勿誤判為 model：

| 前綴/代碼 | 類型 | 範例 |
|-----------|------|------|
| `FIKWLP` | 工廠 F 階 | FIKWLP104003E |
| `CIKWLP` | 工廠 C 階 | CIKWLP104003E |
| `175` | 工廠產測編號 | 175000004890A |
| `F0PWL` | 庫存編號 | F0PWL4155009A |
| `ECN` | RD 文件編號 | ECN260700094 |
| `SWR` | TA 文件編號 | SWR260700192 |
| `2492` | SW code p/n 編號 | 249200000602A |
| `2491` | FW code 編號 | 249100008566A |
| `MTR` | 產測申請單編號 | MTR26020021A |

以下為**實際產品型號**前綴：

| 前綴 | 類型 | 範例 |
|------|------|------|
| `EAP` | AP（Access Point）產品 | EAP111、EAP104、EAP115 |
| `OAP` | AP 產品 | OAP101、OAP103 |
| `ECS` | Switch 產品 | ECS4100、ECS2100 |

### 同步 API 回傳狀態

| status | 意義 |
|--------|------|
| `no_new_files` | `raw_msg/` 中沒有新的 .msg 檔案 |
| `success` | 全部轉換成功 |
| `partial` | 部分成功、部分失敗 |
| `failed` | 有找到檔案但全部轉換失敗 |

### 強制重新索引

呼叫 pipeline 時加入 `force_reindex=True`，會清除 DB 並重新索引所有 .md 檔案。
