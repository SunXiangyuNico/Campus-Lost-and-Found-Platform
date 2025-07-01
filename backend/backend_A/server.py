# 1. 从 flask 等库中导入必要的模块
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv  # <-- 新增第1步: 导入 load_dotenv 函数
import os
from dotenv import load_dotenv

# 在所有其他代码执行前，第一时间从 .env 文件加载环境变量
load_dotenv()

# 2. (关键步骤) 在所有代码执行前，加载 .env 文件中的变量
load_dotenv() # <-- 新增第2步: 执行函数，它会自动查找并加载 .env 文件

from config.db import connectDB # 确保在加载环境变量之后再导入数据库配置
from routes.auth import auth_bp

# 初始化 Flask 应用
app = Flask(__name__)

# --- 中间件和配置 ---

# 启用 CORS (跨源资源共享)
CORS(app)

# 连接到 MongoDB 数据库
connectDB()

# --- 路由注册 ---

# 定义一个根路由，用于测试服务器是否正在运行
@app.route('/')
def index():
    return jsonify({"message": "API Running (Python/Flask)"})

# 注册认证蓝图 (Blueprint)
app.register_blueprint(auth_bp, url_prefix='/api/auth')


# --- 启动服务器 ---

if __name__ == '__main__':
    # 从环境变量中获取端口，如果不存在则默认为 5000
    port = int(os.environ.get("PORT", 5000))
    # 启动 Flask 开发服务器
    app.run(host='0.0.0.0', port=port, debug=True)