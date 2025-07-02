from flask import request, jsonify
from models.Item import Item
from models.User import User
from services.matchingService import find_and_notify_matches
import json

def create_item(current_user):
    """
    创建一个新的失物或拾物条目
    支持 JSON 数据或 Form-data (用于图片上传)
    """
    try:
        data = {}
        # 兼容 form-data 和 application/json
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        # 基本的输入验证
        required_fields = ['name', 'description', 'category', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # 验证 category和status是否合法
        if data['category'] not in Item.CATEGORY_CHOICES:
            return jsonify({'message': 'Invalid category'}), 400
        if data['status'] not in Item.STATUS_CHOICES:
            return jsonify({'message': 'Invalid status'}), 400

        new_item = Item(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            status=data['status'],
            location=data.get('location'),
            user=current_user
        )
        
        # 处理地理坐标
        if 'coordinates' in data:
            try:
                # 假设坐标是 JSON 字符串 '{"longitude": 120, "latitude": 30}'
                coords = json.loads(data['coordinates'])
                new_item.coordinates = [coords['longitude'], coords['latitude']]
            except (json.JSONDecodeError, KeyError, TypeError):
                return jsonify({'message': 'Invalid coordinates format'}), 400
        
        # 图片上传逻辑 (简化版，实际生产需要更复杂的处理)
        # 此处我们仅保存URL，不处理实际文件上传
        if 'image_urls' in data:
            # 期望是一个字符串列表
            if isinstance(data['image_urls'], list):
                new_item.image_urls = data['image_urls']

        new_item.save()
        
        # 触发智能匹配和通知
        find_and_notify_matches(new_item)
        
        return jsonify({'message': 'Item created successfully', 'item': new_item.to_json()}), 201

    except Exception as e:
        return jsonify({'message': 'Failed to create item', 'error': str(e)}), 500

def get_all_items():
    """
    获取物品列表，支持过滤、排序和分页
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # 构建过滤查询
        query_filters = {}
        if request.args.get('status'):
            query_filters['status'] = request.args.get('status')
        if request.args.get('category'):
            query_filters['category'] = request.args.get('category')
        if request.args.get('q'): # 文本搜索
            query_filters['name__icontains'] = request.args.get('q')

        # 排序
        sort_by = request.args.get('sortBy', '-created_at') # 默认按创建时间降序
        
        # 查询并分页
        paginated_items = Item.objects.filter(**query_filters).order_by(sort_by).paginate(page=page, per_page=per_page)

        return jsonify({
            'items': [item.to_json() for item in paginated_items.items],
            'total': paginated_items.total,
            'pages': paginated_items.pages,
            'currentPage': paginated_items.page
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve items', 'error': str(e)}), 500

def get_item_by_id(item_id):
    """
    根据ID获取单个物品的详细信息
    """
    try:
        item = Item.objects.get(id=item_id)
        # 关联查询发布者信息
        user = User.objects.get(id=item.user.id)
        item_json = item.to_json()
        item_json['user'] = {
            'id': str(user.id),
            'username': user.username,
            'avatar': user.avatar
        }
        return jsonify(item_json), 200
    except Item.DoesNotExist:
        return jsonify({'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve item', 'error': str(e)}), 500

def update_item(current_user, item_id):
    """
    更新物品信息
    """
    try:
        item = Item.objects.get(id=item_id)
        
        # 验证权限
        if item.user.id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
            
        data = request.get_json()
        updatable_fields = ['name', 'description', 'category', 'status', 'location', 'image_urls']
        
        for field in updatable_fields:
            if field in data:
                setattr(item, field, data[field])
        
        if 'coordinates' in data:
            coords = data['coordinates']
            item.coordinates = [coords['longitude'], coords['latitude']]
            
        item.save()
        return jsonify({'message': 'Item updated successfully', 'item': item.to_json()}), 200

    except Item.DoesNotExist:
        return jsonify({'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to update item', 'error': str(e)}), 500

def delete_item(current_user, item_id):
    """
    删除物品
    """
    try:
        item = Item.objects.get(id=item_id)
        
        # 验证权限 (只有发布者或未来的管理员能删除)
        if item.user.id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
            
        item.delete()
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Item.DoesNotExist:
        return jsonify({'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Failed to delete item', 'error': str(e)}), 500 