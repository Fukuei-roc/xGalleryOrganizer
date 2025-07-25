from stripImageMetadata import strip_metadata

# 預設測試路徑
input_image = "pinkNight_upscaled_00183_.png"
output_image = "pinkNight_upscaled_00183_clear.png"

# 呼叫函式清除 metadata
strip_metadata(input_image, output_image)
