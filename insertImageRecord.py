import os
import sqlite3
from PIL import Image
import imagehash
from datetime import datetime, timedelta, timezone

DB_FILENAME = 'imageRecords.db'
IMAGE_PATH = 'PinkNight_023.png'  # 要導入的圖片

def get_current_time_taipei():
    """取得台北時區的現在時間（ISO 格式）"""
    taipei_tz = timezone(timedelta(hours=8))
    return datetime.now(taipei_tz).isoformat()

def extract_series(filename):
    """取得圖片系列名稱（檔名第一個 _ 前）"""
    return filename.split('_')[0]

def get_next_index_for_series(conn, series):
    """根據系列名稱，計算下一個索引數字（從 1 開始）"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM images WHERE series = ?", (series,))
    count = cursor.fetchone()[0]
    return count + 1

def insert_image_record(image_path):
    if not os.path.exists(image_path):
        print(f"❌ 找不到圖片檔案：{image_path}")
        return

    # 計算 pHash
    with Image.open(image_path) as img:
        phash = str(imagehash.phash(img))

    original_filename = os.path.basename(image_path)
    series = extract_series(original_filename)

    conn = sqlite3.connect(DB_FILENAME)
    next_index = get_next_index_for_series(conn, series)
    index_str = f"{next_index:03d}"  # 補零變成三碼

    public_preview = f"{series}_public_{index_str}.jpg"
    members_only = f"{series}_{index_str}.png"
    created_at = get_current_time_taipei()

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (
                phash,
                original_filename,
                series,
                public_preview,
                members_only,
                created_at,
                posted_at
            ) VALUES (?, ?, ?, ?, ?, ?, NULL)
        ''', (phash, original_filename, series, public_preview, members_only, created_at))

        conn.commit()
        print(f"✅ 成功導入圖片：{original_filename}")
        print(f"   - phash: {phash}")
        print(f"   - public_preview: {public_preview}")
        print(f"   - members_only: {members_only}")
        print(f"   - created_at: {created_at}")
    except sqlite3.IntegrityError:
        print(f"⚠️ 資料庫已存在相同 phash 的圖片，跳過導入。")
    finally:
        conn.close()

if __name__ == '__main__':
    insert_image_record(IMAGE_PATH)
