import base64
import glob
import io
import json
import os
import re
import socket
import time
import urllib.error
import urllib.request
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from PIL import Image
import pymysql

app = FastAPI(title="Bird Classifier Intranet API")

# 允许跨域请求，防止由于前端限制导致请求被拦截
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = r"F:\Python-program\111"
model = None
latest_model_path = None

def load_latest_model():
    """Load the newest best.pt if available."""
    model_paths = glob.glob(os.path.join(BASE_DIR, "runs", "**", "best.pt"), recursive=True)
    if not model_paths:
        print("警告：未找到 best.pt 模型文件，请检查是否已完成训练。")
        return None, None
    newest_path = max(model_paths, key=os.path.getmtime)
    print(f"=== 加载最新模型 ===\n{newest_path}")
    try:
        return YOLO(newest_path), newest_path
    except Exception as exc:
        print(f"警告：模型加载失败: {exc}")
        return None, None

model, latest_model_path = load_latest_model()

# MySQL 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1001",
    "database": "bird_classification_app",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.get("/api/quiz")
async def get_quiz():
    try:
        # 连接数据库
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 动态生成基于 bird 表的题目，这里我们直接查询 5 只鸟的各个字段
            sql = "SELECT name, family, protect_level, region, habit, feature FROM bird ORDER BY RAND() LIMIT 5"
            cursor.execute(sql)
            birds = cursor.fetchall()
            
            # 为了生成干扰项，我们再取一批包含名字的用于选项
            sql_options = "SELECT name FROM bird ORDER BY RAND() LIMIT 20"
            cursor.execute(sql_options)
            other_birds = [b['name'] for b in cursor.fetchall()]

        connection.close()

        import random

        questions = []
        for bird in birds:
            # 随机挑选一种题型
            # 0: 根据特征猜鸟名
            # 1: 问某种鸟的科属
            # 2: 问某种鸟的保护级别
            # 3: 问某种鸟的分布区域
            q_type = random.choice([0, 1, 2, 3])

            if q_type == 0 and bird['feature']:
                feature = bird['feature'][:30] + "..." if len(bird['feature']) > 30 else bird['feature']
                question_text = f"外形特征为“{feature}”的鸟类是以下哪种？"
                correct_ans = bird['name']
                options = random.sample([b for b in other_birds if b != correct_ans], 3) + [correct_ans]
                random.shuffle(options)
                correct_idx = options.index(correct_ans)
                questions.append({
                    "question": question_text,
                    "option_a": options[0],
                    "option_b": options[1],
                    "option_c": options[2],
                    "option_d": options[3],
                    "correct_answer": chr(65 + correct_idx)
                })
            elif q_type == 1 and bird['family']:
                question_text = f"“{bird['name']}”属于哪个科属？"
                correct_ans = bird['family']
                # 从所有科属里随便造几个选项（这里简化处理）
                fake_options = ["鸭科", "鹰科", "雀科", "鸥科", "鹭科", "鸽科"]
                options = random.sample([f for f in fake_options if f != correct_ans], 3) + [correct_ans]
                random.shuffle(options)
                correct_idx = options.index(correct_ans)
                questions.append({
                    "question": question_text,
                    "option_a": options[0],
                    "option_b": options[1],
                    "option_c": options[2],
                    "option_d": options[3],
                    "correct_answer": chr(65 + correct_idx)
                })
            elif q_type == 2 and bird['protect_level']:
                question_text = f"“{bird['name']}”的保护级别是什么？"
                correct_ans = bird['protect_level']
                fake_options = ["国家一级保护动物", "国家二级保护动物", "三有保护动物", "无危", "濒危"]
                options = random.sample([f for f in fake_options if f != correct_ans], 3) + [correct_ans]
                random.shuffle(options)
                correct_idx = options.index(correct_ans)
                questions.append({
                    "question": question_text,
                    "option_a": options[0],
                    "option_b": options[1],
                    "option_c": options[2],
                    "option_d": options[3],
                    "correct_answer": chr(65 + correct_idx)
                })
            elif q_type == 3 and bird['region']:
                region = bird['region'][:20] + "..." if len(bird['region']) > 20 else bird['region']
                question_text = f"分布在“{region}”及附近区域的鸟类是："
                correct_ans = bird['name']
                options = random.sample([b for b in other_birds if b != correct_ans], 3) + [correct_ans]
                random.shuffle(options)
                correct_idx = options.index(correct_ans)
                questions.append({
                    "question": question_text,
                    "option_a": options[0],
                    "option_b": options[1],
                    "option_c": options[2],
                    "option_d": options[3],
                    "correct_answer": chr(65 + correct_idx)
                })

        # 为了保证一定要有5题（有字段为空的可能）
        while len(questions) < 5:
            # 补足
            questions.append({
                "question": "以下哪项是计算机经常识别的鸟类？",
                "option_a": "猫", "option_b": "狗", "option_c": "麻雀", "option_d": "鱼",
                "correct_answer": "C"
            })

        return {
            "code": 0,
            "data": questions[:5],
            "message": "动态生成题库成功"
        }
    except Exception as e:
        return {
            "code": -1,
            "message": f"数据库连接或查询失败: {str(e)}"
        }

