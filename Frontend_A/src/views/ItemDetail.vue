<template>
  <div class="container">
    <div class="detail-container">
      <div v-if="loading" class="loading">
        <el-skeleton :rows="10" animated />
      </div>
      
      <div v-else-if="item" class="item-detail">
        <div class="item-header">
          <el-button @click="$router.go(-1)" icon="ArrowLeft">
            返回
          </el-button>
          <div class="item-status" :class="item.status">
            {{ item.status === 'lost' ? '失物' : '拾物' }}
          </div>
        </div>
        
        <div class="item-content">
          <div class="item-image">
            <img :src="item.imageUrl || '/placeholder.jpg'" :alt="item.title" />
          </div>
          
          <div class="item-info">
            <h1>{{ item.title }}</h1>
            <p class="description">{{ item.description }}</p>
            
            <div class="info-grid">
              <div class="info-item">
                <span class="label">地点：</span>
                <span>{{ item.location }}</span>
              </div>
              <div class="info-item">
                <span class="label">时间：</span>
                <span>{{ formatDate(item.date) }}</span>
              </div>
              <div class="info-item">
                <span class="label">联系方式：</span>
                <span>{{ item.contact }}</span>
              </div>
              <div class="info-item">
                <span class="label">发布者：</span>
                <span>{{ item.user?.username }}</span>
              </div>
              <div class="info-item">
                <span class="label">发布时间：</span>
                <span>{{ formatDate(item.createdAt) }}</span>
              </div>
            </div>
            
            <div class="actions">
              <el-button type="primary" @click="contactUser">
                <el-icon><Message /></el-icon>
                联系发布者
              </el-button>
              <el-button v-if="canMarkAsFound" type="success" @click="markAsFound">
                <el-icon><Check /></el-icon>
                标记为已找回
              </el-button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="not-found">
        <el-icon size="64" color="#c0c4cc"><Warning /></el-icon>
        <h2>物品不存在</h2>
        <p>该物品可能已被删除或不存在</p>
        <el-button type="primary" @click="$router.push('/')">
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user.js'
import { getItemById, markAsFound } from '@/api/items.js'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ItemDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const item = ref(null)
    const loading = ref(true)

    const canMarkAsFound = computed(() => {
      return userStore.isLoggedIn && 
             item.value && 
             item.value.user?._id === userStore.userInfo?._id &&
             !item.value.isResolved
    })

    const fetchItemDetail = async () => {
      try {
        loading.value = true
        const response = await getItemById(route.params.id)
        item.value = response.data
      } catch (error) {
        console.error('获取物品详情失败:', error)
        ElMessage.error('获取物品详情失败')
      } finally {
        loading.value = false
      }
    }

    const contactUser = () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      
      ElMessage.info('联系功能开发中...')
    }

    const markAsFound = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要将此物品标记为已找回吗？',
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await markAsFound(item.value._id)
        if (response.success) {
          ElMessage.success('标记成功')
          item.value.isResolved = true
        } else {
          ElMessage.error(response.error || '标记失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('标记失败:', error)
          ElMessage.error('标记失败')
        }
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchItemDetail()
    })

    return {
      item,
      loading,
      canMarkAsFound,
      contactUser,
      markAsFound,
      formatDate
    }
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.loading {
  padding: 40px;
}

.item-detail {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.item-status {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  padding: 40px;
}

.item-image {
  text-align: center;
}

.item-image img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.item-info h1 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 24px;
}

.description {
  margin: 0 0 24px 0;
  color: #606266;
  line-height: 1.6;
  font-size: 16px;
}

.info-grid {
  margin-bottom: 32px;
}

.info-item {
  display: flex;
  margin-bottom: 12px;
  font-size: 14px;
}

.info-item .label {
  color: #909399;
  min-width: 80px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 12px;
}

.not-found {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.not-found h2 {
  margin: 16px 0;
  color: #606266;
}

.not-found p {
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .item-content {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 20px;
  }
  
  .actions {
    flex-direction: column;
  }
}
</style> 