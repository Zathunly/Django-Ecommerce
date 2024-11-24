from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.html import format_html


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.name

# SubCategory model
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'subcategory'
        verbose_name = 'Sub-category'
        verbose_name_plural = 'Sub-categories' 

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    in_stock = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0, validators=[MinValueValidator(0.01)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0, validators=[MinValueValidator(0.01)], blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
    
    def get_total_stock_quantity(self):
        return sum(stock.quantity for stock in self.stocks.all())

    def update_in_stock_status(self):
        if not self.stocks.exists():
            self.in_stock = False
        else:
            total_quantity = self.get_total_stock_quantity()
            self.in_stock = total_quantity > 0
        
        self.save(update_fields=['in_stock'])

    get_total_stock_quantity.short_description = "Stock Totals"

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)

    class Meta:
        unique_together = ('name', 'hex_code')

    def __str__(self):
        return self.name

    def color_block(self):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            self.hex_code
        )

    color_block.short_description = 'Color Block'

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="stocks")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='stock_images/', blank=True, null=True)

    class Meta:
        db_table = 'stock_product'
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ("product", "size", "color")  

    def __str__(self):
        return f"{self.product.name} - Size: {self.size.name}, Color: {self.color.name}, Quantity: {self.quantity}"

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)
        self.product.update_in_stock_status()
