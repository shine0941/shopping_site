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
from core.permissions import IsMerchantUser
from products.models import Product
import logging
from core.pagination import CustomPagination
from datetime import datetime
from django.db.models import Sum
from calendar import monthrange

logger = logging.getLogger(__name__)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        try:
            logger.info(request.data)

            shipping_fee = request.data.get("shipping_fee", 0)  # 先寫死，後續可調整
            coupon_code = request.data.get("coupon_code", "")
            recipient = request.data.get("recipient", "")
            address = request.data.get("address", "")
            phone = request.data.get("phone", "")

            cart = Cart.objects.get(customer=user)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({"error": "購物車是空的"}, status=status.HTTP_400_BAD_REQUEST)

            # 原始總價
            total_price = sum(int(item.product.price * Decimal(item.product.discount_percent / 100)) * item.quantity for item in cart_items)
            
            actual_price = total_price + shipping_fee

            # 優惠券處理（可選）
            
            coupon = None
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                    logger.info(coupon)
                    # check coupon valid
                    now = timezone.now()
                    if not (coupon.valid_from <= now <= coupon.valid_to):
                        return Response({"error": "優惠券已過期或尚未開始"}, status=status.HTTP_400_BAD_REQUEST)
                    if coupon.usage_limit>0 and coupon.used_count >= coupon.usage_limit:
                        return Response({"error": "優惠券已達使用上限"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    if coupon.discount_type=='percent':
                        actual_price = actual_price * (coupon.discount_value / 100)
                    elif coupon.discount_type=='fixed':
                        actual_price = actual_price - coupon.discount_value
                except Coupon.DoesNotExist:
                    return Response({"error": "無效的優惠券代碼"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    # 建立訂單
                    order = Order.objects.create(
                        customer=user,
                        total_price=total_price,
                        actual_price=actual_price,
                        shipping_fee=shipping_fee,
                        coupon=coupon,
                        merchant_summary={},  # 先留空，或根據商家分類進一步處理
                        order_status=OrderStatus.UNPAID,
                        recipient=recipient,
                        address=address,
                        phone=phone
                    )
                    
                    if coupon:
                        coupon.used_count += 1
                        coupon.save()

                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            unit_price=int(item.product.price * Decimal(item.product.discount_percent / 100))
                        )

                        logger.info(f"product {item.product} inventory & sold_count update")
                        target_product = item.product
                        target_product.inventory -= item.quantity
                        target_product.sold_count += item.quantity
                        target_product.save()

                    # 清空購物車
                    cart_items.delete()

                    # 回傳結果
                    serializer = OrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # Handle integrity error
                return Response({"error": "IntegrityError"}, status=status.HTTP_400_BAD_REQUEST)    
            except Exception as e:
                # Handle other exceptions
                logger.error(f"Create Order Exception:{e}")
                return Response({"error": "Exception error"}, status=status.HTTP_400_BAD_REQUEST)

        except Cart.DoesNotExist:
            return Response({"error": "找不到購物車"}, status=status.HTTP_404_NOT_FOUND)

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