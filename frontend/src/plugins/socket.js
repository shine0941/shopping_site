let socket = null

export const initSocket = ({ room_id, token, onMessage, onClose }) => {
  socket = new WebSocket(`ws://192.168.1.100:8001/ws/chat/${room_id}/?token=${token}`)

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (onMessage) onMessage(data)
  }

  socket.onclose = () => {
    console.log('WebSocket closed')
    if (onClose) onClose()
  }
}

export const sendMessage = (message) => {
  if (socket && message.trim() !== '') {
    socket.send(JSON.stringify({ content: message }))
  }
}

export const closeSocket = () => {
  if (socket) socket.close()
}
