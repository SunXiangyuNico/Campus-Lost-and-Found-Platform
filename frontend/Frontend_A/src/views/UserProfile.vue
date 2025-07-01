<template>
  <div class="container">
    <div class="profile-container">
      <!-- 用户信息卡片 -->
      <div class="card user-info-card">
        <div class="user-header">
          <el-avatar :size="80" :src="userStore.userInfo?.avatar">
            {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <div class="user-details">
            <h3>{{ userStore.userInfo?.username }}</h3>
            <p class="user-email">{{ userStore.userInfo?.email }}</p>
            <p class="user-phone">{{ userStore.userInfo?.phone }}</p>
          </div>
          <el-button type="primary" @click="showEditDialog = true">
            <el-icon><Edit /></el-icon>
            编辑信息
          </el-button>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="stats-container">
        <div class="stat-card">
          <div class="stat-number">{{ userStats.totalPosts }}</div>
          <div class="stat-label">发布总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ userStats.lostItems }}</div>
          <div class="stat-label">失物信息</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ userStats.foundItems }}</div>
          <div class="stat-label">拾物信息</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ userStats.resolvedItems }}</div>
          <div class="stat-label">已解决</div>
        </div>
      </div>

      <!-- 我的发布 -->
      <div class="card">
        <div class="section-header">
          <h3>我的发布</h3>
          <el-button type="primary" @click="$router.push('/new-post')">
            <el-icon><Plus /></el-icon>
            发布新信息
          </el-button>
        </div>

        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="全部" name="all">
            <div v-if="userItems.length === 0" class="empty-state">
              <el-icon size="48" color="#c0c4cc"><Document /></el-icon>
              <p>暂无发布的信息</p>
              <el-button type="primary" @click="$router.push('/new-post')">
                立即发布
              </el-button>
            </div>
            <div v-else class="items-grid">
              <div
                v-for="item in userItems"
                :key="item._id"
                class="item-card"
                @click="viewItemDetail(item._id)"
              >
                <div class="item-image">
                  <img :src="item.imageUrl || '/placeholder.jpg'" :alt="item.title" />
                  <div class="item-status" :class="item.status">
                    {{ item.status === 'lost' ? '失物' : '拾物' }}
                  </div>
                </div>
                <div class="item-content">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.description }}</p>
                  <div class="item-meta">
                    <span>{{ formatDate(item.createdAt) }}</span>
                    <el-tag :type="item.isResolved ? 'success' : 'warning'" size="small">
                      {{ item.isResolved ? '已解决' : '未解决' }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="失物" name="lost">
            <div v-if="lostItems.length === 0" class="empty-state">
              <p>暂无失物信息</p>
            </div>
            <div v-else class="items-grid">
              <div
                v-for="item in lostItems"
                :key="item._id"
                class="item-card"
                @click="viewItemDetail(item._id)"
              >
                <div class="item-image">
                  <img :src="item.imageUrl || '/placeholder.jpg'" :alt="item.title" />
                  <div class="item-status lost">失物</div>
                </div>
                <div class="item-content">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.description }}</p>
                  <div class="item-meta">
                    <span>{{ formatDate(item.createdAt) }}</span>
                    <el-tag :type="item.isResolved ? 'success' : 'warning'" size="small">
                      {{ item.isResolved ? '已解决' : '未解决' }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="拾物" name="found">
            <div v-if="foundItems.length === 0" class="empty-state">
              <p>暂无拾物信息</p>
            </div>
            <div v-else class="items-grid">
              <div
                v-for="item in foundItems"
                :key="item._id"
                class="item-card"
                @click="viewItemDetail(item._id)"
              >
                <div class="item-image">
                  <img :src="item.imageUrl || '/placeholder.jpg'" :alt="item.title" />
                  <div class="item-status found">拾物</div>
                </div>
                <div class="item-content">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.description }}</p>
                  <div class="item-meta">
                    <span>{{ formatDate(item.createdAt) }}</span>
                    <el-tag :type="item.isResolved ? 'success' : 'warning'" size="small">
                      {{ item.isResolved ? '已解决' : '未解决' }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 编辑用户信息对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑个人信息"
      width="500px"
      @close="resetEditForm"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editForm.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="userStore.isLoading" @click="handleUpdateProfile">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user.js'
import { getUserItems } from '@/api/items.js'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserProfile',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const showEditDialog = ref(false)
    const activeTab = ref('all')
    const userItems = ref([])
    const editFormRef = ref()

    const editForm = reactive({
      username: '',
      email: '',
      phone: ''
    })

    const editRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
      ]
    }

    // 计算属性
    const lostItems = computed(() => 
      userItems.value.filter(item => item.status === 'lost')
    )
    
    const foundItems = computed(() => 
      userItems.value.filter(item => item.status === 'found')
    )

    const userStats = computed(() => ({
      totalPosts: userItems.value.length,
      lostItems: lostItems.value.length,
      foundItems: foundItems.value.length,
      resolvedItems: userItems.value.filter(item => item.isResolved).length
    }))

    // 方法
    const fetchUserItems = async () => {
      try {
        const response = await getUserItems(userStore.userInfo._id)
        userItems.value = response.data || []
      } catch (error) {
        console.error('获取用户物品失败:', error)
        ElMessage.error('获取用户物品失败')
      }
    }

    const handleTabClick = () => {
      // 标签页切换逻辑
    }

    const viewItemDetail = (itemId) => {
      router.push(`/item/${itemId}`)
    }

    const resetEditForm = () => {
      editForm.username = userStore.userInfo?.username || ''
      editForm.email = userStore.userInfo?.email || ''
      editForm.phone = userStore.userInfo?.phone || ''
    }

    const handleUpdateProfile = async () => {
      try {
        await editFormRef.value.validate()
        
        const result = await userStore.updateUserInfo(editForm)
        
        if (result.success) {
          ElMessage.success('个人信息更新成功')
          showEditDialog.value = false
        } else {
          ElMessage.error(result.error)
        }
      } catch (error) {
        console.error('更新个人信息失败:', error)
        ElMessage.error('更新个人信息失败')
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    // 生命周期
    onMounted(() => {
      fetchUserItems()
      resetEditForm()
    })

    return {
      userStore,
      showEditDialog,
      activeTab,
      userItems,
      editForm,
      editFormRef,
      editRules,
      lostItems,
      foundItems,
      userStats,
      handleTabClick,
      viewItemDetail,
      resetEditForm,
      handleUpdateProfile,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

.user-info-card {
  margin-bottom: 20px;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-details h3 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 20px;
}

.user-email,
.user-phone {
  margin: 4px 0;
  color: #606266;
  font-size: 14px;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #303133;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
}

.empty-state p {
  margin: 16px 0;
  font-size: 16px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

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

.item-content h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 16px;
}

.item-content p {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .user-header {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
}
</style> 