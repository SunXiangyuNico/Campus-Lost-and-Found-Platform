from flask import Blueprint
from controllers.messageController import send_message, get_conversations, get_messages_with_user
from middleware.auth import auth_middleware

# 创建一个名为 'messages' 的 Blueprint
message_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

# POST /api/messages/ - 发送一条新消息 (私有)
message_bp.route('/', methods=['POST'])(auth_middleware(send_message))

# GET /api/messages/conversations - 获取当前用户的所有对话列表 (私有)
message_bp.route('/conversations', methods=['GET'])(auth_middleware(get_conversations))

# GET /api/messages/<other_user_id> - 获取与指定用户的消息历史 (私有)
message_bp.route('/<other_user_id>', methods=['GET'])(auth_middleware(get_messages_with_user)) 