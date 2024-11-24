from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField  # Use JSONField for dynamic attributes
from store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = models.JSONField(default=dict, blank=True)  # Store attributes as JSON

    def __str__(self):
        attribute_str = ", ".join(f"{key}: {value}" for key, value in self.attributes.items())
        return f"{self.product.name} ({attribute_str}) (x{self.quantity})"
