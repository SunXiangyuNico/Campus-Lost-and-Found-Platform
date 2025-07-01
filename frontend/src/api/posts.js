import axios from 'axios'

const API_BASE_URL = 'http://localhost:8080/api'

const postsApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000
})

// 请求拦截器 - 添加token
postsApi.interceptors.request.use(
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

import { mockPosts, mockMyPosts, mockClaimedPosts } from '../utils/mockData'

export const postsService = {
  // 获取帖子列表
  getPosts: async (search = '') => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    if (search) {
      return mockPosts.filter(post => 
        post.title.includes(search) || 
        post.description.includes(search) || 
        post.location.includes(search)
      )
    }
    return mockPosts
  },

  // 获取帖子详情
  getPostById: async (id) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return mockPosts.find(post => post.id === parseInt(id))
  },

  // 创建帖子
  createPost: async (postData) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newPost = {
      id: Date.now(),
      type: postData.type,
      title: postData.title,
      description: postData.description,
      location: postData.location,
      latitude: postData.latitude,
      longitude: postData.longitude,
      status: 'open',
      createdAt: new Date().toISOString(),
      author: {
        id: 1,
        nickname: '小明',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        studentId: '2021001'
      },
      images: ['https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'],
      comments: []
    }
    
    return newPost
  },

  // 认领帖子
  claimPost: async (postId) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    return { success: true }
  },

  // 添加评论
  addComment: async (postId, content) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const newComment = {
      id: Date.now(),
      content,
      createdAt: new Date().toISOString(),
      author: {
        id: 1,
        nickname: '小明',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        studentId: '2021001'
      }
    }
    
    return newComment
  },

  // 获取我的帖子
  getMyPosts: async () => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return mockMyPosts
  },

  // 获取历史认领
  getClaimedPosts: async () => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return mockClaimedPosts
  },

  // 更新帖子状态
  updatePostStatus: async (postId, status) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return { success: true }
  },

  // 删除帖子
  deletePost: async (postId) => {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    return { success: true }
  }
} 