# chat/serializers.py
from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from users.models import Customer
from users.serializers import UserSerializer

User = get_user_model()

class ChatRoomSerializer(serializers.ModelSerializer):
    # customer_detail = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    customer = UserSerializer(many=False)
    merchant = UserSerializer(many=False)
    class Meta:
        model = ChatRoom
        fields = ['id', 'customer', 'merchant', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_email', 'content', 'timestamp', 'is_read']

    def get_sender_email(self, obj):
        return obj.sender.email
