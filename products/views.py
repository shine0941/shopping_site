# views.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,ProductCategory
from .serializers import ProductSerializer,ProductCategorySerializer
from core.permissions import IsMerchantUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['category']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMerchantUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        merchant = self.request.user.adminuser  # 使用登入者對應的商家
        serializer.save(merchant=merchant)

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        # 商家只能看自己的商品；其他人可看全部
        if self.request.user.is_authenticated and hasattr(self.request.user, 'adminuser'):
            return Product.objects.filter(merchant=self.request.user.adminuser).order_by('-created_at')
        return Product.objects.all().order_by('-created_at')

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all().order_by('order')
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]