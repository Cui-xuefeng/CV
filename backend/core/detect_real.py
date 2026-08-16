from flask import Blueprint, Response, request, jsonify, url_for
import threading
import cv2
import numpy as np
import time
import core.globals as g
from core.detect_thread import detect_camera
from utils.vedio import generate_unique_filename

# 创建蓝图（用于注册到Flask应用）
detect_real_bp = Blueprint("detect_real_bp", __name__, url_prefix="/local")

#MJPEG视频流接口
def generate_mjpeg():
    while True:
        with g.detect_lock:
            if not g.is_detecting and g.current_frame is None:
                # 无检测时显示等待提示
                for _ in range(10):
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(frame, "等待检测启动...", (100,240),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY,80])
                    yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
                    time.sleep(0.1)
                continue

        # 获取当前帧（线程安全）
        with g.frame_lock:
            frame = g.current_frame.copy() if g.current_frame is not None else None

        if frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "无视频流...", (100,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        # 编码为JPEG流
        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY,80])
        if not ret:
            continue
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
        time.sleep(0.01)

@detect_real_bp.route("/video_feed", methods=["GET"])
def video_feed():
    return Response(generate_mjpeg(), mimetype='multipart/x-mixed-replace; boundary=frame')

#启动检测接口
@detect_real_bp.route("/detect", methods=["POST"])
def start_detect():
    try:
        data = request.get_json() or {}
        mode = data.get("mode")
        save_video = data.get("save_video", False)

        if mode != "video":
            return jsonify({"code":400, "msg":"仅支持video模式"})

        with g.detect_lock:
            if g.is_detecting:
                return jsonify({"code":400, "msg":"检测已在运行"})
            g.is_detecting = True

        # 生成视频保存URL
        video_url = url_for("static", filename=f"videos/{generate_unique_filename('capture_video','mp4')}") if save_video else None

        # 启动检测线程
        threading.Thread(target=detect_camera, args=(0, save_video), daemon=True).start()

        return jsonify({
            "code":200,
            "msg":"检测已启动",
            "data":{"video_feed_url":"/video_feed", "saved_video_url":video_url}
        })
    except Exception as e:
        with g.detect_lock:
            g.is_detecting = False
        return jsonify({"code":500, "msg":f"启动失败：{str(e)}"})

#停止检测接口
@detect_real_bp.route("/stop_detect", methods=["POST"])
def stop_detect():
    with g.detect_lock:
        g.is_detecting = False
    return jsonify({"code":200, "msg":"检测已停止"})


