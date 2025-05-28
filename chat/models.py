# chat/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_customer')
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_merchant')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
