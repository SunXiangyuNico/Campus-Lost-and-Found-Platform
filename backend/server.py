from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config.db import initialize_db
from routes.auth import auth_bp
from routes.item import item_bp
from routes.message import message_bp
from routes.map import map_bp

# 加载环境变量
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)

# --- 标准的 Flask 配置方法 ---
# 1. 从环境变量加载敏感配置
MONGO_URI_FROM_ENV = os.environ.get('MONGO_URI')
if not MONGO_URI_FROM_ENV:
    raise ValueError("No MONGO_URI set for Flask application")

# 2. 将配置设置到 app.config 对象中
app.config['MONGO_URI'] = MONGO_URI_FROM_ENV

# 初始化数据库 (现在它会从 app.config 读取)
initialize_db(app)

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(item_bp, url_prefix='/api/items')
app.register_blueprint(message_bp, url_prefix='/api/messages')
app.register_blueprint(map_bp, url_prefix='/api/map')


if __name__ == '__main__':
    app.run(debug=True)