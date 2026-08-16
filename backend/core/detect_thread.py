import cv2
import numpy as np
from PIL import Image
import time
from contextlib import suppress
import core.globals as g
from utils.getStaticPath import get_static_file_path
from utils.vedio import draw_detection_results, generate_unique_filename
from model.segformer.segformer import SegFormer_Segmentation

def get_model(model_name):
    if model_name == 'UNET':
        from model.unet.unet import Unet
        return Unet()
    else:
        return SegFormer_Segmentation()

def detect_camera(video_path=0, save_video=False, model_name='Segformer'):
    video_writer = None
    video_save_path = ""

    try:
        # 初始化模型
        model = get_model(model_name)
        
        # 初始化摄像头
        with g.capture_lock:
            g.capture = cv2.VideoCapture(video_path)
            if not g.capture.isOpened():
                raise ValueError("未能打开摄像头")

        # 获取摄像头参数
        frame_width = int(g.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(g.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = g.capture.get(cv2.CAP_PROP_FPS) or 25.0

        # 初始化视频保存（若需要）
        if save_video:
            video_filename = generate_unique_filename("capture_video", "mp4")
            video_save_path = get_static_file_path("videos", video_filename)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(video_save_path, fourcc, fps, (frame_width, frame_height))
            if not video_writer.isOpened():
                print("警告：视频写入器初始化失败")
                video_writer = None

        fps_counter = 0.0
        # 检测主循环
        while True:
            with g.detect_lock:
                if not g.is_detecting:
                    break

            # 读取摄像头帧
            ret, frame = g.capture.read()
            if not ret:
                print("摄像头读取完毕")
                break

            t1 = time.time()


            frame = np.uint8(frame)
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            if len(frame.shape) != 3:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)

            # 模型推理+结果处理
            try:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_img = Image.fromarray(frame_rgb)
                detect_output = model.detect_image(frame_img)

                # 处理模型返回的元组结果
                if isinstance(detect_output, tuple):
                    if len(detect_output) >= 1 and isinstance(detect_output[0], (Image.Image, np.ndarray)):
                        frame_detected = detect_output[0]
                    else:
                        frame_detected = draw_detection_results(frame_img, detect_output)
                else:
                    frame_detected = detect_output if isinstance(detect_output, (Image.Image, np.ndarray)) else frame_img
            except Exception as e:
                print(f"推理异常：{e}")
                frame_detected = frame_rgb

            # 修复检测后帧格式
            if isinstance(frame_detected, Image.Image):
                frame_detected = np.array(frame_detected)
            frame_detected = np.uint8(frame_detected)
            if len(frame_detected.shape) == 2:
                frame_detected = cv2.cvtColor(frame_detected, cv2.COLOR_GRAY2RGB)
            elif frame_detected.shape[2] == 4:
                frame_detected = cv2.cvtColor(frame_detected, cv2.COLOR_RGBA2RGB)

            # 转换为BGR+绘制FPS
            frame_bgr = cv2.cvtColor(frame_detected, cv2.COLOR_RGB2BGR)
            fps_counter = (fps_counter + 1/(time.time()-t1)) / 2
            cv2.putText(frame_bgr, f"(*o*)-zZ:{fps_counter:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # 共享帧+保存视频
            with g.frame_lock:
                g.current_frame = frame_bgr.copy()
            if video_writer:
                video_writer.write(frame_bgr)

            time.sleep(max(0, 1/fps - (time.time()-t1)))

    except Exception as e:
        print(f"检测线程异常：{e}")
    finally:
        # 资源释放
        with g.capture_lock:
            if g.capture:
                g.capture.release()
        with suppress(Exception):
            if video_writer:
                video_writer.release()
        with g.detect_lock:
            g.is_detecting = False
        with g.frame_lock:
            g.current_frame = None
        print(f"检测结束，视频路径：{video_save_path if save_video else '无'}")