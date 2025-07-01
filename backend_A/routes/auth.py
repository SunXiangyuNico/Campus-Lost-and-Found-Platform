from flask import Blueprint
from controllers.authController import register_user, login_user, get_me
from middleware.auth import auth_middleware

# 创建一个名为 'auth' 的蓝图 (Blueprint)
# 蓝图用于组织一组相关的路由，使其模块化
auth_bp = Blueprint('auth', __name__)

# @route   POST /api/auth/register
# @desc    注册新用户
# @access  Public
auth_bp.route('/register', methods=['POST'])(register_user)

# @route   POST /api/auth/login
# @desc    用户登录并获取 token
# @access  Public
auth_bp.route('/login', methods=['POST'])(login_user)

# @route   GET /api/auth/me
# @desc    获取当前登录用户的信息
# @access  Private
# 使用 @auth_middleware 装饰器来保护这个路由
auth_bp.route('/me', methods=['GET'])(auth_middleware(get_me)) 