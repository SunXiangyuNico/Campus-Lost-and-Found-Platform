<template>
  <div 
    class="post-card" 
    :class="{ active: isActive }"
    @click="$emit('select', post)"
  >
    <div class="post-header">
      <el-tag 
        :type="post.type === 'lost' ? 'danger' : 'success'"
        size="small"
      >
        {{ post.type === 'lost' ? '失物' : '招领' }}
      </el-tag>
      <span class="post-time">{{ formatTime(post.createdAt) }}</span>
    </div>
    
    <div class="post-title">{{ post.title }}</div>
    
    <div class="post-location">
      <el-icon><Location /></el-icon>
      <span>{{ post.location }}</span>
    </div>
    
    <div class="post-author">
      <el-avatar :src="post.author.avatar" :size="20" />
      <span>{{ post.author.nickname }}</span>
    </div>
  </div>
</template>

<script setup>
import { Location } from '@element-plus/icons-vue'

defineProps({
  post: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select'])

const formatTime = (time) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 1天内
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return date.toLocaleDateString()
  }
}
</script>

<style scoped>
.post-card {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  background-color: #f5f7fa;
}

.post-card.active {
  background-color: #ecf5ff;
  border-left: 3px solid #409eff;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.post-time {
  font-size: 12px;
  color: #909399;
}

.post-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.4;
}

.post-location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;
}
</style> 