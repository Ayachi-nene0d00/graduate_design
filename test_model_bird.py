from ultralytics import YOLO
import random
import os
import glob

# ---------------------- 路径对齐（核心修改点） ----------------------
# 使用原始字符串 r"" 避免转义错误
BASE_DIR = r"F:\Python-program\111"

# 👇 这里修改为了对齐 retrain_better.py 中的 project="runs/classify" 和 name="bird_cls_final_stable"
MODEL_PATH = os.path.join(BASE_DIR, "runs", "classify", "bird_cls_final_stable", "weights", "best.pt")

if not os.path.exists(MODEL_PATH):
    print(f"❌ 未找到模型：{MODEL_PATH}")
    # 尝试自动搜索 fallback
    search_path = os.path.join(BASE_DIR, "runs", "**", "best.pt")
    found = glob.glob(search_path, recursive=True)
    if found:
        # 如果找到多个，按修改时间排序，取最新的一个
        found.sort(key=os.path.getmtime, reverse=True)
        MODEL_PATH = found[0]
        print(f"💡 自动找回最新训练的模型路径：{MODEL_PATH}")
    else:
        print("❌ 错误：请先运行 retrain_better.py 训练脚本生成 best.pt")
        exit(1)

# 加载模型
print(f"🔄 正在加载模型：{MODEL_PATH}")
model = YOLO(MODEL_PATH)

# ---------------------- 验证集路径 ----------------------
val_img_dir = os.path.join(BASE_DIR, "datasets", "birds", "val")
if not os.path.exists(val_img_dir):
    print(f"❌ 验证集路径不存在：{val_img_dir}")
    exit(1)

# 获取图片
img_list = []
for root, dirs, files in os.walk(val_img_dir):
    for f in files:
        if f.lower().endswith(('.jpg', '.png', '.jpeg')):
            img_list.append(os.path.join(root, f))

if not img_list:
    print("❌ 验证集内没有图片！")
    exit(1)

# 随机选5张
samples = random.sample(img_list, min(5, len(img_list)))

print("\n" + "=" * 60)
print("🔍 鸟类识别测试中...")
print("=" * 60)

for img_path in samples:
    # 真实类别是父文件夹名
    true_label = os.path.basename(os.path.dirname(img_path))

    # 预测 (verbose=False 保持控制台清爽)
    results = model(img_path, verbose=False)
    res = results[0]

    # 解析预测结果
    top1_name = res.names[res.probs.top1]
    conf = float(res.probs.top1conf)

    # 比对结果（去除两端空格并统一小写，防止格式问题导致误判）
    is_correct = "✅" if top1_name.strip().lower() == true_label.strip().lower() else "❌"

    print(f"图片: {os.path.basename(img_path)}")
    print(f"真实: {true_label} | 预测: {top1_name} ({conf:.2%}) {is_correct}")
    print("-" * 40)

print("\n✅ 测试完成！")