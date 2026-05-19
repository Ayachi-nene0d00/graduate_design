import os
import shutil

# 将所有 val 下的首张图片复制到 static/bird_images/ 下，保持文件夹名+文件名结构
BASE_DIR = r"F:\Python-program\111"
VAL_DIR = os.path.join(BASE_DIR, "datasets", "birds", "val")
STATIC_DIR = os.path.join(BASE_DIR, "static", "bird_images")
os.makedirs(STATIC_DIR, exist_ok=True)

for folder in os.listdir(VAL_DIR):
    folder_path = os.path.join(VAL_DIR, folder)
    if os.path.isdir(folder_path):
        imgs = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        imgs.sort()
        if imgs:
            src = os.path.join(folder_path, imgs[0])
            dst_folder = os.path.join(STATIC_DIR, folder)
            os.makedirs(dst_folder, exist_ok=True)
            dst = os.path.join(dst_folder, imgs[0])
            shutil.copyfile(src, dst)
print("所有首图已复制到 static/bird_images/ 下")

