<template>
  <v-container style="max-width: 80vw; width: 70vw">
    <h3>customer service</h3>
    <v-spacer></v-spacer>
    <v-card width="70vw" min-height="50vh">
      <v-row style="height: 50vh">
        <v-col cols="4">
          <v-list v-for="(room, i) in rooms">
            <v-list-item :title="room.customer.email" @click="changeRoom(room)">
              <template v-slot:subtitle>
                {{ room.messages[room.messages.length - 1].content }}
              </template>
            </v-list-item>
            <v-divider inset v-if="i < rooms.length"></v-divider>
          </v-list>
        </v-col>
        <v-divider vertical length="100%"></v-divider>
        <v-col>
          <v-card-text>
            <h4 v-if="current_room">{{ current_room.customer.email }}</h4>
            <div style="overflow-y: scroll; max-height: 40vh">
              <div
                v-for="(msg, index) in messages"
                class="mb-2"
                :style="msg.sender == user.userid ? 'text-align: right;' : ''"
              >
                <v-chip>{{ msg.content }}</v-chip>
                <span style="font-size: x-small">{{ formatTimestamp(msg.timestamp) }}</span>
              </div>
            </div>
            <div style="display: flex">
              <v-text-field
                v-model="message"
                type="text"
                placeholder="輸入訊息..."
                class="border p-2 w-full mb-2"
                @keyup.enter="sendMessage"
                style="flex: 6"
              >
              </v-text-field>
              <button @click="sendMessage" class="bg-green-500 px-4 py-2" style="">送出</button>
            </div>
          </v-card-text>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useAdminChatStore } from '@/stores/adminchat'
import { useUserStore } from '@/stores/user'

const adminchat = useAdminChatStore()
const user = useUserStore()

const rooms = ref([])

const current_room = ref(null)
const messages = ref([])
const message = ref('')

let socket = null

const initSocket = (room_id) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close()
  }
  socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/${room_id}/?token=${user.token}`)
  socket.onmessage = (event) => {
    // console.log('onmessage')
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
    // scrollToBottom()
  }
}

const changeRoom = async (room) => {
  current_room.value = room
  messages.value = room.messages

  initSocket(room.id)
  //   trigger load all message
  const history = await adminchat.fetchChatHistory(room.id)
  messages.value = history
}

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // Month is 0-indexed
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  //   return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  return `${hours}:${minutes}`
}

const initChat = async () => {
  rooms.value = await adminchat.initChatStore()
  //   console.log('rooms.value', rooms.value)
}
onMounted(() => {
  //   console.log('onMounted')
  initChat()
})
</script>
