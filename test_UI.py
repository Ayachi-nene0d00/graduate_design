import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import os
import glob


class BirdApp:
    def __init__(self, root):
        self.root = root
        self.root.title("西建大 · 鸟类识别模型本地测试机")
        self.root.geometry("500x700")

        # 1. 自动寻找模型逻辑
        self.model = self.load_model()

        # 2. UI 界面布局
        self.title_label = tk.Label(root, text="智能鸟类识别系统", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        self.btn_select = tk.Button(root, text="选择鸟类照片", command=self.select_image,
                                    bg="#00b894", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        self.btn_select.pack()

        self.canvas = tk.Label(root, text="等待上传照片...", bg="#dfe6e9", width=40, height=15)
        self.canvas.pack(pady=20)

        self.result_label = tk.Label(root, text="识别结果：等待分析", font=("Arial", 14), fg="#2d3436")
        self.result_label.pack(pady=10)

        self.conf_label = tk.Label(root, text="置信度：--", font=("Arial", 12), fg="#636e72")
        self.conf_label.pack()

    def load_model(self):
        # 尝试自动定位模型
        base_path = r"F:\Python-program\111"
        pattern = os.path.join(base_path, "runs", "**", "best.pt")
        found = glob.glob(pattern, recursive=True)

        if not found:
            messagebox.showerror("错误", "找不到 best.pt 模型文件！请检查路径。")
            self.root.destroy()
            return None

        # 选最新的一个
        found.sort(key=os.path.getmtime, reverse=True)
        print(f"✅ 成功加载模型: {found[0]}")
        return YOLO(found[0])

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return

        # 显示图片
        img = Image.open(file_path)
        display_img = img.resize((300, 300))  # 缩放仅用于预览显示
        self.tk_img = ImageTk.PhotoImage(display_img)
        self.canvas.config(image=self.tk_img, text="")

        # 模型预测
        results = self.model.predict(source=file_path, imgsz=224, conf=0.2)

        if results and len(results[0].probs) > 0:
            # 获取最高分的索引和名字
            top1_idx = results[0].probs.top1
            top1_conf = results[0].probs.top1conf.item()
            name = self.model.names[top1_idx]

            # 更新 UI
            self.result_label.config(text=f"识别结果：{name}", fg="#d63031" if top1_conf < 0.5 else "#00b894")
            self.conf_label.config(text=f"置信度：{top1_conf * 100:.2f}%")
        else:
            self.result_label.config(text="识别失败：未检出物体")


if __name__ == "__main__":
    root = tk.Tk()
    app = BirdApp(root)
    root.mainloop()