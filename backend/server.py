from flask import Flask, jsonify
from flask_cors import CORS
from config.db import connectDB
from routes.auth import auth_bp
import os

# 初始化 Flask 应用
app = Flask(__name__)

# --- 中间件和配置 ---

# 1. 启用 CORS (跨源资源共享)
#    允许所有来源的请求，这对于前后端分离的应用是必需的
CORS(app)

# 2. 连接到 MongoDB 数据库
connectDB()

# --- 路由注册 ---

# 定义一个根路由，用于测试服务器是否正在运行
@app.route('/')
def index():
    return jsonify({"message": "API Running (Python/Flask)"})

# 注册认证蓝图 (Blueprint)
# 所有在 auth_bp 中定义的路由都会以 /api/auth 为前缀
# 例如 /register -> /api/auth/register
app.register_blueprint(auth_bp, url_prefix='/api/auth')


# --- 启动服务器 ---

# 这个条件语句确保只有在直接运行这个脚本时，服务器才会启动
# 如果这个文件被其他脚本导入，则不会执行 app.run()
if __name__ == '__main__':
    # 从环境变量中获取端口，如果不存在则默认为 5000
    port = int(os.environ.get("PORT", 5000))
    # 启动 Flask 开发服务器
    # debug=True 会在代码更改后自动重启服务器
    app.run(host='0.0.0.0', port=port, debug=True) 