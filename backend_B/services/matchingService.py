from datetime import datetime, timedelta
from difflib import SequenceMatcher
from typing import List, Dict
from models.Item import Item, ItemStatus
from models.User import User
from services.notificationService import send_notification

class MatchingService:
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """计算两个文本的相似度（0~1）"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    @staticmethod
    def find_potential_matches(new_item: Item) -> List[Dict]:
        """
        为新物品寻找潜在匹配
        返回格式: [{
            'match_item': Item,
            'similarity': float,
            'match_reasons': List[str]
        }]
        """
        # 定义搜索条件（根据业务需求调整）
        search_filters = {
            'status': ItemStatus.PENDING.value,
            'item_type': 'found' if new_item.item_type == 'lost' else 'lost'
        }
        
        # 获取候选物品（最近30天的数据）
        candidate_items = Item.query.filter(
            Item.created_at >= datetime.utcnow() - timedelta(days=30),
            **search_filters
        ).all()

        matches = []
        for candidate in candidate_items:
            similarity = 0
            match_reasons = []
            
            # 1. 名称相似度（权重50%）
            name_sim = MatchingService.calculate_similarity(
                new_item.title, 
                candidate.title
            )
            if name_sim > 0.6:  # 相似度阈值
                similarity += name_sim * 0.5
                match_reasons.append(f"名称相似度{name_sim:.0%}")

            # 2. 分类匹配（权重30%）
            if new_item.category == candidate.category:
                similarity += 0.3
                match_reasons.append("相同分类")

            # 3. 地理位置相近（权重20%）
            if (new_item.location and candidate.location and
                new_item.location.text == candidate.location.text):
                similarity += 0.2
                match_reasons.append("相同地点")

            # 只保留相似度>60%的匹配
            if similarity >= 0.6:
                matches.append({
                    'match_item': candidate,
                    'similarity': similarity,
                    'match_reasons': match_reasons
                })

        # 按相似度降序排序
        return sorted(matches, key=lambda x: x['similarity'], reverse=True)

    @staticmethod
    def trigger_matching_and_notify(new_item_id: int):
        """主服务方法：执行匹配并发送通知"""
        new_item = Item.query.get_or_404(new_item_id)
        
        # 跳过已解决的物品
        if new_item.status != ItemStatus.PENDING.value:
            return

        matches = MatchingService.find_potential_matches(new_item)
        if not matches:
            return

        # 获取物品所有者
        owner = User.query.get(new_item.user_id)
        if not owner:
            return

        # 构建通知内容
        best_match = matches[0]
        notification_content = (
            f"发现与您的{new_item.item_type}物品可能匹配的信息！\n"
            f"匹配度: {best_match['similarity']:.0%}\n"
            f"原因: {', '.join(best_match['match_reasons'])}\n"
            f"联系邮箱: {best_match['match_item'].author.email}"
        )

        # 发送通知（邮件/短信）
        send_notification(
            recipient=owner.email,
            subject="[失物招领] 发现潜在匹配",
            content=notification_content
        )

        # 记录匹配日志（可选）
        print(f"匹配触发: 物品ID {new_item_id} -> "
              f"匹配到 {len(matches)} 个结果，最高相似度 {best_match['similarity']:.0%}")