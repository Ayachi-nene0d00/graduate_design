import os
import pymysql

# 配置
BASE_DIR = r"F:\Python-program\111"
VAL_DIR = os.path.join(BASE_DIR, "datasets", "birds", "val")

# 数据库配置
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1001"  # 用户指定密码
MYSQL_DB = "bird_classification_app"

# 1. 遍历每个类别文件夹，获取首张图片
folder_to_image = {}
for folder in os.listdir(VAL_DIR):
    folder_path = os.path.join(VAL_DIR, folder)
    if os.path.isdir(folder_path):
        imgs = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        imgs.sort()
        if imgs:
            # 构造相对路径，供前端使用
            rel_path = os.path.relpath(os.path.join(folder_path, imgs[0]), BASE_DIR)
            folder_to_image[folder] = rel_path.replace("\\", "/")

# 2. 写入数据库
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
print(f"已更新 {count} 条记录。")

