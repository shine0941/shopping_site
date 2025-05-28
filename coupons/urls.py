# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet,AvailableCouponListView

router = DefaultRouter()
router.register(r'coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    path('', include(router.urls)),
    path('available/', AvailableCouponListView.as_view(), name='available-coupons'),
]