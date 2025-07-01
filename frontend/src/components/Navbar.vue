<template>
  <el-header class="navbar">
    <div class="navbar-container">
      <div class="logo">
        <h2>校园失物招领平台</h2>
      </div>
      
      <div class="nav-links">
        <el-button 
          type="text" 
          @click="$router.push('/')"
          :class="{ active: $route.path === '/' }"
        >
          首页
        </el-button>
        
        <el-button 
          v-if="userStore.isLoggedIn"
          type="text" 
          @click="$router.push('/profile')"
          :class="{ active: $route.path === '/profile' }"
        >
          我的
        </el-button>
      </div>
      
      <div class="user-actions">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <el-avatar 
              :src="userStore.user?.avatar" 
              :size="40"
            />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        
        <template v-else>
          <el-button type="primary" @click="$router.push('/login')">
            登录
          </el-button>
          <el-button @click="$router.push('/register')">
            注册
          </el-button>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/')
  }
}
</script>

<style scoped>
.navbar {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo h2 {
  color: #409eff;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links .el-button {
  font-size: 16px;
  color: #606266;
}

.nav-links .el-button.active {
  color: #409eff;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style> 