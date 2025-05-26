# views.py
from rest_framework import viewsets, permissions
from .models import Coupon
from .serializers import CouponSerializer
from core.permissions import IsMerchantUser

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all().order_by('-created_at')
    serializer_class = CouponSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
