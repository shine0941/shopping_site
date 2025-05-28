# chat/urls.py
from django.urls import path
from .views import ChatRoomListCreateView, ChatMessageListView

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:room_id>/messages/', ChatMessageListView.as_view(), name='chatroom-messages'),
]
