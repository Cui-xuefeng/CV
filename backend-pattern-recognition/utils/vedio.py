import os
from datetime import datetime

from flask import current_app
from PIL import Image, ImageDraw, ImageFont
#工具函数
def get_static_file_path(sub_dir, filename):
    dir_path = os.path.join(current_app.static_folder, sub_dir)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, filename)

def generate_unique_filename(prefix, suffix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{suffix}"

def draw_detection_results(pil_img, detect_info):
    """绘制检测结果到PIL图像上（处理中文）"""
    img = pil_img.copy()
    draw = ImageDraw.Draw(img)
    # 加载中文字体
    try:
        # 优先使用项目目录中的simhei.ttf，无则使用系统字体
        if os.path.exists("simhei.ttf"):
            font = ImageFont.truetype("simhei.ttf", 20)
        else:
            # Windows系统字体路径
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 20)
    except:
        try:
            # Linux系统字体路径
            font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 20)
        except:
            font = ImageFont.load_default()
            print("警告：未找到中文字体，中文将显示为方框")

    # 解析检测结果元组
    if isinstance(detect_info, tuple) and len(detect_info) >= 5:
        try:
            # 解码类别（UTF-8）
            class_conf_bytes = detect_info[0]
            class_conf_str = class_conf_bytes.decode('utf-8') if isinstance(class_conf_bytes, bytes) else str(class_conf_bytes)
            # 提取坐标（x1, y1, x2, y2）
            x1, y1, x2, y2 = map(int, detect_info[1:5])
            # 绘制红色矩形框
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            # 绘制文字（白色背景+黑色文字）
            text_bbox = draw.textbbox((x1, y1-25), class_conf_str, font=font)
            draw.rectangle(text_bbox, fill="white")
            draw.text((x1, y1-25), class_conf_str, fill="black", font=font)
        except Exception as e:
            print(f"绘制检测结果失败：{e}，检测信息：{detect_info}")
    return img