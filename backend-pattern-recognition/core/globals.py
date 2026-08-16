import threading

#多线程共享的全局状态
current_frame = None       # 当前检测帧（供MJPEG流使用）
is_detecting = False       # 检测运行状态
capture = None             # 摄像头捕获对象

# 线程锁（避免多线程竞态）
frame_lock = threading.Lock()    # 保护current_frame
detect_lock = threading.Lock()   # 保护is_detecting
capture_lock = threading.Lock()  # 保护capture