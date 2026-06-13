import { defineStore } from 'pinia'
import { login as apiLogin, getMe } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    role: (state) => state.user?.role || '',
    isAdmin: (state) => state.user?.role === 'admin',
    canWrite: (state) => ['admin', 'asset_manager'].includes(state.user?.role),
  },
  actions: {
    async login(username, password) {
      const res = await apiLogin({ username, password })
      this.token = res.data.access
      this.refreshToken = res.data.refresh
      this.user = res.data.user
      localStorage.setItem('access_token', this.token)
      localStorage.setItem('refresh_token', this.refreshToken)
      return res.data
    },
    async fetchUser() {
      try {
        const res = await getMe()
        this.user = res.data
      } catch {
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.token = ''
      this.refreshToken = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})
