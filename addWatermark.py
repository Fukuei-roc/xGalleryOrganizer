from PIL import Image, ImageDraw, ImageFont
import os
from settings import (
    WATERMARK_TEXT,
    WATERMARK_FONT_PATH,
    WATERMARK_FONT_SIZE,
    WATERMARK_OPACITY
)

def add_watermark(input_path, output_path):
    """
    為圖片加上右下角浮水印，並輸出為指定路徑。

    :param input_path: 原始圖片路徑
    :param output_path: 輸出圖片路徑（格式與輸入相同）
    """
    if not os.path.exists(input_path):
        print(f"❌ 找不到圖片：{input_path}")
        return

    try:
        with Image.open(input_path).convert("RGBA") as base:
            # 建立透明圖層用於浮水印
            txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            # 載入字型
            font = ImageFont.truetype(WATERMARK_FONT_PATH, WATERMARK_FONT_SIZE)

            # 計算浮水印文字尺寸
            text_size = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]

            # 計算右下角偏移（使用圖片大小的2%作為 padding）
            padding_x = int(base.width * 0.02)   # ex: 1400px 寬時約 28px
            padding_y = int(base.height * 0.02)  # ex: 800px 高時約 16px

            position = (base.width - text_width - padding_x,
                        base.height - text_height - padding_y)

            # 畫上浮水印文字
            draw.text(position, WATERMARK_TEXT, font=font, fill=(255, 255, 255, WATERMARK_OPACITY))

            # 合併圖層並轉為 RGB 儲存
            watermarked = Image.alpha_composite(base, txt_layer).convert("RGB")
            watermarked.save(output_path)
            print(f"✅ 浮水印已加入：{output_path}")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
