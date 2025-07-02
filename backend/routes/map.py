from flask import Blueprint
from controllers.mapController import get_items_in_viewport, get_nearby_items

# 创建一个名为 'map' 的 Blueprint
map_bp = Blueprint('map', __name__, url_prefix='/api/map')

# GET /api/map/items - 获取地图视野内的物品标记点 (公开)
map_bp.route('/items', methods=['GET'])(get_items_in_viewport)

# GET /api/map/nearby - 根据经纬度查询附近的物品 (公开)
map_bp.route('/nearby', methods=['GET'])(get_nearby_items) 