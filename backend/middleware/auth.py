from functools import wraps
from flask import request, jsonify
import jwt
import os
from models.User import User

# 直接从环境变量中获取 JWT 密钥
JWT_SECRET = os.environ.get('JWT_SECRET')

def auth_middleware(f):
    """
    认证中间件装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. 从请求头中获取 'Authorization' 字段
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"msg": "No token, authorization denied"}), 401

        try:
            # 2. 检查 Token 的格式是否为 "Bearer <token>"
            parts = auth_header.split()
            if parts[0].lower() != 'bearer' or len(parts) != 2:
                return jsonify({"msg": "Token format must be 'Bearer <token>'"}), 401
            
            token = parts[1]

            # 3. 验证 Token
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = decoded['user']['id']
            
            # 4. 从数据库中获取用户对象
            current_user = User.objects(id=user_id).first()

            if not current_user:
                return jsonify({"msg": "User not found"}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Token is not valid"}), 401
        except Exception as e:
            print(e)
            return jsonify({"msg": "Server error during token validation"}), 500

        # 5. 如果一切正常，将被认证的用户对象作为第一个参数传递给原始的控制器函数
        return f(current_user, *args, **kwargs)

    return decorated_function 