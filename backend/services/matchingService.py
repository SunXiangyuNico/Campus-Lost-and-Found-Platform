from models.Item import Item
from services.notificationService import send_email

def find_and_notify_matches(new_item):
    """
    为一个新发布的物品寻找匹配项，并向相关用户发送邮件通知。

    :param new_item: 新创建的 Item 对象。
    """
    print(f"Starting matching process for item: {new_item.name}")

    # 确定要搜索的状态
    # 如果新物品是'lost'，我们就在'found'物品中搜索，反之亦然
    target_status = 'found' if new_item.status == 'lost' else 'lost'

    # 构建匹配查询
    # 简单的初版匹配逻辑：分类必须相同，并且名称或描述中包含关键词
    # 为了简化，我们将新物品名称按空格分割作为关键词
    keywords = new_item.name.split()
    query_conditions = {
        'status': target_status,
        'category': new_item.category,
        # 使用$in操作符来匹配任何一个关键词
        'name': {'$in': keywords} 
    }

    # 在数据库中查找匹配的物品
    # 使用 Q 对象可以构建更复杂的查询，但这里暂时用字典
    # from mongoengine.queryset.visitor import Q
    # query = (Q(status=target_status) & Q(category=new_item.category) & (Q(name__icontains=keyword) for keyword in keywords))
    
    potential_matches = Item.objects.filter(**query_conditions)

    if not potential_matches:
        print("No potential matches found.")
        return

    print(f"Found {len(potential_matches)} potential match(es).")
    
    # 获取新物品发布者的信息
    new_item_user = new_item.user

    # 为每个匹配的物品，向其发布者发送通知
    for match_item in potential_matches:
        match_user = match_item.user
        
        # 准备邮件内容
        # 1. 通知找到物品的人
        if new_item.status == 'lost':
            recipient_user = match_user # 拾到者
            lost_item_user = new_item_user # 失主
            subject = f"[失物线索] 您捡到的 {match_item.name} 可能与一则失物信息匹配"
            html_content = f"""
            <h3>您好 {recipient_user.username},</h3>
            <p>您好！您在校园失物招领平台发布的拾物信息 <strong>"{match_item.name}"</strong> 可能与一则新的失物信息相匹配。</p>
            <p><strong>失主描述：</strong>"{new_item.description}"</p>
            <p><strong>失主联系方式（邮箱）：</strong> {lost_item_user.email}</p>
            <p>请您核对信息，并考虑与失主取得联系。感谢您的热心帮助！</p>
            <p>-- 校园失物招领平台</p>
            """
            # send_email(recipient_user.email, subject, html_content)

        # 2. 通知丢失物品的人
        else: # new_item.status == 'found'
            recipient_user = new_item_user # 拾到者 (这里逻辑上应该是失主)
            lost_item_user = match_user # 失主
            subject = f"[失物线索] 您丢失的 {match_item.name} 可能有新线索了"
            html_content = f"""
            <h3>您好 {lost_item_user.username},</h3>
            <p>您好！您在校园失物招领平台发布的寻物启事 <strong>"{match_item.name}"</strong> 可能有新的线索了！</p>
            <p><strong>拾获物品描述：</strong>"{new_item.description}"</p>
            <p><strong>拾获者联系方式（邮箱）：</strong> {new_item_user.email}</p>
            <p>请您核对信息，并尽快与对方取得联系。祝您早日找回失物！</p>
            <p>-- 校园失物招领平台</p>
            """
            # send_email(lost_item_user.email, subject, html_content) 