@app.get("/api/recommend")
async def get_recommendations(lat: float = None, lon: float = None, city: str = "四川"):
    try:
        # 实际开发中可以通过 lat 和 lon 调用逆地理编码服务获取真实省市
        # 既然现在有真实的 country, province, city，前端传过来的无论是“成都市”还是“四川省”都可以查
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 修改查询策略：同时根据 region, province, city 去模糊匹配
            sql = "SELECT bird_id, name, english_name, family, feature, habit, protect_level, region, country, province, city, image_url FROM bird WHERE province LIKE %s OR city LIKE %s OR region LIKE %s LIMIT 10"
            search_param = f'%{city}%'
            cursor.execute(sql, (search_param, search_param, search_param))
            birds = cursor.fetchall()
            
            # 如果符合该地区的较少，我们随机补充几只凑够体验
            if len(birds) < 5:
                sql_fallback = "SELECT bird_id, name, english_name, family, feature, habit, protect_level, region, country, province, city, image_url FROM bird ORDER BY RAND() LIMIT %s"
                cursor.execute(sql_fallback, (5 - len(birds),))
                birds.extend(cursor.fetchall())
                
            # 去除可能出现的重复项
            unique_birds = {b['name']: b for b in birds}.values()
            
        connection.close()
        
        # 处理图片链接为空的情况
        final_birds = []
        for b in unique_birds:
            if not b.get('image_url'):
                b['image_url'] = 'https://img.haoma.com/bird_placeholder.jpg'
            final_birds.append(b)
            
        return {
            "code": 0,
            "data": list(final_birds),
            "region": city,
            "message": "获取推荐成功"
        }
    except Exception as e:
        return {
            "code": -1,
            "message": f"获取推荐失败: {str(e)}"
        }

