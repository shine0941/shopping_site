import { defineStore } from 'pinia'
// import axios from 'axios'
import api from '@/api/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
    cart: localStorage.getItem('cart') || '',
    cartItems: localStorage.getItem('cartItems') || [],
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

        const cartRes = await api.fetchCart()
        this.cart = cartRes.data[0].id
        localStorage.setItem('cart', this.cart)

        const cartItemsRes = await api.fetchCartItems()
        this.cartItems = cartItemsRes.data
        localStorage.setItem('cartItems', this.cartItems)
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
