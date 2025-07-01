<template>
  <div class="profile-page">
    <Navbar />
    
    <div class="main-content">
      <div class="profile-container">
        <!-- 个人信息卡片 -->
        <div class="profile-card">
          <div class="profile-header">
            <el-avatar :src="userStore.user?.avatar" :size="80" />
            <div class="profile-info">
              <h2>{{ userStore.user?.nickname }}</h2>
              <p class="student-id">学号：{{ userStore.user?.studentId }}</p>
              <p v-if="userStore.user?.college" class="college">
                学院：{{ userStore.user?.college }}
              </p>
              <p v-if="userStore.user?.contact" class="contact">
                联系方式：{{ userStore.user?.contact }}
              </p>
            </div>
          </div>
        </div>

        <!-- Tab切换 -->
        <div class="tabs-container">
          <el-tabs v-model="activeTab" @tab-click="handleTabClick">
            <el-tab-pane label="历史认领" name="claimed">
              <div class="tab-content">
                <div v-if="claimedLoading" class="loading-container">
                  <el-skeleton :rows="3" animated />
                </div>
                
                <div v-else-if="claimedPosts.length === 0" class="empty-container">
                  <el-empty description="暂无历史认领记录" />
                </div>
                
                <div v-else class="posts-grid">
                  <div 
                    v-for="post in claimedPosts" 
                    :key="post.id"
                    class="post-item"
                    @click="viewPost(post)"
                  >
                    <div class="post-header">
                      <el-tag 
                        :type="post.type === 'lost' ? 'danger' : 'success'"
                        size="small"
                      >
                        {{ post.type === 'lost' ? '失物' : '招领' }}
                      </el-tag>
                      <span class="claim-time">{{ formatTime(post.claimedAt) }}</span>
                    </div>
                    <h4 class="post-title">{{ post.title }}</h4>
                    <p class="post-author">发布者：{{ post.author.nickname }}</p>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="我发布的" name="my">
              <div class="tab-content">
                <div v-if="myPostsLoading" class="loading-container">
                  <el-skeleton :rows="3" animated />
                </div>
                
                <div v-else-if="myPosts.length === 0" class="empty-container">
                  <el-empty description="暂无发布的帖子" />
                </div>
                
                <div v-else class="posts-grid">
                  <div 
                    v-for="post in myPosts" 
                    :key="post.id"
                    class="post-item"
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
                    <h4 class="post-title" @click="viewPost(post)">{{ post.title }}</h4>
                    <div class="post-actions">
                      <el-button 
                        type="text" 
                        size="small"
                        @click="editPost(post)"
                      >
                        编辑
                      </el-button>
                      <el-button 
                        type="text" 
                        size="small"
                        @click="closePost(post)"
                        :disabled="post.status === 'closed'"
                      >
                        {{ post.status === 'closed' ? '已关闭' : '关闭' }}
                      </el-button>
                      <el-button 
                        type="text" 
                        size="small"
                        @click="deletePost(post)"
                        style="color: #f56c6c"
                      >
                        删除
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </div>

    <!-- 帖子详情对话框 -->
    <el-dialog
      v-model="showPostDetail"
      title="帖子详情"
      width="800px"
      :before-close="closePostDetail"
    >
      <PostDetail v-if="selectedPost" :post="selectedPost" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { usePostsStore } from '../stores/posts'
import { postsService } from '../api/posts'
import { ElMessage, ElMessageBox } from 'element-plus'
import Navbar from '../components/Navbar.vue'
import PostDetail from '../components/PostDetail.vue'

const router = useRouter()
const userStore = useUserStore()
const postsStore = usePostsStore()

const activeTab = ref('claimed')
const claimedLoading = ref(false)
const myPostsLoading = ref(false)
const showPostDetail = ref(false)
const selectedPost = ref(null)

// 从store获取数据
const claimedPosts = computed(() => postsStore.claimedPosts)
const myPosts = computed(() => postsStore.myPosts)

const handleTabClick = (tab) => {
  if (tab.name === 'claimed') {
    fetchClaimedPosts()
  } else if (tab.name === 'my') {
    fetchMyPosts()
  }
}

const fetchClaimedPosts = async () => {
  claimedLoading.value = true
  try {
    const data = await postsService.getClaimedPosts()
    // 使用store的方法更新数据
    postsStore.claimedPosts.length = 0
    data.forEach(post => postsStore.claimedPosts.push(post))
  } catch (error) {
    console.error('获取历史认领失败:', error)
    ElMessage.error('获取历史认领失败')
  } finally {
    claimedLoading.value = false
  }
}

const fetchMyPosts = async () => {
  myPostsLoading.value = true
  try {
    const data = await postsService.getMyPosts()
    // 使用store的方法更新数据
    postsStore.myPosts.length = 0
    data.forEach(post => postsStore.myPosts.push(post))
  } catch (error) {
    console.error('获取我的帖子失败:', error)
    ElMessage.error('获取我的帖子失败')
  } finally {
    myPostsLoading.value = false
  }
}

const viewPost = async (post) => {
  try {
    const detail = await postsService.getPostById(post.id)
    selectedPost.value = detail
    showPostDetail.value = true
  } catch (error) {
    console.error('获取帖子详情失败:', error)
    ElMessage.error('获取帖子详情失败')
  }
}

const closePostDetail = () => {
  showPostDetail.value = false
  selectedPost.value = null
}

const editPost = (post) => {
  // 跳转到编辑页面或打开编辑对话框
  ElMessage.info('编辑功能开发中...')
}

const closePost = async (post) => {
  try {
    await ElMessageBox.confirm('确定要关闭这个帖子吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await postsService.updatePostStatus(post.id, 'closed')
    postsStore.updatePostStatus(post.id, 'closed')
    ElMessage.success('帖子已关闭')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('关闭帖子失败:', error)
      ElMessage.error('关闭帖子失败')
    }
  }
}

const deletePost = async (post) => {
  try {
    await ElMessageBox.confirm('确定要删除这个帖子吗？删除后无法恢复', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await postsService.deletePost(post.id)
    // 从列表中移除
    const index = postsStore.myPosts.findIndex(p => p.id === post.id)
    if (index > -1) {
      postsStore.myPosts.splice(index, 1)
    }
    ElMessage.success('帖子已删除')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除帖子失败:', error)
      ElMessage.error('删除帖子失败')
    }
  }
}

const formatTime = (time) => {
  const date = new Date(time)
  return date.toLocaleString()
}

onMounted(() => {
  fetchClaimedPosts()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 20px 20px;
}

.profile-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-info h2 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 24px;
}

.profile-info p {
  margin: 4px 0;
  color: #606266;
  font-size: 14px;
}

.student-id {
  font-weight: 500;
}

.tabs-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tab-content {
  padding: 20px;
}

.loading-container,
.empty-container {
  padding: 40px 20px;
  text-align: center;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.post-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.post-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.post-time,
.claim-time {
  font-size: 12px;
  color: #909399;
}

.post-title {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
  line-height: 1.4;
  cursor: pointer;
}

.post-title:hover {
  color: #409eff;
}

.post-author {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.post-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

@media (max-width: 768px) {
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
}
</style> 