@app.get("/api/bird")
async def get_bird_list(
    keyword: str = Query(None, description="模糊搜索关键字"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """
    鸟类科普库列表/搜索接口，支持分页和模糊查询
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT bird_id, name, english_name, family, feature, habit, protect_level, region, country, province, city, image_url FROM bird"
            params = []
            if keyword:
                sql += " WHERE name LIKE %s OR english_name LIKE %s OR family LIKE %s OR region LIKE %s"
                kw = f"%{keyword}%"
                params = [kw, kw, kw, kw]
            sql += " ORDER BY bird_id LIMIT %s OFFSET %s"
            params += [page_size, (page-1)*page_size]
            cursor.execute(sql, params)
            birds = cursor.fetchall()
        connection.close()
        return {"code": 0, "data": birds, "message": "查询成功"}
    except Exception as e:
        return {"code": -1, "message": f"查询失败: {str(e)}"}

@app.get("/api/bird/{bird_id}")
async def get_bird_detail(bird_id: int):
    """
    鸟类详情接口
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT bird_id, name, english_name, family, feature, habit, protect_level, region, country, province, city, image_url FROM bird WHERE bird_id=%s"
            cursor.execute(sql, (bird_id,))
            bird = cursor.fetchone()
        connection.close()
        if bird:
            return {"code": 0, "data": bird, "message": "查询成功"}
        else:
            return {"code": 1, "message": "未找到该鸟类"}
    except Exception as e:
        return {"code": -1, "message": f"查询失败: {str(e)}"}

# 挂载静态文件目录
# 任何访问 /static/... 的请求，都会被映射到 'F:/Python-program/111/static' 文件夹
# 例如: http://localhost:8000/static/bird.jpg 会返回 static/bird.jpg 文件
app.mount("/static", StaticFiles(directory=r"F:\Python-program\111\static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root_page():
    base_url = get_api_base_url()
    html = f"""
    <!doctype html>
    <html lang="zh-CN">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Bird Classifier Intranet API</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #2d3436; }}
            .card {{ max-width: 640px; padding: 24px; border: 1px solid #e0e0e0; border-radius: 12px; }}
            .links a {{ display: block; margin: 8px 0; color: #0984e3; text-decoration: none; }}
            .tip {{ color: #636e72; font-size: 14px; margin-top: 16px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Bird Classifier Intranet API</h2>
            <div class="links">
                <a href="/docs">API 文档 /docs</a>
                <a href="/api/meta">服务信息 /api/meta</a>
                <a href="/api/bird?page=1&page_size=5">鸟类列表示例 /api/bird</a>
            </div>
            <div class="tip">当前局域网访问地址：{base_url}</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if model is None:
            return {
                "code": -1,
                "message": "未加载模型，请先完成训练并确认 best.pt 存在。"
            }
        # 读取上传的图片流在内存中直接变成图像
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 使用 YOLO 进行预测（设定大小为你训练时的224）
        results = model(image, imgsz=224)
        result = results[0]

        # 提取最高置信度的类别和对应的名字
        top1_index = result.probs.top1
        confidence = float(result.probs.top1conf)
        bird_name = result.names[top1_index]

        return {
            "code": 0,
            "bird_name": bird_name,
            "confidence": round(confidence, 4), # 保留四位小数
            "message": "预测成功"
        }
    except Exception as e:
        return {
            "code": -1,
            "message": f"预测失败: {str(e)}"
        }

def get_local_ip():
    """获取本机局域网IP，优先用于内网服务绑定和前端提示"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_api_base_url():
    return f"http://{get_local_ip()}:8000"

def make_qr_base64(url: str):
    if not qrcode or not PILImage:
        return None
    qr = qrcode.QRCode(border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")

def load_api_key():
    env_key = os.getenv("SILICONFLOW_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    if env_key:
        return env_key.strip()
    api_file = os.path.join(BASE_DIR, "API.txt")
    if not os.path.exists(api_file):
        return None
    with open(api_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"sk-[A-Za-z0-9]+", content)
    return match.group(0) if match else None

def call_ai_api(question: str):
    api_key = load_api_key()
    if not api_key:
        return None, "API key not found"
    payload = {
        "model": "THUDM/GLM-4-9B-0414",
        "messages": [
            {"role": "system", "content": "You are a helpful bird expert. Provide concise, accurate answers."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url="https://api.siliconflow.cn/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            answer = parsed.get("choices", [{}])[0].get("message", {}).get("content", "")
            return answer.strip(), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except Exception as exc:
        return None, str(exc)

@app.get("/api/meta")
async def get_meta():
    base_url = get_api_base_url()
    return {
        "code": 0,
        "data": {
            "base_url": base_url,
            "qr_png_base64": make_qr_base64(base_url)
        },
        "message": "ok"
    }

@app.post("/api/aiqa")
async def aiqa(payload: dict = Body(...)):
    question = (payload.get("question") or "").strip()
    if not question:
        return {"code": -1, "message": "question is required"}
    answer, error = call_ai_api(question)
    if not answer:
        answer = "AI服务暂时不可用，请稍后再试。"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO ai_chat_log (user_id, question, answer) VALUES (%s, %s, %s)"
            cursor.execute(sql, (None, question, answer))
        connection.commit()
        connection.close()
    except Exception:
        pass
    return {
        "code": 0 if not error else -1,
        "data": {"answer": answer},
        "message": "ok" if not error else error
    }

try:
    import qrcode
    from PIL import Image as PILImage
except ImportError:
    qrcode = None
    PILImage = None

if __name__ == "__main__":
    # 更稳定的内网绑定逻辑，自动检测本机IP并打印友好提示
    url = get_api_base_url()
    print(f"\n[INFO] FastAPI服务即将启动，局域网访问地址: {url}\n")
    print("[INFO] 静态文件目录: /static/ (用于前端ONNX模型和图片访问)")
    print("[INFO] 推荐前端配置API地址为上述局域网IP，确保手机/PC同一WiFi下可访问\n")
    # 自动生成二维码
    if qrcode and PILImage:
        qr = qrcode.QRCode(border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        try:
            img.show(title="手机扫码访问本地服务")
        except Exception:
            pass
        print("[INFO] 手机扫码下方二维码即可访问：")
        qr.print_ascii(invert=True)
    else:
        print("[WARN] 未安装qrcode库，无法生成二维码。可用 pip install qrcode[pil] 安装。")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
