from PIL import Image
import os
from settings import TARGET_HEIGHT

def resize_and_convert(input_path, output_path):
    """
    調整圖片大小（以高度為準）並轉存為 JPEG 格式。

    :param input_path: 原始圖片路徑
    :param output_path: 輸出 JPEG 圖片路徑（應以 .jpg 結尾）
    """
    if not os.path.exists(input_path):
        print(f"❌ 找不到圖片：{input_path}")
        return

    try:
        with Image.open(input_path) as img:
            # 計算等比例寬度
            original_width, original_height = img.size
            new_height = TARGET_HEIGHT
            new_width = int((new_height / original_height) * original_width)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # 確保是 RGB 模式才能存成 jpg
            if resized_img.mode in ("RGBA", "P"):
                resized_img = resized_img.convert("RGB")

            resized_img.save(output_path, format="JPEG", quality=95)
            print(f"✅ 圖片已調整為高度 {new_height}px 並另存為 JPG：{output_path}")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
