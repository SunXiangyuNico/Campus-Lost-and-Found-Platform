import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth.js'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isLoading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const userInfo = computed(() => user.value)

  // 方法
  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUser = (userData) => {
    user.value = userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  }

  // 登录
  const login = async (credentials) => {
    try {
      isLoading.value = true
      const response = await authApi.login(credentials)
      
      setToken(response.token)
      setUser(response.user)
      
      return { success: true, data: response }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || '登录失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const register = async (userData) => {
    try {
      isLoading.value = true
      const response = await authApi.register(userData)
      
      setToken(response.token)
      setUser(response.user)
      
      return { success: true, data: response }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || '注册失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      isLoading.value = true
      const response = await authApi.getUserInfo()
      setUser(response)
      return { success: true, data: response }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || '获取用户信息失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 更新用户信息
  const updateUserInfo = async (userData) => {
    try {
      isLoading.value = true
      const response = await authApi.updateUserInfo(userData)
      setUser(response)
      return { success: true, data: response }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || '更新用户信息失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 修改密码
  const changePassword = async (passwordData) => {
    try {
      isLoading.value = true
      await authApi.changePassword(passwordData)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.message || '修改密码失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 退出登录
  const logout = async () => {
    try {
      if (token.value) {
        await authApi.logout()
      }
    } catch (error) {
      console.error('退出登录失败:', error)
    } finally {
      setToken(null)
      setUser(null)
    }
  }

  // 初始化 - 从本地存储恢复用户状态
  const init = () => {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (error) {
        console.error('解析用户信息失败:', error)
        localStorage.removeItem('user')
      }
    }
  }

  // 初始化
  init()

  return {
    // 状态
    user,
    token,
    isLoading,
    
    // 计算属性
    isLoggedIn,
    userInfo,
    
    // 方法
    login,
    register,
    fetchUserInfo,
    updateUserInfo,
    changePassword,
    logout,
    setToken,
    setUser
  }
}) 