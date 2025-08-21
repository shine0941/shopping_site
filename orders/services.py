# order/services/checkout_service.py
from decimal import Decimal
import logging

from django.utils import timezone
from django.db import transaction, IntegrityError

from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters

from .models import Order,OrderStatus,OrderItem
from .serializers import OrderSerializer
from cart.models import Cart,CartItem
from coupons.models import Coupon

logger = logging.getLogger(__name__)

@transaction.atomic
def checkout(user, shipping_fee, **kwargs):
    try:
        coupon_code = kwargs['coupon_code']
        recipient = kwargs['recipient']
        address = kwargs['address']
        phone = kwargs['phone']

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
                else:
                    coupon.used_count += 1
                    coupon.save()
                
                if coupon.discount_type=='percent':
                    actual_price = actual_price * (coupon.discount_value / 100)
                elif coupon.discount_type=='fixed':
                    actual_price = actual_price - coupon.discount_value
            except Coupon.DoesNotExist:
                return Response({"error": "無效的優惠券代碼"}, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO 金流

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
    
@transaction.atomic
def cancel(user, order_id, **kwargs):
    order = Order.objects.get(id=order_id)

    with transaction.atomic():
        # check order status
        if not order.is_cancellable:
            return Response({"error": "Order is not cancellable"}, status=status.HTTP_400_BAD_REQUEST)
        
        # refund
        # TODO 金流
        pass
        
        # reset coupon
        if order.coupon:
            order.coupon.used_count -= 1
            order.coupon.save()

        # reset products
        if order.items:
            items = OrderItem.objects.filter(order=order)
            for item in items:
                target_product = item.product
                target_product.inventory += item.quantity
                target_product.sold_count -= item.quantity
                target_product.save()
        
        # update order status
        order.order_status = OrderStatus.CANCELLED
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)