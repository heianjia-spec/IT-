import api from './index'

export function login(data) {
  return api.post('/auth/login/', data)
}

export function getMe() {
  return api.get('/auth/me/')
}

export function changePassword(data) {
  return api.post('/auth/change-password/', data)
}
