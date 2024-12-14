import os
from django import forms
from django.urls import path, reverse
from django.shortcuts import render, redirect  
from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Product, SubCategory, Stock, Color, Size, Sale, SaleCollection
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import ProductForm
from django.utils.timezone import now
from django.contrib.admin import register 
from django.urls import reverse_lazy  
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from django.views.generic import TemplateView


from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import action
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget
from unfold.views import UnfoldModelAdminViewMixin


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

class SaleAdmin(ModelAdmin):
    list_display = ('name', 'percent',)
    search_fields = ('name',)
    autocomplete_fields = ['products']

    class Media:
        css = {
            'all': ('css/admin/sale_product_search.css',),
        }

class SaleCollectionAdmin(ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('is_active', 'start_date', 'end_date')
    filter_horizontal = ('products', 'sales')  # Enable multi-selection for Many-to-Many fields
    date_hierarchy = 'start_date'  # Adds date-based navigation
    readonly_fields = ('is_active',)  # Example: Mark `is_active` as read-only if needed

    def save_model(self, request, obj, form, change):
        """Custom save logic for SaleCollection"""
        super().save_model(request, obj, form, change)
        # Handle many-to-many field saving explicitly (if necessary)
        if 'products' in form.cleaned_data:
            obj.products.set(form.cleaned_data['products'])  # Update products
        if 'sales' in form.cleaned_data:
            obj.sales.set(form.cleaned_data['sales'])  # Update sales

        obj.save()

class ProductAdmin(ModelAdmin):
    form = ProductForm
    autocomplete_fields = ['category', 'subcategory']
    exclude = ['in_stock']
    list_display = (
        'id', 
        'product_link', 
        'description', 
        'in_stock', 
        'get_total_stock_quantity', 
        'view_stock',
        'price', 
        'is_sale', 
        'sale_percentage',
        'formatted_sale_price', 
        'category', 
        'subcategory', 
        'image_preview', 
        'created_at', 
        'updated_at'
    )
    fields = (
        'name',
        'description',
        'price',
        'is_sale',
        'sale_percentage',
        'sale_price',
        'category',
        'subcategory',
        'image',
    )
    readonly_fields = ('sale_price',)
    search_fields = ('name', 'description') 
    list_editable = ['price', 'sale_percentage', 'is_sale', 'category', 'subcategory']
    actions = ['apply_sale_product_page']

    class Media:
        js = ('js/admin/product_changeform.js', 'js/admin/product_inline.js',)

    def formatted_sale_price(self, obj):
        if obj.sale_price:
            sale_price = f"{int(obj.sale_price):,}".replace(",", ".")
            return sale_price
        return "N/A"

    formatted_sale_price.short_description = "Sale Price"

    def product_link(self, obj):
        url = reverse('admin:store_product_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.name)
    product_link.short_description = 'Product'

    def view_stock(self, obj):
        url = reverse('admin:store_stock_changelist')
        query_params = f"?product__id__exact={obj.id}"
        full_url = f"{url}{query_params}"
        return format_html(
            '<a href="{}" class="button" '
            'style="text-decoration: none; font-weight: bold; color: white; '
            'background-color: #8e44ad; border: none; padding: 5px 10px; '
            'border-radius: 5px;">View</a>',
            full_url
        )
    view_stock.short_description = 'Stock Links'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 70px; height: auto;" /></a>',
                obj.image.url,  
                obj.image.url   
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'

    def category(self, obj):
        return obj.subcategory.category if obj.subcategory else 'N/A'
    category.short_description = 'Category'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-subcategories/', self.admin_site.admin_view(self.get_subcategories), name='get_subcategories'),
        ]
        return custom_urls + urls

    def get_changelist_form(self, request, **kwargs):
        kwargs['form'] = ProductForm
        return super().get_changelist_form(request, **kwargs)

    def get_subcategories(self, request):
        pass 

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image and os.path.exists(obj.image.path):
                os.remove(obj.image.path)
            obj.delete()

    @action(description=_("Apply Sale or SaleCollection to Selected Products"), url_path="apply-sale-action")
    def apply_sale_product_page(self, request: HttpRequest, permissions=["change_list"]):
        from django.shortcuts import render, redirect
        from django.urls import reverse_lazy
        from django.contrib import messages

        active_sales = Sale.objects.all()  
        active_collections = SaleCollection.objects.filter(is_active=True)  

        if request.method == "POST" and "apply_sale" in request.POST:
            selected_product_ids = request.POST.getlist("product_ids[]")
            sale_id = request.POST.get("sale")
            collection_id = request.POST.get("sale_collection")

            print(f"Selected Product IDs: {selected_product_ids}")
            print(f"Selected Sale ID: {sale_id}")
            print(f"Selected Sale Collection ID: {collection_id}")

            try:
                queryset = Product.objects.filter(id__in=selected_product_ids)

                if sale_id:
                    selected_sale = Sale.objects.get(id=sale_id)
                    discount_percent = selected_sale.percent
                    print(f"Applying Sale: {selected_sale.name} ({discount_percent}%)")

                    for product in queryset:
                        if product.price:  
                            discount = discount_percent / 100
                            new_sale_price = product.price * (1 - discount)
                            product.sale_price = round(new_sale_price, 2)
                            product.is_sale = True
                            product.save()

                    self.message_user(
                        request,
                        _("Successfully applied '%(sale)s' sale (%(percent)d%% discount) to %(count)d products.") % {
                            "sale": selected_sale.name,
                            "percent": discount_percent,
                            "count": queryset.count(),
                        },
                        level=messages.SUCCESS,
                    )

                elif collection_id:
                    selected_collection = SaleCollection.objects.get(id=collection_id)
                    if selected_collection.is_currently_active():
                        for sale in selected_collection.sales.all():
                            discount_percent = sale.percent
                            print(f"Applying Sale from Collection: {sale.name} ({discount_percent}%)")

                            for product in queryset.filter(sales=sale):
                                if product.price:  
                                    discount = discount_percent / 100
                                    new_sale_price = product.price * (1 - discount)
                                    product.sale_price = round(new_sale_price, 2)
                                    product.is_sale = True
                                    product.save()

                        self.message_user(
                            request,
                            _("Successfully applied the '%(collection)s' sale collection to %(count)d products.") % {
                                "collection": selected_collection.name,
                                "count": queryset.count(),
                            },
                            level=messages.SUCCESS,
                        )
                    else:
                        self.message_user(request, _("The selected sale collection is not active."), level=messages.WARNING)

                else:
                    self.message_user(request, _("No sale or sale collection was selected."), level=messages.ERROR)

            except Sale.DoesNotExist:
                self.message_user(request, _("The selected sale does not exist."), level=messages.ERROR)
            except SaleCollection.DoesNotExist:
                self.message_user(request, _("The selected sale collection does not exist."), level=messages.ERROR)

            return redirect(reverse_lazy("admin:store_product_changelist"))

        if request.method == "POST" and "action" in request.POST:
            selected_product_ids = request.POST.getlist("_selected_action")
            queryset = Product.objects.filter(id__in=selected_product_ids)

            return render(
                request,
                "admin/store/product/apply_sale_action.html",
                {
                    "queryset": queryset,
                    "sales": active_sales,
                    "collections": active_collections,
                    "opts": self.model._meta,
                    "back_url": request.META.get("HTTP_REFERER", reverse_lazy("admin:store_product_changelist")),
                },
            )

        self.message_user(request, _("No products were selected."), level=messages.ERROR)
        return redirect(reverse_lazy("admin:store_product_changelist"))

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
    list_editable = ('quantity','size', 'color',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 70px; height: auto;" /></a>',
                obj.image.url, 
                obj.image.url   
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleCollection, SaleCollectionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)