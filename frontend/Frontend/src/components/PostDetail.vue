<template>
  <el-card class="post-detail">
    <div class="post-header">
      <el-avatar :src="post.avatar" size="large" />
      <div class="post-user-info">
        <div class="nickname">{{ post.nickname }}</div>
        <div class="time">{{ post.time }}</div>
      </div>
    </div>
    <h2 class="post-title">{{ post.title }}</h2>
    <div class="post-desc">{{ post.desc }}</div>
    <el-carousel v-if="post.images && post.images.length" height="200px" class="carousel">
      <el-carousel-item v-for="(img, idx) in post.images" :key="idx">
        <img :src="img" class="post-img" />
      </el-carousel-item>
    </el-carousel>
    <div class="map-section">
      <el-divider>丢失/拾取地点</el-divider>
      <div class="map-container">
        <img :src="mapImg" class="map-img" />
        <div v-if="post.locationCoord" class="map-marker" :style="markerStyle"></div>
      </div>
      <div class="location-text">{{ post.locationText }}</div>
    </div>
    <div class="comment-section">
      <el-divider>评论区</el-divider>
      <div v-if="post.comments && post.comments.length">
        <div v-for="(c, i) in post.comments" :key="i" class="comment-item">
          <el-avatar :src="c.avatar" size="small" />
          <span class="comment-nickname">{{ c.nickname }}</span>
          <span class="comment-time">{{ c.time }}</span>
          <span class="comment-content">{{ c.content }}</span>
        </div>
      </div>
      <el-empty v-else description="暂无评论" />
      <div class="comment-input">
        <el-input v-model="commentText" placeholder="写下你的评论..." clearable />
        <el-button type="primary" @click="onSendComment" :disabled="!commentText">发送</el-button>
      </div>
    </div>
    <div class="post-actions">
      <el-button type="primary" :disabled="post.claimed" @click="onClaim">
        {{ post.claimed ? '已认领' : (post.type === 'lost' ? '认领' : '联系失主') }}
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  mapImg: {
    type: String,
    required: false
  }
})
const emit = defineEmits(['claim', 'comment'])
const commentText = ref('')

function onClaim() {
  emit('claim', props.post)
}
function onSendComment() {
  if (!commentText.value) return
  emit('comment', commentText.value)
  ElMessage.success('评论已发送')
  commentText.value = ''
}
// 当帖子切换时清空评论输入框
watch(() => props.post.id, () => { commentText.value = '' })

const markerStyle = computed(() => {
  if (!props.post.locationCoord) return {}
  // 假设地图图片宽高为 500x300，locationCoord 为 [x, y] 像素坐标
  const [x, y] = props.post.locationCoord
  return {
    left: x + 'px',
    top: y + 'px'
  }
})
</script>

<style scoped>
.post-detail {
  max-width: 650px;
  min-height: 600px;
  margin: 0 auto;
  padding: 32px 36px 24px 36px;
  border-radius: 12px;
  box-shadow: 0 4px 24px #e6e8f0;
}
.post-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}
.post-user-info .nickname {
  font-weight: bold;
}
.post-user-info .time {
  color: #999;
  font-size: 12px;
}
.post-title {
  margin: 12px 0 8px 0;
  font-size: 22px;
  font-weight: 600;
}
.post-desc {
  margin-bottom: 16px;
  color: #333;
}
.carousel {
  margin-bottom: 16px;
}
.post-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 6px;
}
.map-section {
  margin: 18px 0 12px 0;
}
.map-container {
  position: relative;
  width: 500px;
  height: 300px;
  margin: 0 auto 8px auto;
  background: #f0f2f5;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px #f0f1f2;
}
.map-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.map-marker {
  position: absolute;
  width: 22px;
  height: 22px;
  background: #ff4d4f;
  border: 2.5px solid #fff;
  border-radius: 50%;
  left: 0;
  top: 0;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 8px #ff4d4f44;
  z-index: 2;
}
.location-text {
  color: #666;
  font-size: 15px;
  margin-bottom: 8px;
  text-align: center;
}
.comment-section {
  margin: 18px 0 12px 0;
}
.comment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
}
.comment-nickname {
  font-weight: 500;
  margin-right: 6px;
}
.comment-time {
  color: #aaa;
  font-size: 12px;
  margin-right: 8px;
}
.comment-content {
  color: #333;
}
.comment-input {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
.post-actions {
  margin-top: 24px;
  text-align: right;
}
</style> 