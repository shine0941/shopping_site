# chat/serializers.py
from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from users.models import Customer,User,AdminUser
from users.serializers import UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    # customer_detail = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    customer = UserSerializer(many=False,read_only=True)
    merchant = UserSerializer(many=False,read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Customer.objects.all(), write_only=True, source='customer')
    merchant_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=AdminUser.objects.all(), write_only=True, source='merchant')
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
