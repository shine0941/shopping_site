from django.db import models
from users.models import AdminUser

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Product(models.Model):
    merchant = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=100)  # 100 = 無折扣，90 = 九折
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    inventory = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    sold_count = models.PositiveIntegerField(default=0)  # 用於銷售排行

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name} Image"
