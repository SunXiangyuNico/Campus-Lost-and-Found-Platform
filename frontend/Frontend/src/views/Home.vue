<template>
  <div class="home-layout">
    <Navbar 
      @publish="showPostDialog = true" 
      @login="showLoginDialog = true"
      @register="showRegisterDialog = true"
    />
    <div class="main-content">
      <div class="left-panel">
        <div class="filter-section">
          <div class="filter-tabs">
            <button 
              v-for="tab in filterTabs" 
              :key="tab.value"
              :class="['filter-tab', { active: typeFilter === tab.value }]"
              @click="typeFilter = tab.value"
            >
              <span class="tab-icon">
                <svg v-if="tab.value === 'all'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 3H21V21H3V3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M3 9H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 21V9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else-if="tab.value === 'lost'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.7088 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.76488 14.1003 1.98232 16.07 2.85999" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              {{ tab.label }}
            </button>
          </div>
          
          <div class="date-filter">
            <el-date-picker 
              v-model="dateFilter" 
              type="date" 
              placeholder="选择日期" 
              class="date-picker"
              size="small"
            />
          </div>
        </div>
        
        <PostList :posts="filteredPosts" :selectedId="selectedPostId" @select="selectPost" />
      </div>
      
      <div class="right-panel">
        <div class="detail-container">
          <PostDetail v-if="selectedPost" :post="selectedPost" :map-img="mapImg" :is-login="isLogin" @require-login="showLoginDialog = true" />
          <div v-else class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>请选择一条帖子</h3>
            <p>从左侧列表中选择一条帖子查看详细信息</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 发布对话框 -->
    <el-dialog 
      v-model="showPostDialog" 
      title="发布新信息" 
      width="650px" 
      :close-on-click-modal="false"
      class="post-dialog"
    >
      <NewPostForm @success="handlePostSuccess" />
    </el-dialog>
    
    <!-- 登录对话框 -->
    <Login 
      v-model:visible="showLoginDialog"
      @switch-register="switchToRegister"
    />
    
    <!-- 注册对话框 -->
    <Register 
      v-model:visible="showRegisterDialog"
      @switch-login="switchToLogin"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import PostList from '../components/PostList.vue'
import PostDetail from '../components/PostDetail.vue'
import NewPostForm from '../components/NewPostForm.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import { useUserStore } from '../store/user'
import { getMyPosts } from '../api/items'

const mapImg = '/map.png'

const posts = ref([])

async function fetchPosts() {
  const resp = await getMyPosts()
  posts.value = resp.data
}

onMounted(fetchPosts)

function handlePostSuccess() {
  showPostDialog.value = false
  fetchPosts()
}

const search = ref('')
const typeFilter = ref('all')
const dateFilter = ref(null)
const selectedPostId = ref(posts.value[0]?.id || null)

const filterTabs = [
  { label: '全部', value: 'all' },
  { label: '失物', value: 'lost' },
  { label: '招领', value: 'found' }
]

const selectedPost = computed(() => posts.value.find(p => p.id === selectedPostId.value))

const filteredPosts = computed(() => {
  return posts.value.filter(p => {
    const matchType = typeFilter.value === 'all' || p.type === typeFilter.value
    const matchSearch = !search.value || p.title.includes(search.value) || p.location.includes(search.value)
    const matchDate = !dateFilter.value || p.time === dateFilter.value?.toLocaleDateString('zh-CN')
    return matchType && matchSearch && matchDate
  })
})

function selectPost(id) {
  selectedPostId.value = id
}

function switchToRegister() {
  showLoginDialog.value = false
  showRegisterDialog.value = true
}

function switchToLogin() {
  showRegisterDialog.value = false
  showLoginDialog.value = true
}

const showPostDialog = ref(false)
const showLoginDialog = ref(false)
const showRegisterDialog = ref(false)

const userStore = useUserStore()
const isLogin = computed(() => !!userStore.token)
</script>

<style scoped>
.home-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-gray);
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-panel {
  width: 380px;
  min-width: 320px;
  background: var(--bg-white);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-light);
}

.filter-section {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-white);
}

.filter-tabs {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.filter-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  background: var(--bg-white);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  border-color: var(--brand-blue-light);
  color: var(--brand-blue);
}

.filter-tab.active {
  background: var(--brand-blue);
  border-color: var(--brand-blue);
  color: white;
}

.tab-icon {
  display: flex;
  align-items: center;
}

.date-filter {
  display: flex;
  justify-content: center;
}

.date-picker {
  width: 100%;
}

.right-panel {
  flex: 1;
  padding: var(--spacing-xl);
  overflow-y: auto;
  background: var(--bg-gray);
}

.detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  margin-bottom: var(--spacing-lg);
  color: var(--text-light);
}

.empty-state h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-secondary);
}

.empty-state p {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

/* 对话框样式优化 */
:deep(.el-dialog) {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-heavy);
}

:deep(.el-dialog__header) {
  padding: var(--spacing-lg) var(--spacing-xl) var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

:deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: var(--spacing-xl);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .left-panel {
    width: 340px;
    min-width: 280px;
  }
  
  .right-panel {
    padding: var(--spacing-lg);
  }
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100%;
    min-width: 0;
    border-right: none;
    border-bottom: 1px solid var(--border-light);
  }
  
  .filter-section {
    padding: var(--spacing-md);
  }
  
  .right-panel {
    padding: var(--spacing-md);
  }
  
  .detail-container {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .filter-tabs {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .filter-tab {
    justify-content: flex-start;
  }
 }
</style>