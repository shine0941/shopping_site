<template>
  <v-dialog width="40vw" max-height="50vh">
    <template v-slot:activator="{ props: activatorProps }">
      <v-tooltip text="Chat" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="mergeProps(activatorProps, props)" icon="mdi-cart">
            <v-icon>mdi-chat</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card width="30vw">
        <div style="display: flex">
          <v-card-title> customer service chat </v-card-title>
          <v-spacer></v-spacer>
          <v-btn @click="isActive.value = false" icon="mdi-close"></v-btn>
        </div>
        <v-card-text>
          <div style="height: 20vh; display: flex">
            <div id="chat" style="flex: 6; overflow-y: scroll">
              <div
                v-for="(msg, index) in messages"
                :key="index"
                class="mb-2"
                :style="msg.sender == user.userid ? 'text-align: right;' : ''"
              >
                <!-- <strong>{{ msg.sender }}:</strong> -->
                <v-chip>{{ msg.content }}</v-chip>
              </div>
            </div>
            <div style="flex: 1"></div>
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
        <!-- <v-card-actions>
          <v-btn text="Close Cart" @click="isActive.value = false" prepend-icon="mdi-close"></v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text="Checkout"
            prepend-icon="mdi-cart"
            to="/checkout/"
            @click="isActive.value = false"
          ></v-btn>
        </v-card-actions> -->
      </v-card>
    </template>
  </v-dialog>
</template>
<script setup>
import { mergeProps, onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
const user = useUserStore()
const chat = useChatStore()

const message = ref('')
const messages = ref([])
let socket = null

const initSocket = () => {
  socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/${chat.room_id}/?token=${user.token}`)
  //   socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/1/`)
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
    scrollToBottom()
  }
}
const initChat = async () => {
  const _ = await chat.initChatStore()
  const history = await chat.fetchChatHistory()
  messages.value = messages.value.concat(history)

  scrollToBottom()
}
const scrollToBottom = () => {
  const objDiv = document.getElementById('chat')
  if (objDiv) {
    objDiv.scrollTop = objDiv.scrollHeight
  }
}
onMounted(() => {
  //   check room exist
  initChat()
  if (user.isLoggedin) {
    initSocket()
  }
})
</script>
