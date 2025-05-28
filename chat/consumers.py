import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from django.conf import settings
from channels.db import database_sync_to_async


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

        # 解析 token
        # token = self.scope['query_string'].decode().split('=')[1]
        # try:
        #     validated_token = UntypedToken(token)
        #     decoded_data = jwt_decode(validated_token, settings.SECRET_KEY, algorithms=["HS256"])
        #     self.user = await database_sync_to_async(User.objects.get)(id=decoded_data["user_id"])
        # except Exception:
        #     await self.close()
        #     return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user = self.scope["user"]
            content = data['content']

            self.user = await database_sync_to_async(User.objects.get)(id=1)
            user = self.user
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
        print(f'user:{user}')
        room = ChatRoom.objects.get(id=room_id)
        return Message.objects.create(room=room, sender=user, content=content)
