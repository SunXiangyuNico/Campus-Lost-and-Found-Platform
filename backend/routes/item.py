from flask import Blueprint
from controllers.itemController import create_item, get_all_items, get_item_by_id, update_item, delete_item
from controllers.mapController import update_item_location
from middleware.auth import auth_middleware

# 创建一个名为 'items' 的 Blueprint
# url_prefix 会添加到此 Blueprint 中定义的所有路由前面
item_bp = Blueprint('items', __name__)

# 定义路由
# POST /api/items/ - 创建新物品 (私有)
item_bp.route('/', methods=['POST'])(auth_middleware(create_item))

# GET /api/items/ - 获取所有物品列表 (公开)
item_bp.route('/', methods=['GET'])(get_all_items)

# GET /api/items/<item_id> - 获取单个物品的详细信息 (公开)
item_bp.route('/<item_id>', methods=['GET'])(get_item_by_id)

# PUT /api/items/<item_id> - 更新物品信息 (私有)
item_bp.route('/<item_id>', methods=['PUT'])(auth_middleware(update_item))

# DELETE /api/items/<item_id> - 删除物品 (私有)
item_bp.route('/<item_id>', methods=['DELETE'])(auth_middleware(delete_item))

# PUT /api/items/<item_id>/location - 更新物品的地理位置 (私有)
item_bp.route('/<item_id>/location', methods=['PUT'])(auth_middleware(update_item_location)) 