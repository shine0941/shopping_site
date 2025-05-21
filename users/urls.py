from django.urls import path
from .views import AdminRegisterView, AdminTokenObtainPairView,CustomerTokenObtainPairView,CustomerRegisterView



urlpatterns = [
    path("register/admin/", AdminRegisterView.as_view(), name="admin-register"),
    path('login/admin/', AdminTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
    path("register/customer/", CustomerRegisterView.as_view(), name="customer-register"),
    path('login/customer/', CustomerTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),

]
