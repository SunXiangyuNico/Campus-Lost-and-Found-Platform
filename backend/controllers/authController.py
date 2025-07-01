from flask import request, jsonify
from models.User import User
# 导入邮件发送服务
from services.notificationService import send_email
import bcrypt
import jwt
import json
import datetime
import os

# 直接从环境变量中获取 JWT 密钥
JWT_SECRET = os.environ.get('JWT_SECRET')

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
        # 6. 将新用户保存到数据库
        new_user.save()

        # 7. 发送一封欢迎邮件 (新功能!) - 暂时禁用以修复服务器错误
        # send_email(
        #     to_email=new_user.email,
        #     subject='欢迎注册校园失物招领平台！',
        #     html_content=f'<strong>你好 {new_user.username},</strong><p>感谢您注册我们的平台，希望您在这里能有好的体验！</p>'
        # )

        # 8. 返回成功的响应
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

def update_me():
    """
    Controller: 更新当前登录用户的信息
    (例如: 用户名)
    """
    try:
        # 1. user_id 由 auth_middleware 注入
        user_id = request.user_id
        user = User.objects.with_id(user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # 2. 获取请求体中的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Request body must be JSON"}), 400

        # 3. 更新允许修改的字段
        # 我们只允许用户更新他们的 username
        if 'username' in data:
            new_username = data['username']
            # 可选的健壮性检查: 确保新用户名没有被其他人使用
            if User.objects(username=new_username, id__ne=user_id).first():
                 return jsonify({"msg": "Username already taken"}), 400
            user.username = new_username

        # 4. 保存更新后的用户对象
        user.save()

        # 5. 返回更新后的用户信息
        return jsonify(user.to_json()), 200

    except Exception as e:
        print(f"Error in update_me: {e}")
        return jsonify({"msg": "Server Error"}), 500 