import { defineStore } from 'pinia'
import api from '@/api/api'

export const cartStore = defineStore('cart', {
  state: () => ({
    cart: localStorage.getItem('cart') || '',
    cartItems: JSON.parse(localStorage.getItem('cartItems')) || [],
  }),
  actions: {
    async init() {
      console.log('cartStore init')
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
  },
})
