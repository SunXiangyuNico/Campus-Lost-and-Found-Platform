<template>
  <div class="post-list-container">
    <div class="post-list-scroll">
      <div 
        v-for="post in filteredPosts" 
        :key="post.id" 
        :class="['post-card', { selected: post.id === selectedId }]" 
        @click="$emit('select', post.id)"
      >
        <div class="post-header">
          <div class="post-type-badge" :class="post.type">
            <svg v-if="post.type === 'lost'" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.7088 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.76488 14.1003 1.98232 16.07 2.85999" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ post.type === 'lost' ? '失物' : '招领' }}
          </div>
          <div class="post-title">{{ post.title }}</div>
          <div class="post-meta">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>{{ post.location }}</span>
            <span class="dot">·</span>
            <span class="author-name">{{ post.nickname }}</span>
            <span class="dot">·</span>
            <span class="post-time">{{ formatTime(post.time) }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="filteredPosts.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <p>暂无相关帖子</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  posts: Array,
  selectedId: Number
})

const filteredPosts = computed(() => props.posts)

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
</script>

<style scoped>
.post-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.post-list-scroll {
  flex: 1;
  padding: var(--spacing-md);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.post-card {
  background: var(--bg-white);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  min-height: 44px;
  display: flex;
  align-items: center;
}

.post-card:hover {
  border-color: var(--brand-blue-light);
  box-shadow: var(--shadow-medium);
  transform: translateY(-1px);
}

.post-card.selected {
  border-color: var(--brand-blue);
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.05), rgba(74, 144, 226, 0.02));
  box-shadow: 0 0 0 1px var(--brand-blue), var(--shadow-light);
}

.post-card.selected::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--brand-blue);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.post-header {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 10px;
}

.post-type-badge {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.post-type-badge.lost {
  background: rgba(245, 108, 108, 0.08);
  color: var(--status-lost);
  border: 1px solid rgba(245, 108, 108, 0.15);
}

.post-type-badge.found {
  background: rgba(103, 194, 58, 0.08);
  color: var(--status-found);
  border: 1px solid rgba(103, 194, 58, 0.15);
}

.post-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
}

.author-name {
  color: var(--text-secondary);
  font-weight: 400;
}

.post-time {
  color: var(--text-muted);
}

.dot {
  margin: 0 2px;
  color: var(--text-light);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  margin-bottom: var(--spacing-md);
  color: var(--text-light);
}

.empty-state p {
  margin: 0;
  font-size: var(--font-size-sm);
  font-weight: 500;
}

/* 滚动条样式 */
.post-list-scroll::-webkit-scrollbar {
  width: 4px;
}

.post-list-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.post-list-scroll::-webkit-scrollbar-thumb {
  background: var(--border-medium);
  border-radius: 2px;
}

.post-list-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--text-light);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-list-scroll {
    padding: var(--spacing-md);
  }
  
  .post-card {
    padding: var(--spacing-md);
  }
  
  .post-title {
    font-size: var(--font-size-sm);
  }
}
</style> 