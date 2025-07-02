import { createRouter, createWebHistory } from 'vue-router'

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

export default router 