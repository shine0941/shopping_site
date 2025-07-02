import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from django.conf import settings
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        user = self.scope["user"]
        logger.info(f"{self.room_id} {user} connect")
        if user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user_email = self.scope["user"]
            logger.info(f"user_email:{user_email}")
            content = data['content']

            self.user = await database_sync_to_async(User.objects.get)(email=user_email)
            user = self.user
            # 儲存訊息到資料庫
            message = await self.save_message(self.room_id, user, content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'sender': user.id,
                        'content': message.content,
                        'timestamp': message.timestamp.isoformat(),
                    }
                }
            )
        except KeyError:
            print("❗接收到的資料缺少 'content' 欄位：", text_data)
            await self.send(text_data=json.dumps({
                'error': "Missing 'content' field."
            }))
        except json.JSONDecodeError:
            print("❗接收到非 JSON 格式資料：", text_data)
            await self.send(text_data=json.dumps({
                'error': "Invalid JSON format."
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    # @staticmethod
    @database_sync_to_async
    def save_message(self, room_id, user, content):
        room = ChatRoom.objects.get(id=room_id)
        return Message.objects.create(room=room, sender=user, content=content)
