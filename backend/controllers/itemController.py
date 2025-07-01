from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from models.Item import Item, ItemStatus
from models.User import User
from services.matchingService import MatchingService
from extensions import db
from middleware.auth import auth_middleware

class ItemController:
    
    # --------------------------
    # 物品基础操作
    # --------------------------
    
    @staticmethod
    def create_item():
        """创建物品（API 3.1）"""
        try:
            # 获取表单数据
            user_id = request.form.get('userId')
            title = request.form.get('title')
            description = request.form.get('description')
            item_type = request.form.get('type')  # 'lost' or 'found'
            category = request.form.get('category')
            location_text = request.form.get('locationText')
            event_date_str = request.form.get('eventDate')
            coordinates = request.form.get('coordinates')  # JSON字符串
            
            # 验证必填字段
            if not all([user_id, title, description, item_type]):
                return jsonify({'error': '缺少必要字段'}), 400

            # 处理图片上传
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '':
                    filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
                    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items')
                    os.makedirs(upload_dir, exist_ok=True)
                    filepath = os.path.join(upload_dir, filename)
                    file.save(filepath)
                    image_url = f"/uploads/items/{filename}"

            # 创建物品记录
            new_item = Item(
                user_id=user_id,
                title=title,
                description=description,
                item_type=item_type,
                category=category,
                location_text=location_text,
                coordinates=coordinates if coordinates else None,
                event_date=datetime.strptime(event_date_str, '%Y-%m-%d') if event_date_str else None,
                image_url=image_url,
                status=ItemStatus.PENDING.value
            )
            
            db.session.add(new_item)
            db.session.commit()
            
            # 触发智能匹配（异步）
            MatchingService.trigger_matching_and_notify(new_item.id)
            
            return jsonify({
                'id': new_item.id,
                'title': new_item.title,
                'type': new_item.item_type,
                'createdAt': new_item.created_at.isoformat()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_items():
        """获取物品列表（API 3.2）"""
        try:
            # 解析查询参数
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            item_type = request.args.get('type')
            category = request.args.get('category')
            sort_by = request.args.get('sortBy', 'createdAt')
            direction = request.args.get('direction', 'desc')

            # 构建查询
            query = Item.query.filter_by(status=ItemStatus.PENDING.value)
            if item_type:
                query = query.filter_by(item_type=item_type)
            if category:
                query = query.filter_by(category=category)
            
            # 排序
            order_field = getattr(Item, sort_by)
            query = query.order_by(order_field.desc() if direction == 'desc' else order_field.asc())
            
            # 分页
            pagination = query.paginate(page=page, per_page=per_page)
            items = [{
                'id': item.id,
                'title': item.title,
                'type': item.item_type,
                'locationText': item.location_text,
                'imageUrl': item.image_url,
                'createdAt': item.created_at.isoformat()
            } for item in pagination.items]
            
            return jsonify({
                'items': items,
                'total': pagination.total,
                'pages': pagination.pages,
                'currentPage': page
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # --------------------------
    # 物品高级操作
    # --------------------------
    
    @staticmethod
    @auth_middleware
    def update_item(item_id):
        """更新物品信息（API 3.5）"""
        try:
            item = Item.query.get_or_404(item_id)
            current_user_id = request.user_id  # 从中间件获取
            
            # 检查权限
            if str(item.user_id) != current_user_id:
                return jsonify({'error': '无权修改此物品'}), 403
            
            data = request.get_json()
            updatable_fields = ['title', 'description', 'category', 'locationText', 'coordinates']
            for field in updatable_fields:
                if field in data:
                    setattr(item, field, data[field])
            
            item.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'id': item.id,
                'title': item.title,
                'updatedAt': item.updated_at.isoformat()
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @auth_middleware
    def delete_item(item_id):
        """删除物品（API 3.6）"""
        try:
            item = Item.query.get_or_404(item_id)
            current_user_id = request.user_id
            
            # 检查权限（发布者或管理员）
            if str(item.user_id) != current_user_id and not request.is_admin:
                return jsonify({'error': '无权删除此物品'}), 403
            
            # 删除关联图片
            if item.image_url:
                image_path = os.path.join(current_app.static_folder, item.image_url.lstrip('/'))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': '物品删除成功'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # --------------------------
    # 图片上传（单独接口）
    # --------------------------
    
    @staticmethod
    @auth_middleware
    def upload_item_image(item_id):
        """上传物品图片（API 5.1）"""
        try:
            item = Item.query.get_or_404(item_id)
            current_user_id = request.user_id
            
            if str(item.user_id) != current_user_id:
                return jsonify({'error': '无权修改此物品'}), 403
            
            if 'image' not in request.files:
                return jsonify({'error': '未提供图片文件'}), 400
                
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': '空文件名'}), 400
                
            # 删除旧图片
            if item.image_url:
                old_path = os.path.join(current_app.static_folder, item.image_url.lstrip('/'))
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # 保存新图片
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items')
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            # 更新数据库
            item.image_url = f"/uploads/items/{filename}"
            db.session.commit()
            
            return jsonify({
                'imageUrl': item.image_url,
                'message': '图片上传成功'
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # --------------------------
    # 智能匹配相关
    # --------------------------
    
    @staticmethod
    @auth_middleware
    def get_item_matches(item_id):
        """获取物品匹配结果（API 3.8）"""
        try:
            item = Item.query.get_or_404(item_id)
            current_user_id = request.user_id
            
            if str(item.user_id) != current_user_id:
                return jsonify({'error': '无权查看此物品的匹配结果'}), 403
            
            matches = MatchingService.find_potential_matches(item)
            return jsonify([{
                'id': match['match_item'].id,
                'title': match['match_item'].title,
                'similarity': match['similarity'],
                'reasons': match['match_reasons']
            } for match in matches])
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500