import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user.js'

// 页面组件
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import UserProfile from '@/views/UserProfile.vue'
import NewPost from '@/views/NewPost.vue'
import ItemDetail from '@/views/ItemDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录', guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册', guest: true }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { title: '个人中心', requiresAuth: true }
  },
  {
    path: '/new-post',
    name: 'NewPost',
    component: NewPost,
    meta: { title: '发布信息', requiresAuth: true }
  },
  {
    path: '/item/:id',
    name: 'ItemDetail',
    component: ItemDetail,
    meta: { title: '物品详情' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 失物招领平台` : '失物招领平台'
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 已登录用户不能访问登录/注册页
  if (to.meta.guest && userStore.isLoggedIn) {
    next('/')
    return
  }
  
  next()
})

export default router 