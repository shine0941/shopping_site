# serializers.py
from rest_framework import serializers
from .models import Cart,CartItem
from products.serializers import CartProductSerializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['customer', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart']  # 其他欄位允許使用者傳入
