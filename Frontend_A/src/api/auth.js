import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // token过期，清除本地存储并跳转到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 用户注册
export const register = (userData) => {
  return api.post('/auth/register', userData)
}

// 用户登录
export const login = (credentials) => {
  return api.post('/auth/login', credentials)
}

// 获取用户信息
export const getUserInfo = () => {
  return api.get('/auth/profile')
}

// 更新用户信息
export const updateUserInfo = (userData) => {
  return api.put('/auth/profile', userData)
}

// 修改密码
export const changePassword = (passwordData) => {
  return api.put('/auth/password', passwordData)
}

// 退出登录
export const logout = () => {
  return api.post('/auth/logout')
}

export default api 