# views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemSerializer
from products.models import Product
import logging

logger = logging.getLogger(__name__)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        if Cart.objects.filter(customer=request.user).exists():
            return Response({'detail': '購物車已存在'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer=self.request.user)
    
    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(customer=request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        logger.info(f"cart item create=>cart:{cart}|product:{product_id}|quantity:{quantity}")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            logger.info('update existed cart item')
            cart_item.quantity += quantity
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.info('create new cart item')
            serializer = self.get_serializer(data={"product_id": product_id, "quantity": quantity})
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="remove")
    def remove_item(self, request):
        item = self.get_object()
        cart = Cart.objects.get(customer=request.user)
        if not item.cart == cart:
            return Response({"error": "cart not match"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            item.delete()
            return Response({"message": "商品已從購物車移除"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "購物車中找不到該商品"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["delete"], url_path="clear")
    def clear_cart(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
            deleted_count, _ = CartItem.objects.filter(cart=cart).delete()
            return Response({"message": f"已清空購物車，共移除 {deleted_count} 項商品"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "找不到使用者的購物車"}, status=status.HTTP_404_NOT_FOUND)