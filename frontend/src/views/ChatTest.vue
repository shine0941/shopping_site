<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">聊天室測試</h2>

    <div v-if="!token" class="mb-4">
      <h3 class="font-semibold">登入</h3>
      <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full mb-2" />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="border p-2 w-full mb-2"
      />
      <button @click="login" class="bg-blue-500 text-white px-4 py-2">登入</button>
    </div>

    <div v-else>
      <div class="border rounded p-4 h-64 overflow-y-scroll mb-4 bg-gray-100">
        <div v-for="(msg, index) in messages" :key="index" class="mb-2">
          <strong>{{ msg.sender }}:</strong> {{ msg.content }}
        </div>
      </div>
      <input
        v-model="message"
        type="text"
        placeholder="輸入訊息..."
        class="border p-2 w-full mb-2"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage" class="bg-green-500 text-white px-4 py-2">送出</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const token = ref(localStorage.getItem('access'))
const message = ref('')
const messages = ref([])
let socket = null

const login = async () => {
  try {
    // http://192.168.1.100:8001/api/docs/#/chat/chat_chatrooms_create
    const res = await axios.post('http://192.168.1.100:8001/users/admin/login/', {
      email: email.value,
      password: password.value,
    })
    token.value = res.data.access
    localStorage.setItem('access', token.value)
    initSocket()
  } catch (error) {
    alert('登入失敗')
  }
}

const initSocket = () => {
  //   socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/1/?token=${token.value}`)
  socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/1/`)

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    messages.value.push(data)
  }

  socket.onclose = () => {
    console.log('WebSocket closed')
  }
}

const sendMessage = () => {
  if (socket && message.value.trim() !== '') {
    socket.send(JSON.stringify({ content: message.value }))
    message.value = ''
  }
}

if (token.value) {
  initSocket()
}

onBeforeUnmount(() => {
  if (socket) {
    socket.close()
  }
})
</script>

<style scoped>
input {
  border-radius: 4px;
}
</style>
