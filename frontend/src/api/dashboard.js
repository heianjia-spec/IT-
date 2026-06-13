import api from './index'

export const getSummary = () => api.get('/dashboard/summary/')
export const getByCategory = () => api.get('/dashboard/by_category/')
export const getByDepartment = () => api.get('/dashboard/by_department/')
export const getByStatus = (params) => api.get('/dashboard/by_status/', { params })
export const getExpiryReminders = () => api.get('/dashboard/expiry_reminders/')
