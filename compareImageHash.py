from PIL import Image
import imagehash

# 設定圖片檔案路徑
image_path1 = 'PinkNight_023.png'
image_path2 = 'PinkNight_public_023.jpg'

# 計算 pHash
hash1 = imagehash.phash(Image.open(image_path1))
hash2 = imagehash.phash(Image.open(image_path2))

# 印出 hash 值
print(f"{image_path1} pHash: {hash1}")
print(f"{image_path2} pHash: {hash2}")

# 計算漢明距離
hamming_distance = hash1 - hash2
print(f"🧮 漢明距離: {hamming_distance}")
