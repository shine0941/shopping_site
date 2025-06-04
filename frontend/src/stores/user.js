import { defineStore } from 'pinia'
// import axios from 'axios'
import api from '@/api/api'
import { cartStore } from './cart'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
  }),
  actions: {
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

        // 取得用戶資訊
        this.username = res.data.user.full_name
        localStorage.setItem('username', this.username)

        console.log('call cartStore init')
        await cartStore().init()
      } catch (err) {
        console.log('error', err)
        throw new Error('登入失敗')
      }
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('token')
      alert('logout successed')
    },
  },
})
