from django.db import models
from users.models import User
from products.models import Product
from coupons.models import Coupon  # 後面會建立
# from django.contrib.postgres.fields import JSONField  # PostgreSQL 專用

class OrderStatus(models.IntegerChoices):
    INIT = 0, "Init"

    UNPAID = 10, "Unpaid"
    PAID = 11, "Paid"

    PROCESSING = 20,"Processing"
    READYFORPICKUP = 21, "Ready for pickup"
    OUTOFDELIVERY = 22, "Out of delivery"
    DELIVERED = 23, "Delivered"

    FAILED = 90, "Failed"
    FAILEDPAYMENT = 91, "Payment failed"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 原始金額
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)  # 實際付款金額
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    merchant_summary = models.JSONField(default=dict, blank=True)  # 記錄涉及的商家資訊

    payment_method = models.CharField(max_length=50, blank=True)  # e.g., credit_card, line_pay
    payment_status = models.CharField(max_length=20, default="unpaid")  # unpaid, paid, failed
    paid_at = models.DateTimeField(null=True, blank=True)
    order_status = models.PositiveSmallIntegerField(choices=OrderStatus.choices,default=OrderStatus.INIT)

    recipient = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # 當下價格快照

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
