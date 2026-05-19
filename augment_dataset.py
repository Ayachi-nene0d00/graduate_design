import os
import shutil
from pathlib import Path
from PIL import Image
from torchvision import transforms

# ---------------------- 配置参数 ----------------------
DATASET_PATH = "datasets/birds"
AUGMENT_FACTOR = 3  # 每个图像生成3个增强版本
OUTPUT_PATH = "datasets/birds_augmented"
MIN_IMAGES_PER_CLASS = 1000  # 每类至少扩充到1000张

# 数据增强变换
augment_transforms = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.3),
    transforms.RandomRotation(degrees=30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
])

def augment_image(img_path, output_dir, base_name, aug_count):
    """对单张图像进行增强，生成指定数量的增强图像"""
    img = Image.open(img_path).convert('RGB')
    for i in range(aug_count):
        augmented_img = augment_transforms(img)
        new_name = f"{base_name}_aug_{i}.jpg"
        output_path = os.path.join(output_dir, new_name)
        augmented_img.save(output_path)

def augment_dataset():
    """扩充整个数据集，每类至少1000张"""
    if not os.path.exists(DATASET_PATH):
        print(f"错误：数据集路径不存在 {DATASET_PATH}")
        return

    output_train = Path(OUTPUT_PATH) / "train"
    output_val = Path(OUTPUT_PATH) / "val"
    output_train.mkdir(parents=True, exist_ok=True)
    output_val.mkdir(parents=True, exist_ok=True)

    total_original = 0
    total_augmented = 0

    # 只增强 train，val 只复制原图
    for split in ['train', 'val']:
        split_path = os.path.join(DATASET_PATH, split)
        output_split_path = output_train if split == 'train' else output_val

        if not os.path.exists(split_path):
            print(f"警告：{split_path} 不存在，跳过")
            continue

        for class_dir in os.listdir(split_path):
            class_path = os.path.join(split_path, class_dir)
            if not os.path.isdir(class_path):
                continue

            output_class_path = output_split_path / class_dir
            output_class_path.mkdir(exist_ok=True)

            img_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            # 复制原始图像
            for img_file in img_files:
                src = os.path.join(class_path, img_file)
                dst = output_class_path / img_file
                shutil.copy2(src, dst)

            total_original += len(img_files)

            if split == 'train':
                # 仅对 train 做增强
                n_orig = len(img_files)
                n_needed = max(0, MIN_IMAGES_PER_CLASS - n_orig)
                if n_needed == 0:
                    print(f"完成类别: {class_dir} (已有{n_orig}张, 无需增强)")
                    continue

                # 平均分配增强数到每张原图
                aug_per_img = n_needed // n_orig
                remainder = n_needed % n_orig
                aug_count_list = [aug_per_img + (1 if i < remainder else 0) for i in range(n_orig)]

                for idx, img_file in enumerate(img_files):
                    img_path = os.path.join(class_path, img_file)
                    base_name = os.path.splitext(img_file)[0]
                    try:
                        augment_image(img_path, str(output_class_path), base_name, aug_count_list[idx])
                        total_augmented += aug_count_list[idx]
                    except Exception as e:
                        print(f"增强失败 {img_file}: {e}")

                print(f"完成类别: {class_dir} ({n_orig} 原图 + {n_needed} 增强)")

    print(f"\n数据集扩充完成！")
    print(f"原始图像总数: {total_original}")
    print(f"增强图像总数: {total_augmented}")
    print(f"总图像数: {total_original + total_augmented}")
    print(f"扩充后数据集路径: {OUTPUT_PATH}")

if __name__ == "__main__":
    augment_dataset()
