啟動虛擬環境
.\.venv\Scripts\activate

---

## 🖼️ Image Processing Pipeline

這是一個自動化圖片處理系統，負責將 `pendingImages` 資料夾中的原始圖片導入資料庫，並依照 `imageRecords.db` 的順序處理後輸出至 `publicPreview` 與 `membersOnly` 兩個資料夾。

---

### 📌 **功能概述**

* 讀取 `pendingImages` 下的圖片，導入資料庫（含 pHash、系列、檔名等資訊）
* 依資料庫順序處理圖片
* 產生兩個版本：

  * **Public Preview**：去除 Metadata → 調整大小（高度 800px） → 轉存 JPG → 加入浮水印
  * **Members Only**：去除 Metadata → 保持原始大小與格式 → 轉存 PNG

---

### 📂 **資料夾結構**

```
project_root/
│── pendingImages/      # 待處理圖片（來源）
│── publicPreview/      # 處理後的公開版（有浮水印）
│── membersOnly/        # 處理後的會員版（原大小、無浮水印）
│── fonts/              # 字型檔案，預設 fonts/arial.ttf
│── settings.py         # 設定檔（浮水印文字、字型大小、透明度、縮放高度）
│── imageRecords.db     # SQLite 資料庫（圖片資訊）
│── main.py             # 主程式（整合所有流程）
```

---

### 🛠 **處理流程**

1. **建立資料庫 `imageRecords.db`**

   * 由 `initImageDatabase.py` 建立
   * 資料表 `images` 結構：

     ```sql
     CREATE TABLE IF NOT EXISTS images (
         phash TEXT PRIMARY KEY,
         original_filename TEXT NOT NULL,
         series TEXT,
         public_preview TEXT,
         members_only TEXT,
         created_at TEXT NOT NULL,
         posted_at TEXT
     );
     ```

2. **導入圖片到資料庫**

   * 由 `insertImageRecord.py` 自動掃描 `pendingImages` 並將圖片資訊寫入資料庫。

3. **依資料庫順序處理圖片**

   * 由 `main.py` 讀取資料庫，依 `created_at` 排序。

4. **輸出 Public Preview**

   * 去除 Metadata（`stripImageMetadata.py`）
   * 調整大小至高度 800px 並轉存 JPG（`resizeAndConvertImage.py`）
   * 加入浮水印（`addWatermark.py`）
   * 另存為 `publicPreview/<public_preview>.jpg`

5. **輸出 Members Only**

   * 去除 Metadata（保持原始大小與格式）
   * 另存為 `membersOnly/<members_only>.png`

6. **重複處理，直到所有圖片完成**

---

### ⚙️ **設定檔 `settings.py`**

```python
# 調整圖片大小的目標高度
TARGET_HEIGHT = 800

# 浮水印設定
WATERMARK_TEXT = "NeonAfterDark.com"
WATERMARK_FONT_PATH = "fonts/arial.ttf"
WATERMARK_FONT_SIZE = 24
WATERMARK_OPACITY = 128  # 0~255，50% 透明度為 128
```

---

### ▶️ **執行方法**

1. 將待處理圖片放入 `pendingImages/`
2. 執行主程式：

   ```bash
   python main.py
   ```
3. 處理後的圖片將自動輸出至：

   * `publicPreview/`（公開版，含浮水印）
   * `membersOnly/`（會員版，無浮水印）

---

### ✅ **使用到的模組**

* `initImageDatabase.py`：建立 SQLite 資料庫
* `insertImageRecord.py`：掃描並將圖片資訊寫入資料庫
* `stripImageMetadata.py`：移除圖片 Metadata
* `resizeAndConvertImage.py`：調整圖片大小並轉換格式為 JPG
* `addWatermark.py`：加入右下角浮水印
* `main.py`：整合所有步驟，批次處理圖片

---

### 🚀 **Git 忽略規則**

`.gitignore` 已設定忽略：

* `__pycache__/`
* `.venv/`
* `pendingImages/*`（保留 `.gitkeep`）
* `publicPreview/*`（保留 `.gitkeep`）
* `membersOnly/*`（保留 `.gitkeep`）
* `imageRecords.db`
