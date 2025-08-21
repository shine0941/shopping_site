import { defineStore } from 'pinia'
import api from '@/api/api'

export const orderStore = defineStore('order', {
  state: () => ({}),
  actions: {
    async getOrderList() {
      const res = await api.fetchOrders()
      return res.data
    },
    async getOrder(id) {
      console.log('getOrder', id)
      const res = await api.fetchOrder(id)
      return res.data
    },
    async cancelOrder(params) {
      const res = await api.cancelOrder(params)
      return res.data
    },
  },
})
