<template>
  <div class="post-detail" v-if="post">
    <!-- 帖子头部信息 -->
    <div class="post-header">
      <div class="author-info">
        <el-avatar :src="post.author.avatar" :size="50" />
        <div class="author-details">
          <div class="author-name">{{ post.author.nickname }}</div>
          <div class="post-time">{{ formatTime(post.createdAt) }}</div>
        </div>
      </div>
      <el-tag 
        :type="post.type === 'lost' ? 'danger' : 'success'"
        size="large"
      >
        {{ post.type === 'lost' ? '失物' : '招领' }}
      </el-tag>
    </div>

    <!-- 帖子标题 -->
    <h2 class="post-title">{{ post.title }}</h2>

    <!-- 帖子描述 -->
    <div class="post-description">
      {{ post.description }}
    </div>

    <!-- 图片轮播 -->
    <div class="post-images" v-if="post.images && post.images.length > 0">
      <el-carousel height="300px">
        <el-carousel-item v-for="(image, index) in post.images" :key="index">
          <img :src="image" :alt="`图片${index + 1}`" class="carousel-image" />
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 地图 -->
    <div class="post-map">
      <div class="map-container">
        <div class="map-placeholder">
          <el-icon size="48"><Location /></el-icon>
          <p>地图位置：{{ post.location }}</p>
          <p>坐标：{{ post.latitude }}, {{ post.longitude }}</p>
        </div>
      </div>
    </div>

    <!-- 评论区 -->
    <div class="comments-section">
      <h3>评论区</h3>
      
      <!-- 评论列表 -->
      <div class="comments-list">
        <div 
          v-for="comment in post.comments" 
          :key="comment.id" 
          class="comment-item"
        >
          <div class="comment-header">
            <el-avatar :src="comment.author.avatar" :size="32" />
            <div class="comment-info">
              <div class="comment-author">{{ comment.author.nickname }}</div>
              <div class="comment-time">{{ formatTime(comment.createdAt) }}</div>
            </div>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>

      <!-- 评论输入框 -->
      <div class="comment-input" v-if="userStore.isLoggedIn">
        <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
          @keyup.enter.ctrl="addComment"
        />
        <el-button 
          type="primary" 
          @click="addComment"
          :loading="commentLoading"
        >
          发表评论
        </el-button>
      </div>
    </div>

    <!-- 认领按钮 -->
    <div class="claim-section" v-if="userStore.isLoggedIn && post.author.id !== userStore.user.id">
      <el-button 
        type="primary" 
        size="large"
        :disabled="post.status === 'claimed'"
        @click="claimPost"
        :loading="claimLoading"
      >
        {{ post.status === 'claimed' ? '已认领' : (post.type === 'lost' ? '认领' : '联系失主') }}
      </el-button>
    </div>
  </div>

  <div v-else class="no-post">
    <el-empty description="请选择一个帖子查看详情" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Location } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { usePostsStore } from '../stores/posts'
import { postsService } from '../api/posts'
import { ElMessage } from 'element-plus'

const props = defineProps({
  post: {
    type: Object,
    default: null
  }
})

const userStore = useUserStore()
const postsStore = usePostsStore()

const newComment = ref('')
const commentLoading = ref(false)
const claimLoading = ref(false)

const formatTime = (time) => {
  const date = new Date(time)
  return date.toLocaleString()
}

const addComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  commentLoading.value = true
  try {
    const newCommentData = await postsService.addComment(props.post.id, newComment.value)
    
    // 直接更新当前帖子的评论列表
    if (props.post.comments) {
      props.post.comments.push(newCommentData)
    } else {
      props.post.comments = [newCommentData]
    }
    
    newComment.value = ''
    ElMessage.success('评论发表成功')
  } catch (error) {
    ElMessage.error('评论发表失败')
  } finally {
    commentLoading.value = false
  }
}

const claimPost = async () => {
  claimLoading.value = true
  try {
    await postsService.claimPost(props.post.id)
    postsStore.updatePostStatus(props.post.id, 'claimed')
    postsStore.addClaimedPost(props.post)
    ElMessage.success('认领成功')
  } catch (error) {
    ElMessage.error('认领失败')
  } finally {
    claimLoading.value = false
  }
}
</script>

<style scoped>
.post-detail {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.post-time {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.post-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.post-description {
  font-size: 16px;
  line-height: 1.6;
  color: #606266;
  margin-bottom: 20px;
}

.post-images {
  margin-bottom: 20px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-map {
  margin-bottom: 20px;
}

.map-container {
  height: 200px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.map-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #909399;
}

.map-placeholder p {
  margin: 4px 0;
}

.comments-section {
  margin-bottom: 20px;
}

.comments-section h3 {
  margin-bottom: 16px;
  color: #303133;
}

.comments-list {
  margin-bottom: 20px;
}

.comment-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-content {
  font-size: 14px;
  line-height: 1.5;
  color: #606266;
  margin-left: 40px;
}

.comment-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.claim-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.no-post {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}
</style> 