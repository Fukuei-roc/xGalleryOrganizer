import os
import sqlite3
from initImageDatabase import init_image_database
from insertImageRecord import process_pending_images
from stripImageMetadata import strip_metadata
from resizeAndConvertImage import resize_and_convert
from addWatermark import add_watermark

DB_FILENAME = 'imageRecords.db'
PENDING_FOLDER = 'pendingImages'
PUBLIC_FOLDER = 'publicPreview'
MEMBERS_FOLDER = 'membersOnly'

# 確保輸出資料夾存在
os.makedirs(PUBLIC_FOLDER, exist_ok=True)
os.makedirs(MEMBERS_FOLDER, exist_ok=True)

# 第一步：建立資料庫（如果尚未存在）
init_image_database()

# 第二步：導入圖片到資料庫
process_pending_images()

# 第三步：依照 imageRecords.db 順序處理圖片
def process_images_from_db():
    if not os.path.exists(DB_FILENAME):
        print("❌ 找不到資料庫，請先執行 initImageDatabase。")
        return

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    cursor.execute("SELECT original_filename, public_preview, members_only FROM images ORDER BY created_at")
    records = cursor.fetchall()
    conn.close()

    for original_filename, public_name, members_name in records:
        input_path = os.path.join(PENDING_FOLDER, original_filename)
        if not os.path.exists(input_path):
            print(f"⚠️ 找不到圖片：{input_path}，跳過。")
            continue

        print(f"\n🖼️ 處理圖片：{original_filename}")

        # ---------- publicPreview ----------
        temp_clean = os.path.join(PUBLIC_FOLDER, '__temp_clean.jpg')
        resized_path = os.path.join(PUBLIC_FOLDER, '__temp_resized.jpg')
        final_public = os.path.join(PUBLIC_FOLDER, public_name)

        # 1. 去除 Metadata
        strip_metadata(input_path, temp_clean)
        # 2. 調整大小 + 轉成 jpg
        resize_and_convert(temp_clean, resized_path)
        # 3. 加浮水印
        add_watermark(resized_path, final_public)

        # 清除中間檔
        if os.path.exists(temp_clean):
            os.remove(temp_clean)
        if os.path.exists(resized_path):
            os.remove(resized_path)

        # ---------- membersOnly ----------
        members_output = os.path.join(MEMBERS_FOLDER, members_name)
        strip_metadata(input_path, members_output)

        print(f"✅ 已完成：{original_filename}")

if __name__ == '__main__':
    process_images_from_db()
