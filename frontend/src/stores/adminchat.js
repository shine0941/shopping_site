import { defineStore } from 'pinia'
import api from '@/api/api'
import { useUserStore } from './user'

export const useAdminChatStore = defineStore('adminchat', {
  state: () => ({
    rooms: [],
  }),
  actions: {
    async initChatStore() {
      // console.log('admin chat initChatStore')
      const res = await api.fetchStaffChatRoom()
      // console.log('res.data', res.data)
      if (res.data.length > 0) {
        this.rooms = res.data
      }
      return this.rooms
    },
    async fetchChatHistory(room_id) {
      const res = await api.fetchChatHistory(room_id)
      // console.log(res.data)
      this.history = res.data
      localStorage.setItem('chat_history', JSON.stringify(this.history))
      return this.history
    },
  },
})
