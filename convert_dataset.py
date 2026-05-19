import os
import shutil
import random
from pathlib import Path

# ---------------------- 配置参数-拆分脚本 ----------------------
# 1. 原始增强数据集路径
RAW_DATA_PATH = r"F:\Python-program\111\bird_species_raw\CUB_200_2011\images"
# 2. 目标路径（改为标准分类结构）
TARGET_DATA_PATH = r"F:\Python-program\111\datasets\birds"
# 3. 拆分比例
TRAIN_RATIO = 0.8


# -----------------------------------------------------

def prepare_dataset():
    # 获取所有种类文件夹名
    if not os.path.exists(RAW_DATA_PATH):
        print(f"错误：找不到路径 {RAW_DATA_PATH}")
        return

    bird_classes = [d for d in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, d))]
    bird_classes.sort()

    print(f"开始处理，检测到 {len(bird_classes)} 个鸟类品种...")

    for cls_name in bird_classes:
        src_cls_path = os.path.join(RAW_DATA_PATH, cls_name)
        img_files = [f for f in os.listdir(src_cls_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        if not img_files:
            continue

        # 随机打乱
        random.shuffle(img_files)
        split_idx = int(len(img_files) * TRAIN_RATIO)
        train_imgs = img_files[:split_idx]
        val_imgs = img_files[split_idx:]

        # 【核心改动】：为每个类别创建独立的子文件夹
        train_dir = Path(TARGET_DATA_PATH) / "train" / cls_name
        val_dir = Path(TARGET_DATA_PATH) / "val" / cls_name

        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)

        # 移动/复制文件 (这里用 copy 比较稳妥)
        for img in train_imgs:
            shutil.copy(os.path.join(src_cls_path, img), train_dir / img)

        for img in val_imgs:
            shutil.copy(os.path.join(src_cls_path, img), val_dir / img)

        print(f"已完成: {cls_name} (train: {len(train_imgs)}, val: {len(val_imgs)})")

    print("\n" + "=" * 50)
    print("增强数据集拆分成功！当前结构符合标准分类要求：")
    print(f"路径: {TARGET_DATA_PATH}/train/ 和 {TARGET_DATA_PATH}/val/ (各下含 {len(bird_classes)} 个品种文件夹)")
    print("=" * 50)


if __name__ == "__main__":
    prepare_dataset()