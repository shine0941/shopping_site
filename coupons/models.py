from django.db import models
from django.utils import timezone


# models.py
class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percent', '百分比'),  # eg. 10% off
        ('fixed', '固定金額'),  # eg. NT$100 off
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.PositiveIntegerField(help_text="百分比填 10 表示 10%，固定金額填實際數值")
    
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    minimum_order_amount = models.PositiveIntegerField(default=0)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="可使用幾次（null 表示不限）")
    used_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )

