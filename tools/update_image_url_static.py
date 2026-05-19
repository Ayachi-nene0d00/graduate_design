import os
import pymysql

BASE_DIR = r"F:\Python-program\111"
STATIC_REL = "static/bird_images"
VAL_DIR = os.path.join(BASE_DIR, "datasets", "birds", "val")

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1001"
MYSQL_DB = "bird_classification_app"

folder_to_image = {}
for folder in os.listdir(VAL_DIR):
    folder_path = os.path.join(VAL_DIR, folder)
    if os.path.isdir(folder_path):
        imgs = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        imgs.sort()
        if imgs:
            rel_path = f"{STATIC_REL}/{folder}/{imgs[0]}"
            folder_to_image[folder] = rel_path.replace("\\", "/")

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    charset="utf8mb4"
)
cursor = conn.cursor()
count = 0
for english_name, image_url in folder_to_image.items():
    sql = "UPDATE bird SET image_url=%s WHERE english_name=%s"
    cursor.execute(sql, (image_url, english_name))
    count += cursor.rowcount
conn.commit()
cursor.close()
conn.close()
print(f"已更新 {count} 条记录。所有 image_url 字段已指向 static/bird_images 下的图片。")

