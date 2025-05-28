# views.py
from rest_framework import viewsets, permissions, generics
from django.utils import timezone
from django.db.models import F
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

class AvailableCouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(
            active=True,
            valid_from__lte=now,
            valid_to__gte=now,
        ).exclude(used_count__gte=F('usage_limit'))