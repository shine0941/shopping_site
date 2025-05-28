import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]
        content = data['content']

        # 儲存訊息到資料庫
        message = await self.save_message(self.room_id, user, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': user.email,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @staticmethod
    async def save_message(room_id, user, content):
        room = ChatRoom.objects.get(id=room_id)
        return Message.objects.create(room=room, sender=user, content=content)
