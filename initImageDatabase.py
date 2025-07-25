# 資料表 SQL 結構：
# CREATE TABLE IF NOT EXISTS images (
#     phash TEXT PRIMARY KEY,
#     original_filename TEXT NOT NULL,
#     series TEXT,
#     public_preview TEXT,
#     members_only TEXT,
#     created_at TEXT NOT NULL,
#     posted_at TEXT
# );

import os
import sqlite3
from datetime import datetime

DB_FILENAME = 'imageRecords.db'

def init_image_database(db_path=DB_FILENAME):
    """建立圖片記錄用的 SQLite 資料庫"""
    if os.path.exists(db_path):
        print(f"✅ 資料庫已存在：{db_path}，不需重新建立。")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            phash TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            series TEXT,
            public_preview TEXT,
            members_only TEXT,
            created_at TEXT NOT NULL,
            posted_at TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ 資料庫已建立：{db_path}")

# 如果被當作主程式執行，則自動建立資料庫
if __name__ == '__main__':
    init_image_database()
