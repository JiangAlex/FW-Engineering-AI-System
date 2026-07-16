# FW Engineering AI System - 修改記錄

## 2026-06-23

### 1. pipeline_service.py - 同步完刪除 .msg
- `run_pipeline` 處理成功後自動刪除 `knowledge/raw_msg/*.msg`

### 2. parser.py - 資安：移除個資
- 新增 `remove_recipients()` 方法
- 移除 `To:` / `Cc:` / `副本` 開頭的行（case-insensitive）
- 移除所有 email 地址
- 移除電話號碼（手機、辦公室、國際格式）
- 移除分機號碼（Ext/分機）
- 移除 WeChat / 微信 / LINE ID
- 清理 Mobile/Cell/Office/Tel/Phone 標籤空行

### 3. server.py - 移除 FW Timeline
- 刪除 `/api/fw/timeline` endpoint
- 刪除前端 Timeline HTML 區塊和 JS

---

## 2026-06-24

### 4. 新增 Note 功能
- **database.py**: 新增 `notes` 表 + `init_notes_db`, `insert_note`, `get_all_notes`, `delete_note`, `update_note`
- **server.py**: 新增 `/api/notes` GET/POST/PUT/DELETE endpoints
- 新增時同步寫入 `knowledge/notes/*.md` + chunks 索引（source_type="note"）
- 刪除時同步清理 .md + chunks
- 支援附加檔案上傳（FormData + UploadFile）
- 附檔存於 `knowledge/notes/attachments/`，透過 `/attachments/` 靜態路徑提供存取
- **前端**: 筆記獨立區塊，可新增（含附檔）/編輯/刪除/查看附件連結

### 5. TRD + ProductLogFiles 納入 AI QA
- **parser.py**: 新增 `parse_docx()`（用 zipfile+xml 解析 .docx）、`parse_cap_txt()`、`extract_project_version()`
- **database.py**: chunks 表加入 `source_type` 欄位（mail/trd/log/note）
- **pipeline_service.py**: `_rebuild_chunks()` 索引四種來源
  - `knowledge/md/*.md` → source_type="mail"
  - `knowledge/TRD/*.docx` → source_type="trd"
  - `knowledge/ProductLogFiles/*.cap|*.txt` → source_type="log"（取前 50 行）
  - notes DB → source_type="note"
- **前端**: 來源標籤顯示類型（📧mail / 📋TRD / 🔧Log / 📝Note）
- 自動從檔名+內容辨識專案名稱和版本號

### 6. 安裝依賴
- `python-multipart==0.0.32`（支援 Form/UploadFile）

---

## 目前索引狀態
| source_type | chunks |
|-------------|--------|
| mail        | 254    |
| trd         | 23     |
| log         | 3      |
| note        | 1      |
| **合計**    | **281**|

---

## 使用者偏好

- **Communication**: 技術解釋使用「繁體中文」，但「變數名稱」、「函數名稱」與「代碼註釋」必須保持英文。
- **Focus**: 極度重視防禦性編程、記憶體管理 (Heap/PSRAM) 與硬體中斷安全。