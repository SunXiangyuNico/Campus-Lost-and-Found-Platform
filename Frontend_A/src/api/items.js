import api from './auth.js'

// 获取物品列表
export const getItems = (params = {}) => {
  return api.get('/items', { params })
}

// 获取单个物品详情
export const getItemById = (id) => {
  return api.get(`/items/${id}`)
}

// 创建新物品
export const createItem = (itemData) => {
  return api.post('/items', itemData)
}

// 更新物品信息
export const updateItem = (id, itemData) => {
  return api.put(`/items/${id}`, itemData)
}

// 删除物品
export const deleteItem = (id) => {
  return api.delete(`/items/${id}`)
}

// 标记物品为已找回
export const markAsFound = (id) => {
  return api.put(`/items/${id}/found`)
}

// 搜索物品
export const searchItems = (searchParams) => {
  return api.get('/items/search', { params: searchParams })
}

// 获取用户发布的物品
export const getUserItems = (userId) => {
  return api.get(`/users/${userId}/items`)
}

// 上传图片
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('image', file)
  
  return api.post('/items/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 