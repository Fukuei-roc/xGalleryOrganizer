from PIL import Image
import os

def strip_metadata(input_path, output_path):
    """
    移除圖片的所有 metadata（EXIF等），並儲存為新檔案
    :param input_path: 原始圖片檔案路徑
    :param output_path: 輸出圖片檔案路徑
    """
    if not os.path.exists(input_path):
        print(f"❌ 找不到圖片：{input_path}")
        return

    try:
        with Image.open(input_path) as img:
            # 重新建立圖片（去除 info / exif）
            data = list(img.getdata())
            cleaned_img = Image.new(img.mode, img.size)
            cleaned_img.putdata(data)
            cleaned_img.save(output_path)
            print(f"✅ Metadata 已清除：{output_path}")
    except Exception as e:
        print(f"❌ 無法處理圖片：{input_path}\n錯誤訊息：{e}")

# 測試用（可獨立執行）
if __name__ == '__main__':
    # 範例：將原圖轉存為 new.jpg，並移除 metadata
    strip_metadata("test_with_metadata.jpg", "test_cleaned.jpg")
