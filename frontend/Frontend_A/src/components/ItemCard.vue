<template>
  <div class="item-card" @click="$emit('click')">
    <div class="item-image">
      <img :src="item.imageUrl || '/placeholder.jpg'" :alt="item.title" />
      <div class="item-status" :class="item.status">
        {{ item.status === 'lost' ? '失物' : '拾物' }}
      </div>
    </div>
    
    <div class="item-content">
      <h3 class="item-title">{{ item.title }}</h3>
      <p class="item-description">{{ item.description }}</p>
      
      <div class="item-meta">
        <div class="meta-item">
          <el-icon><Location /></el-icon>
          <span>{{ item.location }}</span>
        </div>
        <div class="meta-item">
          <el-icon><Clock /></el-icon>
          <span>{{ formatDate(item.date) }}</span>
        </div>
      </div>
      
      <div class="item-footer">
        <span class="publisher">{{ item.user?.username }}</span>
        <el-tag :type="item.isResolved ? 'success' : 'warning'" size="small">
          {{ item.isResolved ? '已解决' : '未解决' }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script>
import { defineProps } from 'vue'

export default {
  name: 'ItemCard',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  emits: ['click'],
  setup() {
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    return {
      formatDate
    }
  }
}
</script>

<style scoped>
.item-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.item-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.item-status.lost {
  background-color: #f56c6c;
}

.item-status.found {
  background-color: #67c23a;
}

.item-content {
  padding: 16px;
}

.item-title {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.item-description {
  margin: 0 0 12px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 12px;
  color: #909399;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.publisher {
  font-size: 12px;
  color: #909399;
}
</style> 