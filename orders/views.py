from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction, IntegrityError
from decimal import Decimal

from .models import Order, OrderItem, OrderStatus
from cart.models import Cart, CartItem
from coupons.models import Coupon
from .serializers import OrderSerializer
from core.permissions import IsMerchantUser, IsAdminUser, IsCustomerUser
from products.models import Product
import logging
from core.pagination import CustomPagination
from datetime import datetime
from django.db.models import Sum
from calendar import monthrange
from .services import checkout,cancel

logger = logging.getLogger(__name__)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    # @transaction.atomic
    def post(self, request):
        user = request.user
        shipping_fee = request.data.get("shipping_fee", 0)
        return checkout(
            user,shipping_fee,
            coupon_code=request.data.get("coupon_code", ""),
            recipient=request.data.get("recipient", ""),
            address=request.data.get("address", ""),
            phone=request.data.get("phone", ""),
        )

class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    # @transaction.atomic
    def post(self, request):
        user = request.user
        order_id = request.data.get("order_id")
        return cancel(user, order_id)

class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')

class CustomerOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
class BackendOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsMerchantUser]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['id','created_at']  # 允許排序的欄位
    ordering = ['-created_at']  # 預設排序：新到舊
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user.adminuser
        queryset = Order.objects.all()
        logger.info(user.role)
        if user.role=='merchant':
            # 找出商家的商品 ID
            merchant_products = Product.objects.filter(merchant=user).values_list('id', flat=True)
            # 找出有包含商家商品的訂單
            queryset = queryset.filter(items__product__in=merchant_products).distinct()
        elif user.role=='manager':
            pass
        else:
            queryset = queryset.none()
        return queryset
    
class MonthlySalesStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchantUser]

    def get(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        monthly_data = []

        for month in range(1, 13):
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            sales = (
                Order.objects
                .filter(created_at__gte=start_date, created_at__lt=end_date)
                .aggregate(total=Sum('actual_price'))['total'] or 0
            )

            monthly_data.append({
                'month': f'{month:02}',
                'sales': float(sales),
            })

        return Response({
            'year': year,
            'monthly_sales': monthly_data
        })
    
class DailySalesStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMerchantUser]

    def get(self, request):
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        daily_data = []

        (start,end) = monthrange(year, month)
        for day in range(start, end+1):
            start_time = datetime(year, month, day,0,0,0)
            end_time = datetime(year , month, day,23,59,59)
            

            sales = (
                Order.objects
                .filter(created_at__gte=start_time, created_at__lt=end_time)
                .aggregate(total=Sum('actual_price'))['total'] or 0
            )

            daily_data.append({
                'day': f'{day:02}',
                'sales': float(sales),
            })

        return Response({
            'year': year,
            'month': month,
            'daily_sales': daily_data
        }) 