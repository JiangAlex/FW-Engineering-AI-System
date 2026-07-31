# 修改記錄：AI 問答搜尋涵蓋所有來源

**日期**：2026-07-31  
**檔案**：`src/server.py` — `/api/ask` 端點

## 問題描述

AI 問答回覆僅根據 mail 記錄回答，未搜尋 ProductLogFiles（產測 Log）和 TRD（測試需求）資料。

### 根因

1. **BM25 排名 + limit 過小**：預設 `search_chunks()` 的 `limit=5`，mail 有 2322 筆 chunks 佔優勢，log（48 筆）和 trd（303 筆）的結果被排名擠掉。
2. **Prompt 誤導**：prompt 寫「請嚴格根據以下 mail 記錄回答問題」，即使搜尋結果包含其他來源，AI 也只會以 mail 角度回答。

## 修改內容

### 1. 提高搜尋 limit

```python
# Before
results = search_chunks(req.question, model=req.model, date_from=req.date_from, limit=5)

# After
results = search_chunks(req.question, model=req.model, date_from=req.date_from, limit=15)
```

### 2. 新增多來源補搜機制

當通用搜尋結果中缺少 `log` 或 `trd` 來源時，自動額外搜尋這些來源各取最多 3 筆：

```python
existing_sources = {r.get("source_type", "mail") for r in results}
supplement_results = []
for stype in ["log", "trd"]:
    if stype not in existing_sources:
        extra = search_chunks(req.question, source_type=stype, limit=3)
        for r in extra:
            if r["filename"] not in existing_filenames:
                supplement_results.append(r)
```

補搜結果保留最多 5 個優先 slot，確保不被 mail 擠掉：

```python
max_supplement = min(len(supplement_results), 5)
max_general = 15 - max_supplement
results = results[:max_general] + supplement_results[:max_supplement]
```

### 3. 修改 AI Prompt

```python
# Before
prompt = """你是一位工程知識助理，請嚴格根據以下 mail 記錄回答問題。若資料中找不到答案，請回答「資料中無相關記錄」。
...
要求：繁體中文回答，條列重點，最後一句總結。"""

# After
prompt = """你是一位工程知識助理，請嚴格根據以下資料（可能包含 mail、產測 Log、TRD 測試需求、筆記等來源）回答問題。若資料中找不到答案，請回答「資料中無相關記錄」。
...
要求：繁體中文回答，條列重點，標註資料來源類型，最後一句總結。"""
```

## 驗證結果

搜尋「EAP101 EAP102」：

| 修改前 | 修改後 |
|--------|--------|
| mail: 5, log: 0, trd: 0 | mail: 10, log: 3, trd: 2 |

成功涵蓋 ProductLogFiles 產測記錄（`.cap`）與 TRD 測試需求文件（`.docx`）。

---

# 修改記錄：修復 _rebuild_chunks skip 邏輯導致新檔案不被索引

**日期**：2026-07-31  
**檔案**：`src/services/pipeline_service.py` — `_rebuild_chunks()`

## 問題描述

`EAP104_PT1-V0.5.1E.22A.cap` 存在於 `knowledge/ProductLogFiles/` 中，但搜尋不到。

### 根因

`_rebuild_chunks()` 中的 skip 條件比較：
- `indexed_files`（chunks 中的 distinct filename）= 222（包含 notes）
- `total_sources`（md + trd + log + image）= 217（**不包含 notes**）

因為 `222 >= 217`，skip 條件永遠成立，新加入的 `.cap` 檔案不會觸發 rebuild。

## 修改內容

在 `total_sources` 計算中加入 notes 數量：

```python
# Before
total_sources = md_count + trd_count + log_count + img_count

# After
from src.core.database import init_notes_db, get_all_notes
init_notes_db()
note_count = len(get_all_notes())
total_sources = md_count + trd_count + log_count + img_count + note_count
```

## 驗證結果

修正後：`total_sources = 223 > indexed_files = 222` → 觸發 rebuild → `EAP104_PT1-V0.5.1E.22A.cap` 成功索引。

## 永久修復：改用 Source Fingerprint 取代數量比對

**原始問題**：用 `indexed_files >= total_sources` 比對本質不可靠，任何新來源類型、刪除檔案、notes 增減等都可能導致誤判。

**永久方案**：改用 SHA-256 fingerprint 機制。

### 新增函數 `_compute_source_fingerprint()`

計算所有來源檔案的 `filename:mtime` 排序後的 SHA-256 hash，涵蓋：
- `knowledge/md/*.md`
- `knowledge/TRD/*.docx`
- `knowledge/ProductLogFiles/*.cap|*.txt`
- `knowledge/image/*`
- Notes（`note_{id}:{created_at}`）

任何檔案的新增、刪除、修改都會改變 fingerprint。

### 修改 `_rebuild_chunks()` skip 邏輯

```python
# Before: 脆弱的數量比對
if indexed_files >= total_sources:
    skip rebuild

# After: fingerprint 比對
current_fingerprint = _compute_source_fingerprint()
saved_fingerprint = read("knowledge/.chunks_fingerprint")
if saved_fingerprint == current_fingerprint:
    skip rebuild
# rebuild 完成後寫入新 fingerprint
```

### 行為

| 場景 | 結果 |
|------|------|
| 無任何變動 | ⏭️ skip（fingerprint match） |
| 新增 .cap 檔案 | 🔄 rebuild |
| 刪除檔案 | 🔄 rebuild |
| 修改檔案內容（mtime 變化） | 🔄 rebuild |
| 新增/刪除 note | 🔄 rebuild |
| `force_reindex=True` | 🔄 rebuild（bypass fingerprint） |
