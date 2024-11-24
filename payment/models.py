from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
import ast 

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True) 
    city_province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f'Shipping Address - {self.full_name}, {self.city_province}'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Cancel', 'Cancel'),
        ('Complete', 'Complete'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1500) 
    amount_paid = models.FloatField(default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    order_complete_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Order - {self.id} by {self.user.username if self.user else "Guest"}'

@receiver(pre_save, sender=Order)
def update_order_complete_date(sender, instance, **kwargs):
    if instance.status == 'Complete' and not instance.order_complete_date:
        instance.order_complete_date = now()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)
    attributes = models.TextField(null=True, blank=True) 

    def set_attributes(self, attr_dict):
        self.attributes = str(attr_dict)

    @property
    def decoded_attributes(self):
        if self.attributes:
            try:
                return ast.literal_eval(self.attributes)
            except (ValueError, SyntaxError):
                return {} 
        return {}