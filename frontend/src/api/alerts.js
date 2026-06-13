import api from './index'

export const getAlertRules = (params) => api.get('/alert-rules/', { params })
export const createAlertRule = (data) => api.post('/alert-rules/', data)
export const updateAlertRule = (id, data) => api.put(`/alert-rules/${id}/`, data)
export const deleteAlertRule = (id) => api.delete(`/alert-rules/${id}/`)

export const getAlertLogs = (params) => api.get('/alert-logs/', { params })
export const markRead = (id) => api.patch(`/alert-logs/${id}/mark_read/`)
export const markAllRead = () => api.patch('/alert-logs/mark_all_read/')

export const getEmailConfig = () => api.get('/email-config/')
export const updateEmailConfig = (data) => api.put('/email-config/update_config/', data)
export const sendTestEmail = (data) => api.post('/email-config/test_email/', data)

export const getEmailTemplate = () => api.get('/email-template/')
export const saveEmailTemplate = (data) => api.post('/email-template/', data)
