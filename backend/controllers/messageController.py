from flask import request, jsonify
from models.Message import Message
from models.User import User
from models.Item import Item

def send_message(current_user):
    """
    发送私信
    POST /api/messages/
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['recipientId', 'itemId', 'content']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # 检查收件人是否存在
        recipient = User.objects(id=data['recipientId']).first()
        if not recipient:
            return jsonify({'message': 'Recipient not found'}), 404

        # 检查关联物品是否存在
        item = Item.objects(id=data['itemId']).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        
        # 不能给自己发消息
        if str(current_user.id) == data['recipientId']:
            return jsonify({'message': 'You cannot send a message to yourself'}), 400

        # 创建消息记录
        new_message = Message(
            sender_id=str(current_user.id),
            receiver_id=data['recipientId'],
            item_id=data['itemId'],
            content=data['content']
        )
        new_message.save()

        # 我们可以选择在这里给收件人发送一封邮件提醒
        # from services.notificationService import send_email
        # subject = f"您有一条来自 {current_user.username} 的新消息"
        # html_content = f"<h3>您好 {recipient.username},</h3><p>您收到了一条关于物品 {item.name} 的新消息。</p><p>内容: {data['content']}</p><p>请登录平台查看详情。</p>"
        # send_email(recipient.email, subject, html_content)

        return jsonify(new_message.to_json()), 201

    except Exception as e:
        return jsonify({'message': 'Failed to send message', 'error': str(e)}), 500

def get_conversations(current_user):
    """
    获取当前用户的所有对话列表
    GET /api/messages/conversations
    """
    try:
        current_user_id = str(current_user.id)
        
        # 使用聚合管道获取每个对话的最新一条消息
        pipeline = [
            {
                '$match': {
                    '$or': [{'sender_id': current_user_id}, {'receiver_id': current_user_id}]
                }
            },
            {
                '$sort': {'created_at': -1}
            },
            {
                '$group': {
                    '_id': {
                        '$cond': {
                           'if': { '$gt': ['$sender_id', '$receiver_id'] },
                           'then': { 'user1': '$receiver_id', 'user2': '$sender_id'},
                           'else': { 'user1': '$sender_id', 'user2': '$receiver_id'}
                        }
                    },
                    'lastMessage': {'$first': '$$ROOT'}
                }
            },
            {
                '$replaceRoot': {'newRoot': '$lastMessage'}
            },
            {
                '$sort': {'created_at': -1}
            }
        ]

        messages = Message.objects.aggregate(pipeline)
        
        conversations = []
        for msg_data in messages:
            other_user_id = msg_data['sender_id'] if msg_data['sender_id'] != current_user_id else msg_data['receiver_id']
            other_user = User.objects(id=other_user_id).first()
            item = Item.objects(id=msg_data['item_id']).first()

            if other_user and item:
                conversations.append({
                    'withUser': {
                        'id': str(other_user.id),
                        'username': other_user.username,
                        'avatar': other_user.avatar
                    },
                    'item': {
                        'id': str(item.id),
                        'name': item.name
                    },
                    'lastMessage': msg_data['content'][:50], # 预览
                    'timestamp': msg_data['created_at'].isoformat(),
                    'isRead': msg_data['is_read']
                })
        
        return jsonify(conversations), 200

    except Exception as e:
        return jsonify({'message': 'Failed to get conversations', 'error': str(e)}), 500

def get_messages_with_user(current_user, other_user_id):
    """
    获取与指定用户的消息历史
    GET /api/messages/<other_user_id>
    """
    try:
        current_user_id = str(current_user.id)
        
        # 验证对方用户是否存在
        other_user = User.objects(id=other_user_id).first()
        if not other_user:
            return jsonify({'message': 'User not found'}), 404
        
        # 查询消息记录
        messages = Message.objects(
            (Message.sender_id == current_user_id and Message.receiver_id == other_user_id) |
            (Message.sender_id == other_user_id and Message.receiver_id == current_user_id)
        ).order_by('created_at') # 按时间升序排列

        # 将发给当前用户的未读消息标记为已读
        Message.objects(
            sender_id=other_user_id, 
            receiver_id=current_user_id, 
            is_read=False
        ).update(set__is_read=True)

        return jsonify([msg.to_json(current_user_id=current_user_id) for msg in messages]), 200

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve messages', 'error': str(e)}), 500 