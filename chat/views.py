# chat/views.py
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from users.serializers import UserSerializer

class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(customer=user) | ChatRoom.objects.filter(merchant=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room_id=room_id).order_by('timestamp')

class MerchantChatRoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # if request.user.id != merchant_id and not request.user.is_staff:
        #     return Response({'detail': 'Not allowed'}, status=403)

        chatrooms = ChatRoom.objects.filter(merchant=user).prefetch_related(
            Prefetch('messages', queryset=Message.objects.order_by('-timestamp'), to_attr='all_messages_desc')
        )

        data = []
        for room in chatrooms:
            # 先拿最新的 3 筆（倒序排列），再反轉成舊到新
            latest_messages = list(sorted(room.all_messages_desc[:3], key=lambda msg: msg.timestamp))
            messages = MessageSerializer(latest_messages, many=True).data

            room_data = {
                'id': room.id,
                'customer': UserSerializer(room.customer).data,
                'merchant': UserSerializer(room.merchant).data,
                'created_at': room.created_at,
                'messages': messages
            }
            data.append(room_data)

        return Response(data)