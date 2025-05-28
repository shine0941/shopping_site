from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AdminRegisterView, AdminTokenObtainPairView,
                    CustomerTokenObtainPairView,CustomerRegisterView,CustomerView)

router = DefaultRouter()
router.register(r'customers', CustomerView, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path("admin/register/", AdminRegisterView.as_view(), name="admin-register"),
    path('admin/login/', AdminTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path("customer/register/", CustomerRegisterView.as_view(), name="customer-register"),
    path('customer/login/', CustomerTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),

]
