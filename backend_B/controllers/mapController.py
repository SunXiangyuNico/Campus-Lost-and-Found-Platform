from flask import request, jsonify
from models.Item import Item
from extensions import db
from middleware.auth import auth_middleware
from geopy.distance import geodesic
import math

class MapController:
    
    @staticmethod
    def get_items_in_viewport():
        """
        获取地图视野内的物品标记点 (对应API 8.1)
        GET /api/v1/map/items
        参数: ne_lat, ne_lng (东北角坐标), sw_lat, sw_lng (西南角坐标)
        """
        try:
            # 验证并获取坐标参数
            ne_lat = float(request.args.get('ne_lat'))
            ne_lng = float(request.args.get('ne_lng'))
            sw_lat = float(request.args.get('sw_lat'))
            sw_lng = float(request.args.get('sw_lng'))

            # 验证坐标有效性
            if not (-90 <= ne_lat <= 90) or not (-180 <= ne_lng <= 180) or \
               not (-90 <= sw_lat <= 90) or not (-180 <= sw_lng <= 180):
                return jsonify({'error': '无效的坐标范围'}), 400

            # 查询地图矩形区域内的物品
            items = Item.query.filter(
                db.and_(
                    Item.coordinates['lat'].astext.cast(db.Float) >= sw_lat,
                    Item.coordinates['lat'].astext.cast(db.Float) <= ne_lat,
                    Item.coordinates['lng'].astext.cast(db.Float) >= sw_lng,
                    Item.coordinates['lng'].astext.cast(db.Float) <= ne_lng,
                    Item.status == 'pending'  # 只显示未解决的物品
                )
            ).limit(100).all()  # 限制返回数量防止过载

            result = [{
                'id': str(item.id),
                'title': item.title,
                'type': item.item_type,
                'coordinates': {
                    'lat': float(item.coordinates['lat']),
                    'lng': float(item.coordinates['lng'])
                },
                'category': item.category
            } for item in items]

            return jsonify(result)

        except ValueError:
            return jsonify({'error': '坐标参数必须为数字'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @auth_middleware
    def update_item_location(item_id):
        """
        更新物品位置坐标 (扩展API)
        PUT /api/v1/items/<item_id>/location
        需要认证且必须是物品所有者
        """
        try:
            current_user_id = request.user_id
            item = Item.query.get_or_404(item_id)

            # 验证权限
            if str(item.user_id) != current_user_id:
                return jsonify({'error': '无权修改此物品'}), 403

            data = request.get_json()
            lat = float(data.get('lat'))
            lng = float(data.get('lng'))

            # 验证坐标有效性
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return jsonify({'error': '无效的经纬度'}), 400

            # 更新坐标
            item.coordinates = {'lat': lat, 'lng': lng}
            db.session.commit()

            return jsonify({
                'status': 'success',
                'newLocation': item.coordinates
            })

        except ValueError:
            return jsonify({'error': '经纬度必须为数字'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_nearby_items():
        """
        获取附近物品 (扩展功能)
        GET /api/v1/map/nearby?lat=xx&lng=xx&radius=xx&limit=xx
        """
        try:
            # 获取参数并设置默认值
            lat = float(request.args.get('lat'))
            lng = float(request.args.get('lng'))
            radius = float(request.args.get('radius', 1.0))  # 默认1公里
            limit = int(request.args.get('limit', 20))      # 默认返回20条

            # 验证坐标
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return jsonify({'error': '无效的经纬度'}), 400

            # 获取所有待匹配物品（可根据实际数据量添加更多过滤条件）
            all_items = Item.query.filter_by(status='pending').all()

            nearby_items = []
            for item in all_items:
                if not item.coordinates:
                    continue

                item_lat = float(item.coordinates['lat'])
                item_lng = float(item.coordinates['lng'])

                # 计算距离（使用geodesic更精确）
                distance = geodesic((lat, lng), (item_lat, item_lng)).kilometers

                if distance <= radius:
                    nearby_items.append({
                        'item': {
                            'id': str(item.id),
                            'title': item.title,
                            'type': item.item_type,
                            'distance': round(distance, 2)
                        },
                        'coordinates': item.coordinates
                    })

            # 按距离排序并限制数量
            nearby_items.sort(key=lambda x: x['item']['distance'])
            result = [item['item'] for item in nearby_items[:limit]]

            return jsonify(result)

        except ValueError:
            return jsonify({'error': '参数必须为数字'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500