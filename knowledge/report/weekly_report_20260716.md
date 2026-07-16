# Weekly Engineering Report

## ✅ Key Projects

| Project | Description | Status |
|---------|-------------|--------|
| ECS4650-54T (印尼專案) | DOA 換貨緊急處理 | 進行中 |
| EAP111 (Jio) | 台灣竹南產線新 PHY 導入驗證 | 進行中 |
| JioWave (JWS2261P/JWS4261P) | MAC/RSN 憑證管理與生產 | 進行中 |
| AP2600/SW2400P (易利信) | SW 進版 V3.4.25 | 進行中 |

---

## ✅ Key Issues

### 1. ECS4650-54T DOA 換貨
- **問題**：2 台設備到貨開機失敗，進入 Diag 而非正常 OS，型號顯示錯誤 (EPS5721-48T6Z)
- **Root Cause**：工廠韌體問題，72PCS 庫存需重工
- **緊急程度**：高（印尼市政府專案，客戶已宣布 DOA，要求立即換貨）

### 2. JioWave 生產線停線
- **問題**：FT-GL 測試工站故障 + MAC/RSN 憑證遲遲無法取得
- **影響**：多張工單停線，950+1950 PCS 積壓
- **緊急程度**：高（倉庫爆倉風險）

### 3. EAP111 FT Calibration 失敗
- **問題**：FT 階段出現 `/lib/firmware/MT7981_iPAiLNA_EEPROM.bin` 校準資料失敗
- **原因**：BRD 檔案 checksum 未檢查導致判 fail
- **緊急程度**：中（已修補，待驗證）

### 4. MTP/PDI 文件反饋
- **問題**：Jio 對 EAP111 測試計劃提出多項疑慮（缺少測試步驟、標準、RF 規格等）
- **緊急程度**：中（影響後續 NPI/PVT 進行）

---

## ✅ Progress

### ECS4650-54T
- ✅ 72PCS 庫存已完成重工，重新 DL Operation Code
- ✅ RD 確認 log 無問題
- ✅ 越南工廠 2 台替換機已確認可出貨（F3 庫）
- ✅ 客戶端 2 台 DOA 設備已遠端確認無法復原

### JioWave
- ✅ FT-GL 工站已修復恢復
- ✅ MAC/RSN 憑證已陸續取得並上傳越南 VM
- ✅ G264231V (950PCS)、G265047V (1950PCS) 已恢復生產
- ✅ G264230V (1000PCS) 可投產，預計 7/6 左右完成

### EAP111
- ✅ PT/FT 產測已更新至 V1.1.1F.8.3
- ✅ 台灣竹南產線驗證 meeting 已完成，結論如下：
  - 新 PHY (AN8801SBN) 已驗證完成，ECN 導入
  - FDL 程式已更新至 V4.1.1.1F.5.2
  - 鋼板、載具、N 階治具、組立治具轉竹南，預計 6/12 前完成
  - 庫存 17PCS 確認可出貨

### AP2600/SW2400P
- ✅ FDL 測試已完成
- ✅ SW 進版單已發出，等待 ECN 確認

---

## ✅ Risks

| Risk | Description | Impact |
|------|-------------|--------|
| JioWave 憑證延誤 | MAC 系統連號限制，無法一次給出 20K | 後續 8K 訂單投產待確認，可能再次停線 |
| MTP/PDI 反饋 | Jio 要求多項文件更新 | 影響 EAP111 NPI/PVT 時程 |
| OEL SFIS 建置 | 需虛擬伺服器跑 Ubuntu OS | 影響越南工廠 MES 系統上線 |
| ECS4650-54T 換貨 | 需確保替換機與原 DOA 機不同批次 | 避免再次發生相同 FW 問題 |

---

## ✅ Conclusion

1. **緊急**：印尼 ECS4650-54T 換貨已獲確認，2 台替換機可立即安排出貨，請持續追蹤客戶端回收事宜。

2. **JioWave**：FT-GL 已恢復，憑證陸續到位，但後續 8K 訂單仍需持續追蹤 Jio 憑證產出進度，避免再次停線。

3. **EAP111**：新 PHY 導入驗證已啟動，各項子任務皆有 owner 與 due date，請按時追蹤。

4. **AP2600/SW2400P**：SW 進版單已發出，待 ECN 確認後可正式投產。

5. **文件**：MTP/PDI 反饋需儘快回覆 Jio，避免影響雙方合作進度。