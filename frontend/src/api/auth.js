import axios from 'axios'

const API_BASE_URL = 'http://localhost:8080/api'

const authApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000
})

// 请求拦截器 - 添加token
authApi.interceptors.request.use(
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

import { mockUser } from '../utils/mockData'

export const authService = {
  // 登录
  login: async (studentId, password) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 模拟验证
    if (studentId === '2021001' && password === '123456') {
      return {
        user: mockUser,
        token: 'mock-jwt-token-' + Date.now()
      }
    } else {
      throw new Error('学号或密码错误')
    }
  },

  // 注册
  register: async (userData) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newUser = {
      id: Date.now(),
      studentId: userData.studentId,
      nickname: userData.nickname,
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      contact: userData.contact || '',
      college: userData.college || ''
    }
    
    return {
      user: newUser,
      token: 'mock-jwt-token-' + Date.now()
    }
  },

  // 获取用户信息
  getUserInfo: async () => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return mockUser
  }
} 