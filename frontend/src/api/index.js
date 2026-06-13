import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// Request interceptor — attach JWT token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — handle errors
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status
    if (status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      ElMessage.error('登录已过期，请重新登录')
      window.location.href = '/login'
    } else if (status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    }
    return Promise.reject(error)
  }
)

export default api
