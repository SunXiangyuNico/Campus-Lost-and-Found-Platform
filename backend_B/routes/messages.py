from flask import Blueprint
from middleware.auth import auth_middleware
from controllers.messageController import (
    send_message,
    get_conversations,
    get_conversation_detail,
    mark_message_read
)

message_bp = Blueprint('message', __name__)

# --------------------------
# 需认证路由（全部私有）
# --------------------------
@message_bp.route('/messages', methods=['POST'])
@auth_middleware
def create_message():
    """发送私信（关联物品）"""
    return send_message()

@message_bp.route('/messages/conversations', methods=['GET'])
@auth_middleware
def list_conversations():
    """获取对话列表（按联系人分组）"""
    return get_conversations()

@message_bp.route('/messages/<string:user_id>', methods=['GET'])
@auth_middleware
def view_conversation(user_id):
    """查看与指定用户的历史消息"""
    return get_conversation_detail(user_id)

@message_bp.route('/messages/<string:message_id>/read', methods=['PATCH'])
@auth_middleware
def mark_as_read(message_id):
    """将消息标记为已读"""
    return mark_message_read(message_id)