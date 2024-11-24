import os
from django import forms
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import admin, messages
from .models import Category, Product, SubCategory, Stock, Color, Size
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from decimal import Decimal
from django.core.files.storage import default_storage
from django.forms.widgets import Select


from .views import get_subcategories
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget


# Inline for SubCategory within Category
class SubCategoryInline(StackedInline):
    model = SubCategory
    extra = 1
    tab = True

class CategoryAdmin(ModelAdmin):
    inlines = [SubCategoryInline] 
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)

class SubCategoryAdmin(ModelAdmin):
    list_display = ('name', 'description', 'category', 'created_at', 'updated_at')
    search_fields = ('name',)


class ProductForm(forms.ModelForm):
    price = forms.CharField(
        widget=UnfoldAdminTextInputWidget(attrs={
            'id': 'id_price',
            'type': 'text',  
        })
    )
    sale_price = forms.CharField(
        widget=UnfoldAdminTextInputWidget(attrs={
            'id': 'id_sale_price',
            'type': 'text',
        }),
        required=False  # Mark as optional since it's hidden initially
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=UnfoldAdminSelectWidget(attrs={
            'id': 'id_category',
            'class': 'custom-category-select'  
        }),
        label="Category"
    )

    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        widget=UnfoldAdminSelectWidget(attrs={
            'id': 'id_subcategory',
            'class': 'custom-subcategory-select'  
        }),
        label="Subcategory"
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format initial value for 'price'
        if 'price' in self.initial and self.initial['price'] is not None:
            price_value = Decimal(self.initial['price']).normalize()
            price_str = format(price_value, 'f')
            if price_str.endswith('.0'):
                price_str = price_str[:-2]
            self.initial['price'] = price_str

        # Format initial value for 'sale_price' if it exists and is not None
        if 'sale_price' in self.initial and self.initial['sale_price'] is not None:
            sale_price_value = Decimal(self.initial['sale_price']).normalize()
            sale_price_str = format(sale_price_value, 'f')
            if sale_price_str.endswith('.0'):
                sale_price_str = sale_price_str[:-2]
            self.initial['sale_price'] = sale_price_str

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price:
            normalized_price = price.replace('.', '').replace(',', '.')
            cleaned_price = Decimal(normalized_price)
            return cleaned_price.normalize()
        return price

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price:
            normalized_sale_price = sale_price.replace('.', '').replace(',', '.')
            cleaned_sale_price = Decimal(normalized_sale_price)
            return cleaned_sale_price.normalize()
        return sale_price

class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    form = ProductForm
    autocomplete_fields = ['category', 'subcategory']
    exclude = ['in_stock',]
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = (
        'id', 
        'product_link', 
        'description', 
        'in_stock', 
        'get_total_stock_quantity', 
        'view_stock',
        'formatted_price', 
        'is_sale', 
        'formatted_sale_price', 
        'category', 
        'subcategory', 
        'image_preview', 
        'created_at', 
        'updated_at'
    )    
    search_fields = ('name', 'subcategory__name')

    def product_link(self, obj):
        url = reverse('admin:store_product_change', args=[obj.id]) 
        return format_html('<a href="{}">{}</a>', url, obj.name)
    
    product_link.short_description = 'Product'

    def view_stock(self, obj):
        url = reverse('admin:store_stock_changelist')  
        query_params = f"?product__id__exact={obj.id}"
        full_url = f"{url}{query_params}"
        return format_html(
            '<a href="{}" class="button" style="text-decoration: none;font-weight:bold ; color: white; background-color: #8e44ad; border: none; padding: 5px 10px; border-radius: 5px;">View</a>',
            full_url
        )

    view_stock.short_description = 'Stock Links'

    def image_preview(self, obj):
        if obj.image:  # Check if an image exists
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-subcategories/', self.admin_site.admin_view(get_subcategories), name='get_subcategories'),
        ]
        return custom_urls + urls
    
    class Media:
        js = ('js/admin/products.js',)  

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                file_path = obj.image.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            obj.delete()
    
    def category(self, obj):
        if obj.subcategory:
            return obj.subcategory.category
        return 'N/A'
    category.short_description = 'Category'

    def formatted_price(self, obj):
        price = obj.price
        if price.is_integer():
            price = int(price)
            return f"{price:,.0f}".replace(",", ".") 
        else:
            return f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    formatted_price.short_description = 'Price'

    def formatted_sale_price(self, obj):
        sale_price = obj.sale_price
        if not sale_price: 
            return "-" 
        if sale_price.is_integer():
            sale_price = int(sale_price)
            return f"{sale_price:,.0f}".replace(",", ".")
        else:
            return f"{sale_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
    formatted_sale_price.short_description = 'Sale Price'

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'

class ColorAdminForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'hex_code': ColorPickerWidget(),  
        }

class ColorAdmin(ModelAdmin):
    form = ColorAdminForm
    list_display = ('name', 'color_block', 'hex_code')
    search_fields = ['name']

class SizeAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class StockAdmin(ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ['product', 'quantity', 'location', 'size', 'color', 'image_preview','last_updated']
    search_fields = ('name',)
    list_filter = ('product','size', 'color')

    def image_preview(self, obj):
        if obj.image:  
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No Image"

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)









