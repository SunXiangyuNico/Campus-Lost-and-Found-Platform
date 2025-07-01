<template>
  <div class="home">
    <Navbar />
    
    <div class="main-content">
      <!-- 顶部工具栏 -->
      <div class="toolbar">
        <div class="search-section">
          <el-input
            v-model="searchQuery"
            placeholder="按物品名称、地点等模糊搜索"
            clearable
            @input="handleSearch"
            @clear="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="publish-section">
          <el-button 
            type="primary" 
            size="large"
            @click="showPublishDialog = true"
            :disabled="!userStore.isLoggedIn"
          >
            <el-icon><Plus /></el-icon>
            发布失物/招领
          </el-button>
        </div>
      </div>

      <!-- 主要内容区域 -->
      <div class="content-area">
        <!-- 左侧帖子列表 -->
        <div class="posts-list">
          <div class="list-header">
            <h3>帖子列表</h3>
            <el-button 
              type="text" 
              @click="refreshPosts"
              :loading="loading"
            >
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
          
          <div class="list-content">
            <div v-if="loading" class="loading-container">
              <el-skeleton :rows="5" animated />
            </div>
            
            <div v-else-if="posts.length === 0" class="empty-container">
              <el-empty description="暂无帖子" />
            </div>
            
            <template v-else>
              <PostCard
                v-for="post in posts"
                :key="post.id"
                :post="post"
                :is-active="currentPost?.id === post.id"
                @select="selectPost"
              />
            </template>
          </div>
        </div>

        <!-- 右侧详情区域 -->
        <div class="post-detail-area">
          <PostDetail :post="currentPost" />
        </div>
      </div>
    </div>

    <!-- 发帖对话框 -->
    <PublishDialog
      v-model="showPublishDialog"
      @success="handlePublishSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { usePostsStore } from '../stores/posts'
import { postsService } from '../api/posts'
import { ElMessage } from 'element-plus'
import Navbar from '../components/Navbar.vue'
import PostCard from '../components/PostCard.vue'
import PostDetail from '../components/PostDetail.vue'
import PublishDialog from '../components/PublishDialog.vue'

const userStore = useUserStore()
const postsStore = usePostsStore()

const searchQuery = ref('')
const loading = ref(false)
const showPublishDialog = ref(false)

// 从store获取数据
const posts = computed(() => postsStore.posts)
const currentPost = computed(() => postsStore.currentPost)

// 搜索处理
const handleSearch = () => {
  fetchPosts()
}

// 获取帖子列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const data = await postsService.getPosts(searchQuery.value)
    postsStore.setPosts(data)
    
    // 如果有帖子且没有选中帖子，默认选中第一个
    if (data.length > 0 && !currentPost.value) {
      selectPost(data[0])
    }
  } catch (error) {
    console.error('获取帖子列表失败:', error)
    ElMessage.error('获取帖子列表失败')
  } finally {
    loading.value = false
  }
}

// 选择帖子
const selectPost = async (post) => {
  try {
    const detail = await postsService.getPostById(post.id)
    postsStore.setCurrentPost(detail)
  } catch (error) {
    console.error('获取帖子详情失败:', error)
    ElMessage.error('获取帖子详情失败')
  }
}

// 刷新帖子
const refreshPosts = () => {
  fetchPosts()
}

// 发布成功处理
const handlePublishSuccess = (post) => {
  // 发布成功后，帖子已经添加到store中，无需额外处理
  ElMessage.success('发布成功！')
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 20px 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.search-section {
  flex: 1;
  max-width: 400px;
}

.publish-section {
  flex-shrink: 0;
}

.content-area {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 20px;
  min-height: calc(100vh - 200px);
}

.posts-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.list-header h3 {
  margin: 0;
  color: #303133;
}

.list-content {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
}

.loading-container,
.empty-container {
  padding: 40px 20px;
}

.post-detail-area {
  min-height: 600px;
}

@media (max-width: 768px) {
  .content-area {
    grid-template-columns: 1fr;
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-section {
    max-width: none;
  }
}
</style> 