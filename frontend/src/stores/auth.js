// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // e.g. { id: 1, email: 'a@b.com', role: 'admin' }
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    isAdmin: (state) => state.user && state.user.role === 'admin',
    isMerchant: (state) => state.user && state.user.role === 'merchant',
    isStaff: (state) =>
      state.user && (state.user.role === 'admin' || state.user.role === 'merchant'),
    roleLevel: (state) =>
      state.user ? (state.user.role === 'admin' ? 10 : state.user.role === 'merchant' ? 1 : 0) : -1,
  },
  actions: {
    setUser(userData) {
      this.user = userData
    },
    logout() {
      this.user = null
    },
  },
})
