import pandas as pd
from flask import Blueprint, request, jsonify
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)
from model.segformer.segformer import SegFormer_Segmentation
import time
import cv2
import numpy as np
from PIL import Image
from utils.getStaticPath import get_static_file_path


detect_bp = Blueprint('detect', __name__,url_prefix='/local')


@detect_bp.post('/img/detect')
def detect():
    data = request.get_json()
    mode = data.get("mode")

    centernet = SegFormer_Segmentation()
    if mode == "video":
        video_path = 0
        video_save_path = get_static_file_path("videos", "capture_video.avi")
        video_fps = 25.0
        capture = cv2.VideoCapture(video_path)
        if video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

        ref, frame = capture.read()
        if not ref:
            raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")

        fps = 0.0
        while (True):
            t1 = time.time()
            # 读取某一帧
            ref, frame = capture.read()
            if not ref:
                break
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame = np.array(centernet.detect_image(frame))
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            fps = (fps + (1. / (time.time() - t1))) / 2
            print("fps= %.2f" % (fps))
            frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # cv2.imshow("video", frame)
            c = cv2.waitKey(1) & 0xff
            if video_save_path != "":
                out.write(frame)

            if c == 27:
                capture.release()
                break

        print("Video Detection Done!")
        capture.release()
        if video_save_path != "":
            print("Save processed video to the path :" + video_save_path)
            out.release()
        cv2.destroyAllWindows()

        return jsonify({
            'code': 200,
            'msg': '查询成功！',
            'data': {'vedio': video_save_path}
        })

    elif mode == "predict":
        crop = False
        count = True

        image_base64 = data.get("image_base64")
        if not image_base64:
            return jsonify({'code': 400, 'msg': '缺少image_base64参数'})

        #解码Base64为图片
        import base64
        from io import BytesIO

        # 去掉Base64前缀
        if image_base64.startswith('data:image'):
            image_base64 = image_base64.split(',')[1]
        image_bytes = base64.b64decode(image_base64)
        img = Image.open(BytesIO(image_bytes))


        # img = input('Input image filename:')

        # image = Image.open(img)

        r_image,classes = centernet.detect_image(image=img, crop = crop, count=count)
        new_classes = {}
        for key, value in classes.items():
            # 处理numpy整数类型
            if isinstance(value, np.integer):
                new_classes[key] = int(value)
            # 处理numpy浮点类型
            elif isinstance(value, np.floating):
                new_classes[key] = float(value)
            # 若有numpy数组，转为列表
            elif isinstance(value, np.ndarray):
                new_classes[key] = value.tolist()
            # 其他类型直接保留
            else:
                new_classes[key] = value
        # r_image.show()
        #classes去查neo4j放回passage
        #
        #
        #
        #



        img_path = get_static_file_path("detect", "predict.jpg")
        r_image.save(img_path)
        url = "http://localhost:5001/static/detect/predict.jpg"
        #shi检测图片img_path
        return jsonify({
            'code': 200,
            'msg': '查询成功！',
            'data': {'img_url': url }
        })

