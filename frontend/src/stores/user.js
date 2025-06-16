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
    userid: '',
  }),
  actions: {
    init(need_login = false) {
      console.log('useUserStore init')
      const token = localStorage.getItem('token')
      const refresh = localStorage.getItem('refresh')
      const username = localStorage.getItem('username')
      const userid = localStorage.getItem('userid')
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
          this.userid = userid
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
    async register(email, password) {
      try {
        const params = {
          email: email,
          password: password,
        }
        const res = await api.register(params)
        console.log('success', res.data)
        if (res.status == 201) {
          this.login(email, password)
        }
      } catch (err) {
        console.log('error', err)
        throw new Error('Register Failed')
      }
    },
    async login(email, password) {
      try {
        const params = {
          email: email,
          password: password,
        }
        const res = await api.login(params)
        console.log('success', res.data)
        this.token = res.data.access
        localStorage.setItem('token', this.token)
        this.refresh = res.data.refresh
        localStorage.setItem('refresh', this.refresh)

        // 取得用戶資訊
        this.userid = res.data.user.cid
        localStorage.setItem('userid', this.userid)
        this.username = res.data.user.full_name
        localStorage.setItem('username', this.username)

        console.log('call cartStore init')
        await cartStore().initCartStore()
      } catch (err) {
        console.log('error', err)
        throw new Error('Login Failed')
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
      this.userid = ''
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      localStorage.removeItem('username')
      localStorage.removeItem('userid')
      cartStore().clearCartStore()
      if (manual) {
        alert('logout successed')
        router.push('/')
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
    async updateUsername(username) {
      const params = {}
      params['full_name'] = username
      const res = await api.updateUser(this.userid, params)
      this.username = res.data.full_name
      localStorage.setItem('username', this.username)
    },
  },
})
