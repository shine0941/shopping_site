from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import OrderItem
from products.models import Product

@receiver(post_save, sender=OrderItem)
def auto_product_update(sender, instance,created, **kwargs):
    if created:
        print(f"product {instance.product} inventory & sold_count update")
        product = instance.product
        product.inventory -= instance.quantity
        product.sold_count += instance.quantity
        product.save()
        print(f"done")