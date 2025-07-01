from flask import request, jsonify
from datetime import datetime
from models.Message import Message
from models.User import User
from models.Item import Item
from extensions import db
from middleware.auth import auth_middleware

class MessageController:
    
    @staticmethod
    @auth_middleware
    def send_message():
        """
        发送站内信 (对应API 6.1)
        POST /api/v1/messages
        """
        try:
            current_user_id = request.user_id  # 从中间件获取
            data = request.get_json()
            
            # 验证必填字段
            required_fields = ['recipientId', 'itemId', 'content']
            if not all(field in data for field in required_fields):
                return jsonify({'error': '缺少必要字段'}), 400

            # 检查收件人是否存在
            recipient = User.query.get(data['recipientId'])
            if not recipient:
                return jsonify({'error': '收件人不存在'}), 404

            # 检查关联物品是否存在
            item = Item.query.get(data['itemId'])
            if not item:
                return jsonify({'error': '关联物品不存在'}), 404

            # 创建消息记录
            new_message = Message(
                sender_id=current_user_id,
                receiver_id=data['recipientId'],
                item_id=data['itemId'],
                content=data['content']
            )
            
            db.session.add(new_message)
            db.session.commit()

            return jsonify({
                'messageId': str(new_message.id),
                'timestamp': new_message.created_at.isoformat()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @auth_middleware
    def get_conversations():
        """
        获取对话列表 (对应API 6.2)
        GET /api/v1/messages/conversations
        """
        try:
            current_user_id = request.user_id

            # 获取最近对话（按联系人分组）
            subquery = db.session.query(
                Message.sender_id,
                Message.receiver_id,
                db.func.max(Message.created_at).label('max_date')
            ).filter(
                (Message.sender_id == current_user_id) |
                (Message.receiver_id == current_user_id)
            ).group_by(
                db.func.least(Message.sender_id, Message.receiver_id),
                db.func.greatest(Message.sender_id, Message.receiver_id)
            ).subquery()

            conversations = db.session.query(
                Message,
                User.username
            ).join(
                subquery,
                (Message.sender_id == subquery.c.sender_id) &
                (Message.receiver_id == subquery.c.receiver_id) &
                (Message.created_at == subquery.c.max_date)
            ).join(
                User,
                (User.id != current_user_id) &
                ((User.id == Message.sender_id) | (User.id == Message.receiver_id))
            ).all()

            result = []
            for msg, username in conversations:
                result.append({
                    'withUser': {
                        'id': str(msg.sender_id if msg.sender_id != current_user_id else msg.receiver_id),
                        'username': username
                    },
                    'lastMessage': msg.content[:50],  # 截取前50字符预览
                    'timestamp': msg.created_at.isoformat()
                })

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @auth_middleware
    def get_conversation(user_id):
        """
        获取与特定用户的对话详情 (对应API 6.3)
        GET /api/v1/messages/<user_id>
        """
        try:
            current_user_id = request.user_id

            # 验证对方用户是否存在
            other_user = User.query.get(user_id)
            if not other_user:
                return jsonify({'error': '用户不存在'}), 404

            # 获取分页参数
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)

            # 查询双方消息记录
            messages = Message.query.filter(
                ((Message.sender_id == current_user_id) & 
                 (Message.receiver_id == user_id)) |
                ((Message.sender_id == user_id) & 
                 (Message.receiver_id == current_user_id))
            ).order_by(
                Message.created_at.desc()
            ).paginate(page=page, per_page=per_page)

            result = [{
                'id': str(msg.id),
                'sender': 'me' if msg.sender_id == current_user_id else 'them',
                'content': msg.content,
                'timestamp': msg.created_at.isoformat(),
                'itemId': str(msg.item_id) if msg.item_id else None
            } for msg in messages.items]

            return jsonify({
                'messages': result,
                'totalPages': messages.pages,
                'currentPage': page
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @auth_middleware
    def mark_as_read(message_id):
        """
        标记消息为已读 (对应API 7.2)
        PATCH /api/v1/messages/<message_id>/read
        """
        try:
            message = Message.query.get_or_404(message_id)
            current_user_id = request.user_id

            # 验证消息归属
            if message.receiver_id != current_user_id:
                return jsonify({'error': '无权操作此消息'}), 403

            message.is_read = True
            db.session.commit()

            return jsonify({'status': 'success'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500