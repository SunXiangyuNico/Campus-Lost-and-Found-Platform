from functools import wraps
from flask import request, jsonify
import jwt
import json
import os

# 从配置文件加载 JWT 密钥
def load_jwt_secret():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default.json')
    with open(config_path) as config_file:
        config = json.load(config_file)
    return config.get('jwtSecret')

JWT_SECRET = load_jwt_secret()

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
            # PyJWT 的 decode 方法会自动验证签名和过期时间
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            
            # 4. 将解码后的用户 ID 附加到 request 对象上，以便后续的控制器使用
            request.user_id = decoded['user']['id']

        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Token is not valid"}), 401
        except Exception as e:
            print(e)
            return jsonify({"msg": "Server error during token validation"}), 500

        # 5. 如果一切正常，调用原始的控制器函数
        return f(*args, **kwargs)

    return decorated_function 