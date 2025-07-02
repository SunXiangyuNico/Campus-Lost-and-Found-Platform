from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime

class Message(Document):
    """
    消息模型 - 匹配API文档的6.x消息接口
    """
    # 内容字段
    content = StringField(required=True, max_length=1000)  # 限制消息长度
    is_read = BooleanField(default=False)  # 对应API的已读状态

    # 关联字段
    sender_id = StringField(required=True)  # 发送者User.id
    receiver_id = StringField(required=True)  # 接收者User.id
    item_id = StringField(required=True)  # 关联Item.id

    # 元数据
    meta = {
        'collection': 'messages',
        'indexes': [
            'sender_id',
            'receiver_id',
            'item_id',
            ('sender_id', 'receiver_id')  # 复合索引加速对话查询
        ],
        'timestamps': True  # 自动时间戳
    }

    def to_json(self, *args, **kwargs):
        """匹配API文档的消息格式"""
        return {
            "id": str(self.id),
            "content": self.content,
            "isRead": self.is_read,
            "senderId": self.sender_id,
            "receiverId": self.receiver_id,
            "itemId": self.item_id,
            "timestamp": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            # 以下为API文档6.3接口需要的字段
            "sender": "me" if kwargs.get('current_user_id') == self.sender_id else "them"
        } 