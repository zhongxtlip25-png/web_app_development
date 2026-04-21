# 路由與頁面設計 (API/Route Design) - 食譜收藏系統

本文件規劃了 Flask 應用程式的路由結構、對應的處理邏輯與 Jinja2 模板。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (食譜列表)** | `GET` | `/` | `index.html` | 顯示所有食譜，支援關鍵字搜尋 |
| **食譜詳情** | `GET` | `/recipe/<int:id>` | `recipe_detail.html` | 顯示單一食譜之食材與步驟 |
| **新增食譜頁面** | `GET` | `/recipe/new` | `recipe_form.html` | 顯示空白表單 |
| **建立食譜** | `POST` | `/recipe/new` | — | 接收資料並存入 DB，完成後導向首頁 |
| **編輯食譜頁面** | `GET` | `/recipe/<int:id>/edit` | `recipe_form.html` | 顯示帶有原有資料的表單 |
| **更新食譜** | `POST` | `/recipe/<int:id>/edit` | — | 更新資料，完成後導向詳情頁 |
| **刪除食譜** | `POST` | `/recipe/<int:id>/delete` | — | 刪除食譜後導向首頁 |
| **食材推薦頁面** | `GET` | `/recommend` | `recommend.html` | 根據使用者輸入食材進行推薦 |
| **烹飪日曆** | `GET` | `/calendar` | `calendar.html` | 顯示週/月烹飪計畫 |
| **新增排程** | `POST` | `/calendar/add` | — | 將食譜排入特定日期 |
| **刪除排程** | `POST` | `/calendar/<int:id>/delete` | — | 移除日曆上的特定活動 |
| **購物清單** | `GET` | `/shopping` | `shopping_list.html` | 顯示所有待買項目 |
| **匯入食譜食材** | `POST` | `/shopping/import` | — | 從指定食譜匯入所有食材至清單 |
| **勾選/取消購買** | `POST` | `/shopping/<int:id>/toggle` | — | 更新項目的購買狀態 |
| **清除清單** | `POST` | `/shopping/clear` | — | 刪除所有購物項目 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁與搜尋
- **輸入**: `q` (query string, 選填)
- **邏輯**: 若有 `q`，則模糊比對 `Recipe.title` 或 `Recipe.tags`；否則回傳所有食譜。
- **輸出**: 渲染 `index.html`。

### 2.2 食譜管理 (CRUD)
- **新增/編輯**: 使用同一個 `recipe_form.html`。
- **輸入**: `title`, `description`, `portions`, `prep_time`, `cook_time`, `ingredients[]`, `steps[]` 等表單欄位。
- **邏輯**: 
    - 驗證必填欄位。
    - 同時更新關連的 `Ingredient` 與 `Step` 資料表。
- **輸出**: 成功後使用 `redirect(url_for(...))`。

### 2.3 食材推薦
- **輸入**: `ingredients` (字串，逗號分隔)
- **邏輯**: 比對 `Recipe.tags` 或 `Ingredient.name`。
- **輸出**: 渲染 `recommend.html` 並顯示結果列表。

### 2.4 購物清單 (採買輔助)
- **匯入邏輯**: 接收 `recipe_id`，查詢該食譜的所有食材，並逐一建立新的 `ShoppingItem`。
- **勾選邏輯**: 使用 AJAX 或簡單 POST 請求更新 `is_bought` 狀態。

---

## 3. Jinja2 模板清單

所有模板將放置於 `app/templates/` 目錄：

- **base.html**: 主佈局，包含導航欄 (Navigation Bar)、Footer 與共用的 CSS/JS 引用。
- **index.html**: 繼承 `base.html`。包含搜尋框與食譜卡片列表。
- **recipe_detail.html**: 繼承 `base.html`。顯示單筆食譜完整資訊。
- **recipe_form.html**: 繼承 `base.html`。供新增與編輯共用的表單頁面。
- **recommend.html**: 繼承 `base.html`。顯示食材搜尋結果。
- **calendar.html**: 繼承 `base.html`。呈現日曆介面。
- **shopping_list.html**: 繼承 `base.html`。呈現清單、勾選框與清除按鈕。

---

## 4. 設計決策 (Design Decisions)

1. **Blueprint 模組化**: 為 `main`, `recipes`, `calendar`, `shopping` 分別建立 Flask Blueprint，避免單一檔案過大。
2. **表單提交 (POST over DELETE/PUT)**: 考量原生 HTML `<form>` 僅支援 GET/POST，因此更新與刪除操作一律使用 POST 搭配 URL 後綴（如 `/edit`, `/delete`）。
3. **AJAX 整合 (Nice to Have)**: 購物清單的勾選狀態與日曆的快速操作，建議搭配 Vanilla JS 進行非同步更新，提升使用者體驗。
