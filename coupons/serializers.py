from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'discount_amount',
            'valid_from', 'valid_until',
            'usage_limit', 'used_count'
        ]
