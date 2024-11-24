from django.db import models
from django.dispatch import receiver
from payment.models import ShippingAddress
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city_province = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


@receiver(post_save, sender=Profile)
def create_or_update_shipping_address(sender, instance, **kwargs):
    full_name = f"{instance.user.first_name} {instance.user.last_name}".strip()
    shipping_address, created = ShippingAddress.objects.get_or_create(user=instance.user)
    shipping_address.full_name = full_name
    shipping_address.address1 = instance.address1
    shipping_address.address2 = instance.address2
    shipping_address.city_province = instance.city_province
    shipping_address.district = instance.district
    shipping_address.save()

post_save.connect(create_profile, sender=User)

                   