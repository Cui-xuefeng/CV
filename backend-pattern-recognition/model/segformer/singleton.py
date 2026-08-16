from model.segformer.segformer import SegFormer_Segmentation
import threading

class SegFormer:
    _instance = None
    _lock = threading.Lock()  # 线程安全锁

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = SegFormer()  # 原模型初始化参数
        return cls._instance

# 全局唯一模型实例
centernet = SegFormer()