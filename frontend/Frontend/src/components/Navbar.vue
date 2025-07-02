<template>
  <el-header class="navbar">
    <div class="navbar-left">
      <el-avatar src="/logo.png" size="small" class="logo" />
      <span class="brand">校园失物招领平台</span>
      <el-menu mode="horizontal" :default-active="activeMenu" class="nav-menu" @select="onMenuSelect">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/profile">个人中心</el-menu-item>
      </el-menu>
    </div>
    <div class="navbar-right">
      <el-button v-if="!isLogin" type="primary" @click="goLogin" size="small">登录</el-button>
      <el-dropdown v-else>
        <span class="el-dropdown-link">
          <el-avatar :src="userStore.userInfo?.avatar || ''" size="small" />
          {{ userStore.userInfo?.nickname || '用户' }}
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script setup>
import { useUserStore } from '../store/user'
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const isLogin = computed(() => !!userStore.token)
const activeMenu = computed(() => {
  if (route.path.startsWith('/profile')) return '/profile'
  if (route.path.startsWith('/new')) return '/new'
  return '/'
})
function onMenuSelect(index) {
  router.push(index)
}
function goLogin() {
  router.push('/login')
}
function logout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  height: 56px;
}
.navbar-left {
  display: flex;
  align-items: center;
}
.logo {
  margin-right: 10px;
}
.brand {
  font-weight: bold;
  font-size: 18px;
  margin-right: 24px;
  color: #409eff;
}
.nav-menu {
  border-bottom: none;
  background: transparent;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.el-dropdown-link {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
</style> 