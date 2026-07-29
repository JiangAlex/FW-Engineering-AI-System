# AI 小人行為規格

## 檔案

| 檔案 | 用途 |
|------|------|
| `src/templates/assistant_up.gif` | 走動動畫 — 向上 |
| `src/templates/assistant_down.gif` | 走動動畫 — 向下 |
| `src/templates/assistant_left.gif` | 走動動畫 — 向左 |
| `src/templates/assistant_right.gif` | 走動動畫 — 向右 |
| `src/templates/assistant.png` | 停下揮手（靜態 PNG） |

## 行為

### 走動（預設狀態）
- 根據移動方向顯示對應 GIF：`assistant_up.gif` / `assistant_down.gif` / `assistant_left.gif` / `assistant_right.gif`
- 方向判定：比較 dx/dy 絕對值，較大者為主方向
- 2D 自由移動，隨機選目標點，朝目標直線移動
- 速度：2px/frame
- 到達目標後短暫停頓（0.5~2 秒），再選新目標
- 初始方向：向下（`assistant_down.gif`）

### 隨機揮手
- 每 6~18 秒隨機觸發一次
- 停止走動，切換為 `assistant.png`
- 彈出氣泡「👋 想詢問什麼問題呢？」（3 秒後消失）
- 3 秒後切回當前方向對應的走動 GIF 繼續走

### 點擊互動
- 點擊小人 → 停止走動 → 切換揮手圖
- 彈出聊天氣泡框（固定寬 320px），出現在小人附近
- 氣泡框內容：
  - 標題「💬 想詢問什麼問題呢？」
  - 多行輸入框（textarea，可 resize）
  - 「取消」按鈕 → 關閉氣泡，小人繼續走
  - 「發送」按鈕 → 呼叫 `/api/ask`，回答顯示在氣泡內
  - Enter 送出，Shift+Enter 換行
- 回答成功後顯示「⭐ 採納」按鈕
  - 點擊採納 → 呼叫 `/api/ask/adopt` → 存為筆記

### 啟動時
- 初始位置：隨機
- 2 秒後首次彈出揮手氣泡

## 頁面結構

- 原本的 AI QA 區塊已移除
- 問答入口只有小人聊天氣泡
- 頁面保留：導航列（同步、週報）+ 筆記區
