<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/" class="logo">
          <el-icon><Search /></el-icon>
          <span>失物招领平台</span>
        </router-link>
      </div>
      
      <div class="navbar-menu">
        <router-link to="/" class="nav-link">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </router-link>
        
        <router-link v-if="userStore.isLoggedIn" to="/new-post" class="nav-link">
          <el-icon><Plus /></el-icon>
          <span>发布信息</span>
        </router-link>
      </div>
      
      <div class="navbar-end">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <div class="user-menu">
              <el-avatar :size="32" :src="userStore.userInfo?.avatar">
                {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.userInfo?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        
        <template v-else>
          <router-link to="/login" class="nav-link">
            <el-icon><User /></el-icon>
            <span>登录</span>
          </router-link>
          <router-link to="/register" class="nav-link">
            <el-icon><UserFilled /></el-icon>
            <span>注册</span>
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { useUserStore } from '@/store/user.js'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'Navbar',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()

    const handleCommand = async (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'logout':
          await userStore.logout()
          ElMessage.success('已退出登录')
          router.push('/')
          break
      }
    }

    return {
      userStore,
      handleCommand
    }
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 60px;
  display: flex;
  align-items: center;
}

.navbar .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #409eff;
  font-size: 20px;
  font-weight: bold;
  gap: 8px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.navbar-end {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #606266;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s;
  gap: 6px;
}

.nav-link:hover {
  color: #409eff;
  background-color: #f0f9ff;
}

.nav-link.router-link-active {
  color: #409eff;
  background-color: #f0f9ff;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.user-menu:hover {
  background-color: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .navbar-menu {
    display: none;
  }
  
  .username {
    display: none;
  }
}
</style> 