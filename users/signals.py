from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import Customer
from cart.models import Cart
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Customer)
def auto_create_cart(sender, instance,created, **kwargs):
    if created:
        logger.info(f"New Cart instance of Customer created with id {instance.id}")
        Cart.objects.create(customer=instance.user)