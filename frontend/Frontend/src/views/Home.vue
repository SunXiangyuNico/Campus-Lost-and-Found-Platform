<template>
  <div class="home-layout">
    <Navbar @login="showLoginDialog = true" @register="showRegisterDialog = true" />
    <div class="main-topbar">
      <el-input v-model="search" placeholder="搜索物品名称、地点等" class="search-input" clearable style="width: 320px; margin-right: 16px;" />
      <el-select v-model="typeFilter" placeholder="全部类型" class="type-select" style="width: 120px; margin-right: 16px;">
        <el-option label="全部" value="all" />
        <el-option label="失物" value="lost" />
        <el-option label="招领" value="found" />
      </el-select>
      <el-date-picker v-model="dateFilter" type="date" placeholder="选择日期" class="date-picker" style="width: 150px;" />
      <div style="flex:1"></div>
      <el-button type="primary" @click="showPostDialog = true">发布</el-button>
    </div>
    <div class="main-content">
      <div class="left-panel">
        <PostList :posts="filteredPosts" :selectedId="selectedPostId" @select="selectPost" />
      </div>
      <div class="right-panel">
        <div class="detail-fixed">
          <PostDetail v-if="selectedPost" :post="selectedPost" :map-img="mapImg" />
          <el-empty v-else description="请选择一条帖子" />
        </div>
      </div>
    </div>
    <el-dialog v-model="showPostDialog" title="发布新信息" width="650px" :close-on-click-modal="false">
      <NewPostForm @success="showPostDialog = false" />
    </el-dialog>
    <el-dialog v-model="showLoginDialog" title="登录" width="400px" :close-on-click-modal="false">
      <LoginForm @success="showLoginDialog = false" />
    </el-dialog>
    <el-dialog v-model="showRegisterDialog" title="注册" width="500px" :close-on-click-modal="false">
      <RegisterForm @success="showRegisterDialog = false" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
// import Navbar from '../components/Navbar.vue'
import PostList from '../components/PostList.vue'
import PostDetail from '../components/PostDetail.vue'
import NewPostForm from '../components/NewPostForm.vue'
// import LoginForm from '../components/LoginForm.vue'
// import RegisterForm from '../components/RegisterForm.vue'
const mapImg = '/map.png'

const posts = ref([
  {
    id: 1,
    type: 'lost',
    title: '丢失黑色钱包',
    location: '图书馆二楼自习室',
    time: '2024/1/15',
    nickname: '小明',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=ming',
    desc: '在图书馆二楼自习室丢了一个黑色钱包，内有身份证、学生证和少量现金。如有拾到请联系我，必有重谢！',
    images: ['https://images.unsplash.com/photo-1465101046530-73398c7f28ca'],
    claimed: false,
    comments: [
      { nickname: '小红', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=hong', time: '2024/1/15 19:00:00', content: '我好像在图里见过，让我想想' }
    ],
    locationText: '图书馆二楼自习室',
    locationCoord: [200, 120] // 地图标点像素坐标
  },
  {
    id: 2,
    type: 'found',
    title: '捡到蓝色水杯',
    location: '松学楼A座一楼大厅',
    time: '2024/1/15',
    nickname: '小李',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=li',
    desc: '在松学楼A座一楼大厅捡到一个蓝色水杯，有需要的同学请联系我。',
    images: [],
    claimed: false,
    comments: [],
    locationText: '松学楼A座一楼大厅',
    locationCoord: [350, 180]
  },
  {
    id: 3,
    type: 'lost',
    title: '丢失苹果手机',
    location: '学生食堂一楼',
    time: '2024/1/15',
    nickname: '小王',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=wang',
    desc: '学生食堂一楼丢失一部苹果手机，壳是红色的。',
    images: [],
    claimed: false,
    comments: [],
    locationText: '学生食堂一楼',
    locationCoord: [100, 250]
  }
])
const search = ref('')
const typeFilter = ref('all')
const dateFilter = ref(null)
const selectedPostId = ref(posts.value[0]?.id || null)
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
const showPostDialog = ref(false)
const showLoginDialog = ref(false)
const showRegisterDialog = ref(false)
</script>

<style scoped>
.home-layout {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px);
  background: #f5f6fa;
  font-size: 18px;
}
.main-topbar {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 24px 40px 0 40px;
  background: #f5f6fa;
  gap: 0;
}
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.left-panel {
  width: 340px;
  min-width: 300px;
  background: #f8f9fb;
  padding: 24px 12px 12px 24px;
  border-right: 1.5px solid #e5e6eb;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.right-panel {
  flex: 1;
  padding: 32px 40px 0 40px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.detail-fixed {
  width: 650px;
  min-height: 600px;
  max-width: 100%;
  background: transparent;
}
@media (max-width: 900px) {
  .main-topbar {
    flex-direction: column;
    padding: 12px;
    gap: 8px;
  }
  .main-content {
    flex-direction: column;
  }
  .left-panel {
    width: 100%;
    min-width: 0;
    border-right: none;
    border-bottom: 1.5px solid #e5e6eb;
    padding: 12px;
  }
  .right-panel {
    padding: 12px;
  }
  .detail-fixed {
    width: 100%;
    min-width: 0;
  }
}
</style> 