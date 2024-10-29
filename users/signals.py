from django.db.models.signals import post_save
from .models import User
from order.models import Cart
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in)
def update_last_active_on_login(sender, request, user, **kwargs):
    user.update_last_active()

@receiver(user_logged_out)
def update_last_active_on_logout(sender, request, user, **kwargs):
    user.update_last_active()

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(cart_id=instance)


