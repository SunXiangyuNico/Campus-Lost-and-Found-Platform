import axios from 'axios'

// 配置axios基础URL，指向mock服务器
axios.defaults.baseURL = 'http://localhost:3001'

const API_BASE = '/api/auth'

export function register(data) {
  return axios.post(`${API_BASE}/register`, data)
}

export function login(data) {
  return axios.post(`${API_BASE}/login`, data)
}

export function getUserInfo(token) {
  return axios.get(`${API_BASE}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  })
} 