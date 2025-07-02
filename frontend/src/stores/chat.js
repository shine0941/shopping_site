import { defineStore } from 'pinia'
import api from '@/api/api'
import { useUserStore } from './user'

export const useChatStore = defineStore('chat', {
  state: () => ({
    room_id: localStorage.getItem('room_id') || '',
    history: [],
  }),
  actions: {
    async initChatStore() {
      // console.log('initChatStore')
      const res = await api.fetchChatRoom()
      if (res.data.length > 0) {
        this.room_id = res.data[0].id
        localStorage.setItem('room_id', this.room_id)
        // this.fetchChatHistory()
      } else {
        console.log('no chat room')
        this.createChatRoom()
      }
    },
    async createChatRoom() {
      const userid = useUserStore().userid
      const params = {
        customer: userid,
        merchant: 1,
      }
      const res = await api.createChatRoom(params)
      // console.log(res.data)
      this.room_id = res.data.id
      localStorage.setItem('room_id', this.room_id)
    },
    async fetchChatHistory() {
      const res = await api.fetchChatHistory(this.room_id)
      // console.log(res.data)
      this.history = res.data
      localStorage.setItem('chat_history', JSON.stringify(this.history))
      return this.history
    },
  },
})
