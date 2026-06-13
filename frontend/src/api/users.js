import api from './index'

export const getUsers = (params) => api.get('/auth/users/', { params })
export const createUser = (data) => api.post('/auth/users/', data)
export const updateUser = (id, data) => api.put(`/auth/users/${id}/`, data)
export const deleteUser = (id) => api.delete(`/auth/users/${id}/`)
export const resetPassword = (id, newPassword) => api.post(`/auth/users/${id}/reset_password/`, { new_password: newPassword })
