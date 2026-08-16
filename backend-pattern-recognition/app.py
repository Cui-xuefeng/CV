import threading

from config import Config
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes.detect import detect_bp
from routes.detect_real import detect_real_bp
from routes.detect_unet import detect_unet_bp
from routes.detect_real_unet import detect_real_unet_bp
# 初始化应用
def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.static_url_path = '/static'
    # 加载配置
    app.config.from_object(Config)

    # 解决跨域
    CORS(app, resources={
        r"/api/*": {"origins": "*"},  # 开发环境宽松配置
        r"/static/*": {"origins": "*"},
        r"/local/*": {"origins": "*"}
    })
    jwt = JWTManager(app)
    # 数据库配置
    db_uri = f"mysql+pymysql://{Config.DB_CONFIG['user']}:{Config.DB_CONFIG['password']}@" \
             f"{Config.DB_CONFIG['host']}:{Config.DB_CONFIG['port']}/{Config.DB_CONFIG['database']}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 注册蓝图
    app.register_blueprint(detect_bp, url_prefix='/local')
    app.register_blueprint(detect_real_bp, url_prefix='/local')
    app.register_blueprint(detect_unet_bp, url_prefix='/local')
    app.register_blueprint(detect_real_unet_bp, url_prefix='/local')
    return app


# 启动应用
if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )