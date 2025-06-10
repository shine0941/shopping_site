import { defineStore } from 'pinia'
import router from '@/router'
import api from '@/api/api'
import { cartStore } from './cart'
import { jwtDecode } from 'jwt-decode'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    refresh: '',
    username: '',
  }),
  actions: {
    init(need_login = false) {
      console.log('useUserStore init')
      const token = localStorage.getItem('token')
      const refresh = localStorage.getItem('refresh')
      const username = localStorage.getItem('username')
      if (token) {
        if (this.isTokenExpired(token)) {
          console.log('token expired')
          if (refresh && !this.isTokenExpired(refresh)) {
            console.log('call refreshAccess')
            this.refreshAccess()
          } else {
            console.log('refresh expired')
            this.handleNoToken(need_login)
          }
        } else {
          console.log('store token')
          this.token = token
          this.refresh = refresh
          this.username = username || ''
        }
      } else {
        console.log('no token')
        this.handleNoToken(need_login)
      }
      if (this.token) {
        console.log('user init cart')
        cartStore().initCartStore()
      }
    },
    handleNoToken(need_login = false) {
      cartStore().clearCartStore()
      if (need_login) {
        router.push('/login')
      }
    },
    async login(username, password) {
      try {
        const params = {
          email: username,
          password: password,
        }
        const res = await api.login(params)
        console.log('success', res.data)
        this.token = res.data.access
        localStorage.setItem('token', this.token)
        this.refresh = res.data.refresh
        localStorage.setItem('refresh', this.refresh)

        // 取得用戶資訊
        this.username = res.data.user.full_name
        localStorage.setItem('username', this.username)

        console.log('call cartStore init')
        await cartStore().initCartStore()
      } catch (err) {
        console.log('error', err)
        throw new Error('登入失敗')
      }
    },
    async refreshAccess() {
      console.log('refreshAccess')
      const refresh = localStorage.getItem('refresh')
      if (refresh) {
        const params = {
          refresh: refresh,
        }
        const res = await api.refresh(params)
        console.log('success', res.data)
        this.token = res.data.access
        localStorage.setItem('token', this.token)
      }
    },
    logout(manual = false) {
      this.token = ''
      this.refresh = ''
      this.username = ''
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      localStorage.removeItem('username')
      cartStore().clearCartStore()
      if (manual) {
        alert('logout successed')
      }
    },
    isTokenExpired(token) {
      try {
        const decoded = jwtDecode(token)
        const now = Date.now() / 1000 // 秒
        return decoded.exp < now
      } catch (err) {
        console.log('isTokenExpired err', err)
        return true
      }
    },
  },
})
