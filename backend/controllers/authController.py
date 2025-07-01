from flask import request, jsonify
from models.User import User
import bcrypt
import jwt
import json
import datetime
import os

# 从配置文件加载 JWT 密钥
def load_jwt_secret():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
    return config.get('jwtSecret')

JWT_SECRET = load_jwt_secret()

def register_user():
    """
    Controller: 注册新用户
    """
    try:
        # 1. 从请求体中获取 JSON 数据
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # 简单的验证
        if not all([username, email, password]):
            return jsonify({"errors": [{"msg": "Missing required fields"}]}), 400
        if len(password) < 6:
            return jsonify({"errors": [{"msg": "Password must be at least 6 characters"}]}), 400

        # 2. 检查邮箱是否已存在
        if User.objects(email=email).first():
            return jsonify({"msg": "User already exists"}), 400

        # 3. 对密码进行哈希加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 4. 创建一个新的用户实例并保存
        new_user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8')
        )
        new_user.save()

        # 5. 返回成功的响应
        return jsonify({"message": "用户注册成功"}), 201

    except Exception as e:
        print(f"Error in register_user: {e}")
        return jsonify({"msg": "Server error"}), 500


def login_user():
    """
    Controller: 用户登录
    """
    try:
        # 1. 从请求体中获取数据
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"msg": "Invalid Credentials"}), 400

        # 2. 检查用户是否存在
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"msg": "Invalid Credentials"}), 400

        # 3. 比较提交的密码和数据库中存储的哈希密码
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # 4. 创建 JWT payload
            payload = {
                'user': {
                    'id': str(user.id)
                },
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
            }

            # 5. 签名并生成 JWT
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            return jsonify({"token": token}), 200
        else:
            return jsonify({"msg": "Invalid Credentials"}), 400

    except Exception as e:
        print(f"Error in login_user: {e}")
        return jsonify({"msg": "Server Error"}), 500


def get_me():
    """
    Controller: 获取当前登录用户的信息
    (需要 auth 中间件注入用户信息)
    """
    try:
        # user_id 是在 auth 中间件中从 token 解码后附加到 request 对象上的
        user_id = request.user_id
        user = User.objects.with_id(user_id)
        
        if not user:
             return jsonify({"msg": "User not found"}), 404
        
        # 使用我们之前在 User 模型中定义的 to_json 方法来序列化
        return jsonify(user.to_json()), 200

    except Exception as e:
        print(f"Error in get_me: {e}")
        return jsonify({"msg": "Server Error"}), 500 