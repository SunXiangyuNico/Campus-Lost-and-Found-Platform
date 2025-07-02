from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, PointField
from datetime import datetime
from .User import User

class Item(Document):
    """
    失物招ling物品的数据模型
    """
    # 物品状态的选项
    STATUS_CHOICES = ('lost', 'found')
    
    # 物品分类的选项
    CATEGORY_CHOICES = ('electronics', 'keys', 'books', 'clothing', 'documents', 'others')

    name = StringField(required=True, max_length=100)
    description = StringField(required=True, max_length=500)
    category = StringField(required=True, choices=CATEGORY_CHOICES)
    status = StringField(required=True, choices=STATUS_CHOICES) # 'lost' 或 'found'
    location = StringField(max_length=200) # 丢失或拾获的地点
    
    # 新增：用于存储地理位置坐标，方便地图查询
    coordinates = PointField() # [经度, 纬度]
    
    # 关联到发布该物品的用户
    user = ReferenceField(User, required=True)
    
    # 物品图片的URL列表
    image_urls = ListField(StringField())
    
    # 创建和更新的时间戳
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        """重写save方法，在保存时自动更新updated_at"""
        self.updated_at = datetime.utcnow()
        return super(Item, self).save(*args, **kwargs)

    def to_json(self):
        """将文档对象转换为可序列化为JSON的字典"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "location": self.location,
            "coordinates": {
                "longitude": self.coordinates['coordinates'][0],
                "latitude": self.coordinates['coordinates'][1]
            } if self.coordinates else None,
            "user": str(self.user.id), # 返回用户的ID
            "image_urls": self.image_urls,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    meta = {
        'collection': 'items',
        'indexes': [
            'name',
            'category',
            'status',
            'coordinates' # 为地理空间查询创建索引
        ]
    } 