<template>
  <el-card class="post-list-card">
    <el-scrollbar class="post-list-scroll">
      <div v-for="post in filteredPosts" :key="post.id" :class="['post-list-item', {selected: post.id === selectedId}]" @click="$emit('select', post.id)">
        <el-tag :type="post.type === 'lost' ? 'danger' : 'success'" size="small">{{ post.type === 'lost' ? '失物' : '招领' }}</el-tag>
        <span class="title">{{ post.title }}</span>
        <div class="meta">
          <el-icon><el-icon-location /></el-icon> {{ post.location }}
        </div>
        <div class="meta">
          <el-icon><el-icon-user /></el-icon> {{ post.nickname }}
          <span class="time">{{ post.time }}</span>
        </div>
      </div>
      <el-empty v-if="filteredPosts.length === 0" description="暂无相关帖子" />
    </el-scrollbar>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  posts: Array,
  selectedId: Number
})
const filteredPosts = computed(() => props.posts)
</script>

<style scoped>
.post-list-card {
  padding: 0 0 8px 0;
  border-radius: 12px;
  min-width: 280px;
  max-width: 340px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.post-list-scroll {
  flex: 1;
  padding: 0 8px 8px 8px;
  overflow-y: auto;
}
.post-list-item {
  background: #f7f8fa;
  border-radius: 8px;
  padding: 10px 12px 8px 12px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  border: 1.5px solid transparent;
}
.post-list-item.selected {
  background: #e6f7ff;
  border-color: #409eff;
  box-shadow: 0 2px 8px #e6f7ff;
}
.title {
  font-weight: 500;
  font-size: 17px;
  margin-left: 8px;
}
.meta {
  color: #888;
  font-size: 15px;
  margin-top: 2px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.time {
  margin-left: 8px;
  font-size: 13px;
}
</style> 