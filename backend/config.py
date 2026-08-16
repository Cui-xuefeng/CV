class Config:
    # 基础配置
    DEBUG = True
    PORT = 5001
    BASE_URL = f"http://127.0.0.1:{PORT}"  # 基础URL，供其他地方引用


    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录
    static_path = os.path.join(BASE_DIR, "static")