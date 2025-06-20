# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CreateOrderView,CustomerOrderListView,CustomerOrderDetailView,
BackendOrderListView,MonthlySalesStatsView,DailySalesStatsView)


urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', CustomerOrderListView.as_view(), name='customer-orders'),
    path('orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='customer-order-detail'),
    path('backend-list/', BackendOrderListView.as_view(), name='backend-orders'),
    path('stats/monthly-sales/', MonthlySalesStatsView.as_view()),
    path('stats/daily-sales/', DailySalesStatsView.as_view()),
]