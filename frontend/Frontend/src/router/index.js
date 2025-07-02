import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  // { path: '/login', name: 'Login', component: () => import('../views/Login.vue') }, // 已删除
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  { path: '/profile', name: 'UserProfile', component: () => import('../views/UserProfile.vue') },
  // { path: '/new', name: 'NewPost', component: () => import('../views/NewPost.vue') }, // 已废弃，已删除
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  // 这里不能直接useUserStore()，需用window全局token判断
  const token = localStorage.getItem('token')
  if (to.path === '/profile' && !token) {
    window.dispatchEvent(new CustomEvent('show-login-tip'))
    next(false)
  } else {
    next()
  }
})

export default router 