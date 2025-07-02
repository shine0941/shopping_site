// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('userData')) || null, // e.g. { id: 1, email: 'a@b.com', role: 'admin' }
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    isAdmin: (state) => state.user && state.user.role === 'manager',
    isMerchant: (state) => state.user && state.user.role === 'merchant',
    isStaff: (state) =>
      state.user && (state.user.role === 'manager' || state.user.role === 'merchant'),
    roleLevel: (state) =>
      state.user
        ? state.user.role === 'manager'
          ? 10
          : state.user.role === 'merchant'
            ? 1
            : 0
        : -1,
  },
  actions: {
    setUser(userData) {
      this.user = userData
      // console.log('userData', userData)
      localStorage.setItem('userData', JSON.stringify(this.user))
    },
    logout() {
      localStorage.removeItem('userData')
      this.user = null
    },
  },
})
