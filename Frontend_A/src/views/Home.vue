<template>
  <div class="container">
    <div class="home-header">
      <h1>失物招领平台</h1>
      <p>帮助您快速找到丢失的物品或归还拾到的物品</p>
    </div>
    
    <div class="search-section">
      <SearchBar />
    </div>
    
    <div class="content-section">
      <div class="section-header">
        <h2>最新信息</h2>
        <el-button v-if="userStore.isLoggedIn" type="primary" @click="$router.push('/new-post')">
          <el-icon><Plus /></el-icon>
          发布信息
        </el-button>
      </div>
      
      <div class="items-container">
        <div v-if="items.length === 0" class="empty-state">
          <el-icon size="48" color="#c0c4cc"><Document /></el-icon>
          <p>暂无信息</p>
        </div>
        <div v-else class="items-grid">
          <ItemCard
            v-for="item in items"
            :key="item._id"
            :item="item"
            @click="viewItemDetail(item._id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user.js'
import SearchBar from '@/components/SearchBar.vue'
import ItemCard from '@/components/ItemCard.vue'
import { getItems } from '@/api/items.js'

export default {
  name: 'Home',
  components: {
    SearchBar,
    ItemCard
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const items = ref([])

    const fetchItems = async () => {
      try {
        const response = await getItems()
        items.value = response.data || []
      } catch (error) {
        console.error('获取物品列表失败:', error)
      }
    }

    const viewItemDetail = (itemId) => {
      router.push(`/item/${itemId}`)
    }

    onMounted(() => {
      fetchItems()
    })

    return {
      items,
      userStore,
      viewItemDetail
    }
  }
}
</script>

<style scoped>
.home-header {
  text-align: center;
  margin-bottom: 40px;
}

.home-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 12px;
}

.home-header p {
  font-size: 16px;
  color: #606266;
}

.search-section {
  margin-bottom: 40px;
}

.content-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
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

@media (max-width: 768px) {
  .home-header h1 {
    font-size: 24px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
}
</style> 