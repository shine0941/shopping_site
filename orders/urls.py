# urls.py
from django.urls import path
from .views import CreateOrderView,CustomerOrderListView,CustomerOrderDetailView,BackendOrderListView


urlpatterns = [
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', CustomerOrderListView.as_view(), name='customer-orders'),
    path('orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='customer-order-detail'),
    path('admin/orders/', BackendOrderListView.as_view(), name='backend-orders'),
]