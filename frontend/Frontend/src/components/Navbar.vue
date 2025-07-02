<template>
  <header class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <span class="brand">校园失物招领平台</span>
        </div>
        
        <div class="search-section">
          <div class="search-wrapper">
            <div class="search-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <input 
              type="text" 
              placeholder="搜索物品名称，如：蓝色水杯、图书馆..." 
              class="search-input"
              v-model="searchQuery"
              @input="onSearch"
            />
          </div>
        </div>
      </div>
      
      <div class="navbar-right">
        <nav class="nav-menu">
          <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            首页
          </router-link>
          <router-link to="/profile" class="nav-item" :class="{ active: $route.path.startsWith('/profile') }">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            个人中心
          </router-link>
        </nav>
        
        <div class="auth-section">
          <el-button 
            v-if="!isLogin" 
            type="text" 
            class="login-btn"
            @click="goLogin"
          >
            登录
          </el-button>
          <el-button 
            v-if="!isLogin" 
            type="text" 
            class="register-btn"
            @click="goRegister"
          >
            注册
          </el-button>
          <el-button 
            type="primary" 
            class="publish-btn"
            @click="goPublish"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            发布
          </el-button>
          
          <el-dropdown v-if="isLogin" class="user-dropdown">
            <div class="user-info">
              <el-avatar :src="userStore.userInfo?.avatar || ''" size="small" />
              <span class="username">{{ userStore.userInfo?.nickname || '用户' }}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polyline points="6,9 12,15 18,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <polyline points="16,17 21,12 16,7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '../store/user'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const isLogin = computed(() => !!userStore.token)
const searchQuery = ref('')

function onSearch() {
  // 触发搜索事件
  emit('search', searchQuery.value)
}

function goLogin() {
  emit('login')
}

function goRegister() {
  emit('register')
}

function goPublish() {
  emit('publish')
}

function logout() {
  userStore.logout()
  router.push('/')
}

const emit = defineEmits(['search', 'publish', 'login', 'register'])
</script>

<style scoped>
.navbar {
  background: var(--bg-white);
  box-shadow: var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--border-light);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  flex: 1;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  min-width: 200px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--brand-blue), var(--brand-blue-light));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand {
  font-weight: 600;
  font-size: var(--font-size-lg);
  color: var(--text-primary);
  white-space: nowrap;
}

.search-section {
  flex: 1;
  max-width: 500px;
}

.search-wrapper {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  z-index: 1;
}

.search-input {
  width: 100%;
  height: 40px;
  padding: 0 var(--spacing-md) 0 44px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  background: var(--bg-gray);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--brand-blue);
  background: var(--bg-white);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.nav-item.active {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.1);
}

.auth-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.login-btn {
  color: var(--text-secondary);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
}

.login-btn:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.register-btn {
  color: var(--text-secondary);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
}

.register-btn:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.publish-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-weight: 500;
  border-radius: var(--radius-lg);
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: background 0.2s ease;
}

.user-info:hover {
  background: var(--bg-gray);
}

.username {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .navbar-container {
    padding: 0 var(--spacing-lg);
  }
  
  .navbar-left {
    gap: var(--spacing-lg);
  }
  
  .search-section {
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 var(--spacing-md);
  }
  
  .navbar-left {
    gap: var(--spacing-md);
  }
  
  .logo-section {
    min-width: auto;
  }
  
  .brand {
    display: none;
  }
  
  .search-section {
    max-width: 200px;
  }
  
  .nav-menu {
    display: none;
  }
}

@media (max-width: 480px) {
  .search-section {
    display: none;
  }
  
  .auth-section {
    gap: var(--spacing-xs);
  }
  
  .publish-btn {
    padding: var(--spacing-sm);
  }
  
  .publish-btn span {
    display: none;
  }
}
</style> 