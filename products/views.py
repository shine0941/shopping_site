# views.py
import logging
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,ProductCategory
from .serializers import ProductSerializer,ProductCategorySerializer
from core.permissions import IsMerchantUser
from core.pagination import CustomPagination

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields=['category','is_available']
    ordering_fields = ['id','created_at', 'price']  # 允許排序的欄位
    ordering = ['-created_at']  # 預設排序：新到舊
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMerchantUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        merchant = self.request.user.adminuser  # 使用登入者對應的商家
        serializer.save(merchant=merchant)

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        # 商家只能看自己的商品；其他人可看全部
        if self.request.user.is_authenticated and hasattr(self.request.user, 'adminuser'):
            adminuser = getattr(self.request.user, 'adminuser')
            if adminuser.role == 'merchant':
                queryset =  queryset.filter(merchant=self.request.user.adminuser)
        else:
            queryset = queryset.filter(is_available=True)
        return queryset

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all().order_by('order')
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]