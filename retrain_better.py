from ultralytics import YOLO
import os
import torch
import multiprocessing

# ---------------------- 系统级优化（规避Windows兼容性问题，优化算力调配） ----------------------
os.environ["CUDNN_BENCHMARK"] = "1"  # 固定尺寸选最优卷积算法
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # 稳定识别GPU
# 限制OpenMP线程数，避免12核全开导致线程争抢和上下文切换开销（设为4-8最适宜）
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
# 关闭dynamo/triton依赖（彻底解决Windows下的核心报错）
os.environ["TORCHDYNAMO_DISABLE"] = "1"


# ---------------------- 显存精准控制（4G显存绝对安全） ----------------------
def get_optimal_batch():
    """RTX3050 4G显存优化batch=16（最大化并行加速）"""
    try:
        if torch.cuda.is_available():
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
            if gpu_mem >= 4:
                return 16  # 尝试最大batch加速
            elif gpu_mem >= 3:
                return 12
            else:
                return 8
        else:
            return 8
    except:
        return 12


# ---------------------- 详细监控函数（修复了作用域参数问题） ----------------------
def print_gpu_info(batch_size):
    """打印完整GPU信息，方便排查显存/算力问题"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        total_mem = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
        used_mem = 2.5 if batch_size == 16 else 3.5  # 预估batch占用
        print(f"🖥️ GPU详情：{gpu_name} | 总显存：{total_mem:.1f}G | 预估占用：{used_mem}G")
        print(f"🎛️ 算力配置：batch={batch_size} | 混合精度(FP16) | CUDNN优化开启")
    else:
        print("⚠️ 未检测到GPU，使用CPU训练")


# ---------------------- 主执行逻辑（Windows 多进程安全防线） ----------------------
if __name__ == '__main__':
    # 加载预训练的分类模型（而不是之前的权重）
    model = YOLO("yolov8n-cls.pt")

    current_batch = get_optimal_batch()

    # ---------------------- 最终训练参数（剔除无用参数，匹配分类任务） ----------------------
    train_params = {
        "data": "datasets/birds",  # 直接使用拆分后的数据集
        "epochs": 40,
        "imgsz": 224,  # 保持224保证精度
        "batch": current_batch,
        "lr0": 0.001,
        "lrf": 0.01,
        "device": 0 if torch.cuda.is_available() else "cpu",
        "project": "runs/classify",
        "name": "bird_cls_final_stable",
        "exist_ok": True,

        # 👇 核心提速与系统稳定
        "half": True,  # 混合精度
        "amp": True,  # 自动混合精度
        "compile": False,  # 关闭编译，规避Windows下Triton报错
        "cache": True,  # 启用缓存加速数据加载
        "workers": 8,  # 保持8加速数据加载

        # 👇 日志与图表
        "plots": True,  # 保留图表
        "verbose": True,  # 保留详细日志
        "save_period": 10,  # 每10轮保存一次
        "save_json": True,  # 保存结果到JSON
        "save_txt": True,  # 保存结果到TXT
        "save_conf": True,  # 保存置信度

        # 👇 图像分类专属增强与优化
        # (已移除 mosaic, mixup, hsv 等检测专属参数，避免警告和内部冲突)
        "auto_augment": "randaugment",  # 保持增强保证精度
        "pretrained": True,
        "warmup_epochs": 3,
        "weight_decay": 0.0005,
        "optimizer": "AdamW",
        "patience": 15,
    }

    # 训练前清理GPU缓存
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        print("✅ GPU缓存已清理，准备就绪。")

    print("\n🚀 最终稳定版训练启动")
    print_gpu_info(current_batch)

    # 1. 开始训练
    results = model.train(**train_params)

    # 2. 验证模型
    print("\n📊 开始验证最终模型...")
    metrics = model.val(verbose=True, workers=0)  # 禁用多进程避免页面文件错误

    # 3. 导出ONNX模型
    print("\n🔧 导出ONNX模型...")
    # 注意：simplify=True 需要你提前 pip install onnxsim
    onnx_path = model.export(
        format="onnx",
        imgsz=224,
        opset=12,
        dynamic=False,
        simplify=True,
        verbose=True
    )

    if os.path.exists(onnx_path):
        import shutil

        os.makedirs("static", exist_ok=True)
        shutil.copy2(onnx_path, "static/bird_cls_final_stable.onnx")
        print(f"✅ 模型已复制到：static/bird_cls_final_stable.onnx")

    # 4. 打印总结
    print(f"\n🎉 训练完成！")
    print(f"📈 验证集Top1准确率：{metrics.top1:.4f}（{metrics.top1 * 100:.2f}%）")
    print(f"📈 验证集Top5准确率：{metrics.top5:.4f}（{metrics.top5 * 100:.2f}%）")
    if torch.cuda.is_available():
        peak_mem = torch.cuda.max_memory_allocated() / 1024 ** 3
        print(f"💾 实际GPU显存峰值：{peak_mem:.2f}G")
