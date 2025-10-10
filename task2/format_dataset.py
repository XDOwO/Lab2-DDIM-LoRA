import os
import json

# 設定圖片資料夾路徑
img_dir = "./miku_dataset/train"
output_metadata = "./miku_dataset/metadata.jsonl"
default_prompt = "a Chibi girl"

# 取得所有 jpg 檔案並排序
jpg_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(".jpg")])

metadata = []
for idx, old_name in enumerate(jpg_files, 1):
    new_name = f"{idx:04d}.jpg"
    old_path = os.path.join(img_dir, old_name)
    new_path = os.path.join(img_dir, new_name)
    os.rename(old_path, new_path)
    metadata.append({"file_name": new_name, "text": default_prompt})

# 寫入 metadata.jsonl
with open(output_metadata, "w", encoding="utf-8") as f:
    for item in metadata:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Done! Renamed images and generated metadata.jsonl.")