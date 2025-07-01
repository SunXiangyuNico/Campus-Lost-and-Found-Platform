from mongoengine import Document, StringField, DateTimeField, DictField, EnumField
from datetime import datetime
from enum import Enum

class ItemType(Enum):
    LOST = 'lost'
    FOUND = 'found'

class ItemStatus(Enum):
    PENDING = 'pending'
    RECLAIMED = 'reclaimed'

class Item(Document):
    """
    物品模型 - 匹配API文档的3.x物品相关接口
    """
    # 基础字段
    title = StringField(required=True, max_length=50)  # 匹配API的50字符限制
    description = StringField(required=True, max_length=1000)  # 匹配API的1000字符限制
    item_type = EnumField(ItemType, required=True)  # 对应API的'type'字段
    category = StringField(max_length=30)  # 如"电子产品"、"证件"
    location_text = StringField(max_length=100)  # 对应API的locationText
    coordinates = DictField()  # 存储 { "lat": 39.9, "lng": 116.4 }
    event_date = DateTimeField()  # 对应API的eventDate (存储为DateTime便于查询)
    image_url = StringField()  # 对应API的上传图片URL
    status = EnumField(ItemStatus, default=ItemStatus.PENDING)

    # 关联字段
    user_id = StringField(required=True)  # 关联User.id (MongoDB的ObjectId或自定义ID)

    # 元数据
    meta = {
        'collection': 'items',
        'indexes': [
            'title',  # 基础索引
            'item_type',
            'status',
            {'fields': ['coordinates'], 'cls': False}  # 地理空间索引(如果使用MongoDB地理查询)
        ],
        'timestamps': True  # 自动管理createdAt和updatedAt
    }

    def to_json(self, *args, **kwargs):
        """定制化JSON输出，完全匹配API文档格式"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "type": self.item_type.value,  # 使用.value输出字符串
            "category": self.category,
            "locationText": self.location_text,
            "eventDate": self.event_date.isoformat()[:10] if self.event_date else None,  # 转为YYYY-MM-DD
            "imageUrl": self.image_url,
            "coordinates": self.coordinates,
            "status": self.status.value,
            "createdAt": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            "updatedAt": self.updated_at.isoformat() if hasattr(self, 'updated_at') else None,
            "userId": self.user_id  # 注意命名与API文档一致
        }