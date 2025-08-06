from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from coupons.serializers import CouponSerializer
from users.serializers import UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(many=False, read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'created_at', 'total_price',
            'actual_price', 'shipping_fee', 'coupon',
            'merchant_summary', 'items','order_status'
        ]
