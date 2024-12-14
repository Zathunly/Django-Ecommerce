from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
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

# Sale
class Sale(models.Model):
    name = models.CharField(max_length=255)
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage to apply (e.g., 20 for 20%)."
    )
    products = models.ManyToManyField('Product', related_name='sales', blank=True)

    def __str__(self):
        return self.name

    def apply_discount(self):
        for product in self.products.all():
            if not product.is_sale:
                product.is_sale = True
                product.sale_price = round(product.price * (1 - self.percent / 100), 2)
                product.save(update_fields=['is_sale', 'sale_price'])

    def remove_discount(self):
        for product in self.products.all():
            product.is_sale = False
            product.sale_price = 0
            product.save(update_fields=['is_sale', 'sale_price'])

# Sale Collection
class SaleCollection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    sales = models.ManyToManyField('Sale', related_name='collections')
    products = models.ManyToManyField(
        'Product',
        related_name='sale_collections',
        blank=True,
        help_text="Products included in this SaleCollection."
    )

    def __str__(self):
        return self.name

    def is_currently_active(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def apply_discounts(self):
        if self.is_currently_active():
            for sale in self.sales.all():
                sale.apply_discount()

    def remove_discounts(self):
        for sale in self.sales.all():
            sale.remove_discount()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_currently_active():
            self.apply_discounts()
        else:
            self.remove_discounts()

# Product model
class Product(models.Model):
    in_stock = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    sale_percentage = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter the discount percentage (0-100)."
    )
    sale_price = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
    
    def calculate_sale_price(self):
        if self.sale_percentage > 0 and self.price > 0:
            self.sale_price = round(self.price * (1 - (self.sale_percentage / 100)), 2)
            self.is_sale = True
        else:
            self.sale_price = 0
            self.is_sale = False

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

    def save(self, *args, **kwargs):
        self.calculate_sale_price()
        super().save(*args, **kwargs)



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
