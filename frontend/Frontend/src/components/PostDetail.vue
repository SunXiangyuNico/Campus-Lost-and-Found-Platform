<template>
  <div class="post-detail">
    <!-- 用户信息头部 -->
    <div class="post-header">
      <div class="user-info">
        <el-avatar :src="post.avatar" size="large" />
        <div class="user-details">
          <div class="user-name">{{ post.nickname }}</div>
          <div class="post-meta">
            <span class="post-time">{{ formatTime(post.time) }}</span>
            <span class="post-type-badge" :class="post.type">
              {{ post.type === 'lost' ? '失物' : '招领' }}
            </span>
          </div>
        </div>
      </div>
      <div class="post-actions">
        <el-button 
          type="primary" 
          size="large"
          :disabled="post.claimed" 
          @click="onContact"
          class="contact-btn"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 2H2C1.46957 2 0.960859 2.21071 0.585786 2.58579C0.210714 2.96086 0 3.46957 0 4V22C0 22.5304 0.210714 23.0391 0.585786 23.4142C0.960859 23.7893 1.46957 24 2 24H22C22.5304 24 23.0391 23.7893 23.4142 23.4142C23.7893 23.0391 24 22.5304 24 22V4C24 3.46957 23.7893 2.96086 23.4142 2.58579C23.0391 2.21071 22.5304 2 22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          {{ post.claimed ? '已认领' : (post.type === 'lost' ? '联系拾主' : '联系失主') }}
        </el-button>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          物品描述
        </h3>
        <p class="post-description">{{ post.desc }}</p>
      </div>

      <!-- 图片展示 -->
      <div v-if="post.images && post.images.length" class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="8.5" cy="8.5" r="1.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="21,15 16,10 5,21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          相关图片
        </h3>
        <div class="image-gallery">
          <div 
            v-for="(img, idx) in post.images" 
            :key="idx" 
            class="image-item"
            @click="previewImage(img)"
          >
            <img :src="img" :alt="`图片 ${idx + 1}`" />
          </div>
        </div>
      </div>

      <!-- 地点信息 -->
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          丢失/拾取地点
        </h3>
        <div class="location-info">
          <div class="location-text">{{ post.locationText }}</div>
          <div class="map-container">
            <img :src="mapImg" class="map-img" alt="校园地图" />
            <div v-if="post.locationCoord" class="map-marker" :style="markerStyle"></div>
          </div>
        </div>
      </div>

      <!-- 评论区 -->
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          评论区
        </h3>
        
        <div v-if="post.comments && post.comments.length" class="comments-list">
          <div v-for="(comment, i) in post.comments" :key="i" class="comment-item">
            <el-avatar :src="comment.avatar" size="small" />
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author">{{ comment.nickname }}</span>
                <span class="comment-time">{{ formatTime(comment.time) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-comments">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无评论</p>
        </div>
        
        <div class="comment-input">
          <el-input 
            v-model="commentText" 
            placeholder="写下你的评论..." 
            type="textarea"
            :rows="3"
            maxlength="200"
            show-word-limit
          />
          <el-button 
            type="primary" 
            @click="onSendComment" 
            :disabled="!commentText.trim()"
            class="send-btn"
          >
            发送评论
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  mapImg: {
    type: String,
    required: false
  },
  isLogin: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['claim', 'comment', 'require-login'])
const commentText = ref('')

function formatTime(timeStr) {
  const date = new Date(timeStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) {
    return '今天'
  } else if (diffDays === 2) {
    return '昨天'
  } else if (diffDays <= 7) {
    return `${diffDays - 1}天前`
  } else {
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  }
}

function onContact() {
  if (props.post.claimed) {
    ElMessage.info('该物品已被认领')
    return
  }
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再联系！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }
  emit('claim', props.post)
  ElMessage.success('已发送联系请求')
}

function onSendComment() {
  if (!commentText.value.trim()) return
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再评论！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }
  emit('comment', commentText.value)
  ElMessage.success('评论已发送')
  commentText.value = ''
}

function previewImage(img) {
  // 这里可以实现图片预览功能
  window.open(img, '_blank')
}

// 当帖子切换时清空评论输入框
watch(() => props.post.id, () => { 
  commentText.value = '' 
})

const markerStyle = computed(() => {
  if (!props.post.locationCoord) return {}
  const [x, y] = props.post.locationCoord
  return {
    left: x + 'px',
    top: y + 'px'
  }
})
</script>

<style scoped>
.post-detail {
  background: var(--bg-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-light);
  overflow: hidden;
}

.post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(135deg, var(--bg-gray), var(--bg-white));
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.user-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.post-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.post-time {
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

.post-type-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.post-type-badge.lost {
  background: rgba(245, 108, 108, 0.1);
  color: var(--status-lost);
  border: 1px solid rgba(245, 108, 108, 0.2);
}

.post-type-badge.found {
  background: rgba(103, 194, 58, 0.1);
  color: var(--status-found);
  border: 1px solid rgba(103, 194, 58, 0.2);
}

.contact-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-lg);
  font-weight: 500;
  border-radius: var(--radius-lg);
}

.post-content {
  padding: var(--spacing-xl);
}

.post-title {
  margin: 0 0 var(--spacing-xl) 0;
  font-size: var(--font-size-title);
  font-weight: 700;
  color: var(--text-primary);
  line-height: var(--line-height-tight);
}

.content-section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.post-description {
  margin: 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-relaxed);
  color: var(--text-secondary);
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.image-item {
  aspect-ratio: 4/3;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.image-item:hover {
  transform: scale(1.02);
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.location-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.location-text {
  font-size: var(--font-size-md);
  font-weight: 500;
  color: var(--text-primary);
  text-align: center;
}

.map-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 300px;
  margin: 0 auto;
  background: var(--bg-gray);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-light);
}

.map-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.map-marker {
  position: absolute;
  width: 24px;
  height: 24px;
  background: var(--status-lost);
  border: 3px solid white;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: var(--shadow-medium);
  z-index: 2;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-gray);
  border-radius: var(--radius-lg);
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary);
}

.comment-time {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.comment-text {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
  color: var(--text-secondary);
}

.empty-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-xl);
  color: var(--text-muted);
  text-align: center;
}

.empty-comments svg {
  margin-bottom: var(--spacing-md);
  color: var(--text-light);
}

.empty-comments p {
  margin: 0;
  font-size: var(--font-size-sm);
}

.comment-input {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.send-btn {
  align-self: flex-end;
  padding: var(--spacing-sm) var(--spacing-lg);
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
  }
  
  .post-content {
    padding: var(--spacing-lg);
  }
  
  .post-title {
    font-size: var(--font-size-xl);
  }
  
  .image-gallery {
    grid-template-columns: 1fr;
  }
  
  .map-container {
    height: 200px;
  }
}
</style> 