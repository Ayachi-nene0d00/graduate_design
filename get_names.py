from ultralytics import YOLO
import json
import os
import glob

# ---------------------- 智能路径搜索 ----------------------
BASE_DIR = r"F:\Python-program\111"
# 自动在 runs 目录下递归查找所有的 best.pt
search_pattern = os.path.join(BASE_DIR, "runs", "**", "best.pt")
found_files = glob.glob(search_pattern, recursive=True)

if not found_files:
    print(f"❌ 错误：在 {BASE_DIR} 的 runs 文件夹里没找到任何 best.pt！")
    print("💡 请确认：1. 训练是否已经结束？ 2. 文件夹路径是否正确？")
    # 列出当前目录下有的文件夹，帮你排查
    if os.path.exists(os.path.join(BASE_DIR, "runs")):
        print(f"当前 runs 目录下的文件夹有：{os.listdir(os.path.join(BASE_DIR, 'runs'))}")
    exit(1)

# 如果找到了多个，取最后修改的那一个（通常是最新的训练结果）
found_files.sort(key=os.path.getmtime, reverse=True)
pt_path = found_files[0]

print(f"✅ 自动定位到模型：{pt_path}")

# ---------------------- 提取逻辑 ----------------------
try:
    model = YOLO(pt_path)
    names_dict = model.names
    # 按照索引顺序排列
    names_list = [names_dict[i] for i in sorted(names_dict.keys())]

    print("\n" + "="*50)
    print("👇 请复制下方数组内容到 UniApp 的 birdNames 中 👇")
    print("="*50 + "\n")
    print(json.dumps(names_list, ensure_ascii=False, indent=2))
    print("\n" + "="*50)

except Exception as e:
    print(f"❌ 提取失败：{e}")