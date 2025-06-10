import { defineStore } from 'pinia'
import api from '@/api/api'

export const orderStore = defineStore('order', {
  state: () => ({}),
  actions: {
    async getOrderList() {
      const res = await api.fetchOrders()
      return res.data
    },
  },
})
