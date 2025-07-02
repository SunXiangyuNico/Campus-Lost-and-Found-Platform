<template>
  <div class="profile-layout">
    <div class="profile-navbar">
      <el-button type="primary" icon="el-icon-arrow-left" @click="goHome" round>返回主页</el-button>
      <span class="profile-title">个人中心</span>
    </div>
    <div class="profile-header">
      <UserCard :user="userInfo" />
    </div>
    <el-card class="profile-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="我的发布" name="published">
          <PostList :posts="myPublishedPosts" :selectedId="selectedPublishedId" @select="selectPublished" />
          <div v-if="selectedPublishedPost" class="detail-panel">
            <PostDetail :post="selectedPublishedPost" :map-img="mapImg" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="我的认领" name="claimed">
          <PostList :posts="myClaimedPosts" :selectedId="selectedClaimedId" @select="selectClaimed" />
          <div v-if="selectedClaimedPost" class="detail-panel">
            <PostDetail :post="selectedClaimedPost" :map-img="mapImg" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import UserCard from '../components/UserCard.vue'
import PostList from '../components/PostList.vue'
import PostDetail from '../components/PostDetail.vue'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo || {
  avatar: '',
  nickname: '未登录',
  studentId: '',
  contact: '',
  college: ''
})
const mapImg = '/map.png'

// 模拟数据
const myPublishedPosts = ref([
  {
    id: 1,
    type: 'lost',
    title: '丢失黑色钱包',
    location: '图书馆二楼自习室',
    time: '2024/1/15',
    nickname: 'Ankar',
    avatar: '',
    desc: '在图书馆二楼自习室丢了一个黑色钱包，内有身份证、学生证和少量现金。如有拾到请联系我，必有重谢！',
    images: [],
    claimed: false,
    comments: [],
    locationText: '图书馆二楼自习室',
    locationCoord: [200, 120]
  }
])
const myClaimedPosts = ref([
  // 示例：暂时为空
])

const activeTab = ref('published')
const selectedPublishedId = ref(myPublishedPosts.value[0]?.id || null)
const selectedClaimedId = ref(myClaimedPosts.value[0]?.id || null)
const selectedPublishedPost = computed(() => myPublishedPosts.value.find(p => p.id === selectedPublishedId.value))
const selectedClaimedPost = computed(() => myClaimedPosts.value.find(p => p.id === selectedClaimedId.value))

function selectPublished(id) {
  selectedPublishedId.value = id
}
function selectClaimed(id) {
  selectedClaimedId.value = id
}

const router = useRouter()
function goHome() {
  router.push('/')
}
</script>

<style scoped>
.profile-navbar {
  width: 650px;
  max-width: 95vw;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}
.profile-title {
  font-size: 22px;
  color: #ff9800;
  font-weight: bold;
}
.profile-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f5f6fa;
  min-height: calc(100vh - 56px);
  padding: 32px 0 0 0;
}
.profile-header {
  width: 650px;
  max-width: 95vw;
  margin-bottom: 18px;
}
.profile-card {
  width: 650px;
  max-width: 95vw;
  border-radius: 16px !important;
  box-shadow: 0 4px 24px #ffe0b2 !important;
  background: #fff8e1 !important;
  padding: 24px 32px 32px 32px;
}
.detail-panel {
  margin-top: 24px;
}
@media (max-width: 900px) {
  .profile-header, .profile-card, .profile-navbar {
    width: 100%;
    min-width: 0;
    padding: 8px;
  }
}
</style> 