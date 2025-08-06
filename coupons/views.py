# views.py
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
from django.utils import timezone
from django.db.models import F
from .models import Coupon
from .serializers import CouponSerializer
from core.permissions import IsMerchantUser
from core.pagination import CustomPagination

logger = logging.getLogger(__name__)
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    ordering_fields = ['id','created_at']
    ordering = ['-created_at']
    pagination_class = CustomPagination

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
class CheckCouponView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logger.info(request.data)
        coupon_code = request.data.get("coupon_code", "")
        logger.info(coupon_code)
        coupon = None
        is_valid = False
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon:
                    # check coupon valid
                    now = timezone.now()
                    if (coupon.valid_from <= now <= coupon.valid_to):
                        # return Response({"error": "優惠券已過期或尚未開始"}, status=status.HTTP_400_BAD_REQUEST)
                        is_valid = True
                    if coupon.usage_limit>0 and coupon.used_count < coupon.usage_limit:
                        is_valid = True
            except Coupon.DoesNotExist:
                is_valid = False
        
        coupon_data = None
        if is_valid:
            serializer = CouponSerializer(coupon)
            coupon_data = serializer.data
        
        return Response({
                    "is_valid": is_valid,
                    "coupon_data": coupon_data
                }, status=status.HTTP_200_OK)