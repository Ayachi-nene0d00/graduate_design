# 毕业设计：鸟类识别与科普系统

本项目是一个基于 YOLOv8 分类模型的鸟类识别系统，包含：
- 数据集处理与增强脚本
- 模型训练、导出 ONNX 脚本
- FastAPI 本地后端服务（局域网可访问）
- UniApp 前端相关工程与集成资源
  
# 项目视频演示
[毕业设计视频演示.webm](https://github.com/user-attachments/assets/543f125b-4a34-40e0-99b7-767b87bed0b0)

## 项目结构

- `/convert_dataset.py`：将原始 CUB-200_2011 数据集拆分为 `train/val` 分类目录结构  
- `/augment_dataset.py`：对训练集做数据增强，生成扩充数据集  
- `/retrain_better.py`：训练分类模型并导出 ONNX  
- `/test_model_bird.py`：随机抽样验证模型预测效果  
- `/test_UI.py`：本地交互式测试界面  
- `/get_names.py`：导出模型类别名称数组  
- `/backend/main.py`：FastAPI 后端服务入口（含预测、推荐、问答等接口）  
- `/Uni_app_relation/`：UniApp 相关前端工程文件  

## 环境准备

建议使用 Python 3.9+，并安装项目依赖（按实际脚本需要）：

- `ultralytics`
- `torch`
- `torchvision`
- `pillow`
- `fastapi`
- `uvicorn`
- `pymysql`
- `qrcode[pil]`（可选，用于二维码）

## 数据准备流程

1. 准备原始数据集（默认路径示例：`bird_species_raw/CUB_200_2011/images/`）
2. 执行数据拆分：

```bash
python convert_dataset.py
```

3. （可选）执行数据增强：

```bash
python augment_dataset.py
```

## 模型训练与导出

运行训练脚本：

```bash
python retrain_better.py
```

训练完成后会在 `runs/classify/.../weights/best.pt` 生成模型，并导出 ONNX 到 `static/bird_cls_final_stable.onnx`。

## 本地后端运行

启动 FastAPI：

```bash
python backend/main.py
```

默认监听 `0.0.0.0:8000`，可在同一局域网内由手机或其他设备访问。

常用接口：

- `POST /predict`：上传图片并返回鸟类预测结果
- `GET /api/meta`：返回服务地址与二维码信息
- `GET /api/quiz`：获取题库（依赖 MySQL `quiz` 表）
- `GET /api/recommend`：地区推荐（依赖 MySQL `bird` 表）
- `GET /api/bird`、`GET /api/bird/{bird_id}`：鸟类百科查询
- `POST /api/aiqa`：鸟类问答（需要 AI API Key）

## 注意事项

- 脚本中包含 Windows 路径配置（如 `F:\\Python-program\\111`），在其他环境运行前请按本机路径调整。
- `backend/main.py` 的数据库配置默认使用本地 MySQL，请先创建并导入 `bird_classification_app` 相关表数据。
- 若重新训练模型，请同步更新前端使用的 ONNX 文件及类别名称列表。
