import { defineStore } from 'pinia'
import api from '@/api/api'

export const cartStore = defineStore('cart', {
  state: () => ({
    cart: localStorage.getItem('cart') || '',
    cartItems: JSON.parse(localStorage.getItem('cartItems')) || [],
  }),
  actions: {
    init() {
      // console.log('cartStore init')
    },
    async initCartStore() {
      // console.log('cartStore init')
      const cartRes = await api.fetchCart()
      this.cart = cartRes.data[0].id
      localStorage.setItem('cart', this.cart)

      this.fetchCartItems()
    },
    async appendCartItems(product_id, quantity = 1) {
      const params = {
        quantity: quantity,
        product: product_id,
      }
      const res = await api.addToCart(params)
      this.fetchCartItems()
    },
    async fetchCartItems() {
      const cartItemsRes = await api.fetchCartItems()
      this.cartItems = cartItemsRes.data
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
    },
    async updateCartItem(item) {
      if (item.quantity > 0) {
        const res = await api.updateCartItem(item.id, {
          quantity: item.quantity,
        })
      } else {
        const res = await api.removeCartItem(item.id)
      }
      this.fetchCartItems()
    },
    async removeCartItem(item) {
      const res = await api.removeCartItem(item.id)
      this.fetchCartItems()
    },
    async checkout(params) {
      const res = await api.createOrder(params)
      // console.log('res', res)
      if (res.status == 201) {
        this.clearCartStore()
      }
      return res
    },
    clearCartStore() {
      // console.log('clearCartStore')
      this.cart = ''
      this.cartItems = []
      localStorage.removeItem('cart')
      localStorage.removeItem('cartItems')
    },
  },
})
