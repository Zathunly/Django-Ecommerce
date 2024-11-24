import os
from django import forms
from django.contrib import admin
from . models import Order, OrderItem
from .models import ShippingAddress, Order, OrderItem, PaymentMethod
from django.core.files.storage import default_storage
from decimal import Decimal
from django.utils.timezone import now
from django.contrib import messages

from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from import_export.admin import ImportExportModelAdmin
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    hide_title = True
    tab = True
    readonly_fields = ('price',) 
    max_num=0

    def get_readonly_fields(self, request, obj=None):
        return ('user', 'product', 'quantity', 'price', 'attributes')

class ShippingAddressAdmin(ModelAdmin):
    list_display = ('full_name', 'address1', 'address2', 'city_province', 'district')
    search_fields = ('full_name',)

class OrderForm(forms.ModelForm):
    amount_paid = forms.CharField(
        widget=UnfoldAdminTextInputWidget(attrs={
            'id': 'id_amount_paid',
            'type': 'text',
        })
    )

    class Meta:
        model = Order
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'amount_paid' in self.initial:
            amount_value = Decimal(self.initial['amount_paid']).normalize()
            formatted_amount = format(amount_value, 'f')
            if formatted_amount.endswith('.0'):
                formatted_amount = formatted_amount[:-2]
            self.initial['amount_paid'] = formatted_amount.replace('.', ',') 

    def clean_amount_paid(self):
        amount_paid = self.cleaned_data.get('amount_paid', '')
        try:
            normalized_amount = Decimal(amount_paid.replace('.', '').replace(',', '.')).normalize()
        except ValueError:
            raise forms.ValidationError("Invalid amount paid format.")
        return normalized_amount

class OrderAdmin(ModelAdmin):
    form = OrderForm
    inlines = [OrderItemInline]
    list_display = ('user', 'full_name', 'email', 'formatted_amount_paid', 'status', 'date_ordered', 'payment_method', 'order_complete_date')
    readonly_fields = ('amount_paid', 'date_ordered', 'payment_method', 'order_complete_date')  
    fields = ('user', 'full_name', 'email', 'amount_paid', 'date_ordered', 'status', 'payment_method', 'order_complete_date')
    search_fields = ('user__username', 'full_name', 'email')
    list_filter = ('date_ordered', 'payment_method')
    ordering = ('-date_ordered',)
    actions = ['mark_orders_as_complete']

    def formatted_amount_paid(self, obj):
        amount_paid = obj.amount_paid
        if amount_paid.is_integer():
            return f"{int(amount_paid):,}".replace(",", ".")
        else:
            return f"{amount_paid:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 

    formatted_amount_paid.short_description = 'Amount Paid'
    
    def mark_orders_as_complete(self, request, queryset):
        pending_orders = queryset.filter(status='Pending')  
        
        updated_count = pending_orders.update(
            status='Complete',
            order_complete_date=now()
        )
        completed_orders = queryset.filter(status='Complete')  

        messages.success(
            request,
            f"{updated_count} order(s) successfully marked as Complete."
        )

        for order in completed_orders:
            user = order.user
            if user and user.email:
                try:
                    user.email_user(
                        'Your order has been shipped',
                        f'Dear {user.username},\n\nYour order with ID {order.id} has been shipped.',
                        'admin@example.com',
                        fail_silently=False
                    )
                    print(f"Email sent to {user.email} for order ID {order.id}.")
                except Exception as e:
                    print(f"Failed to send email to {user.email}: {e}")
            else:
                print(f"Order #{order.id} does not have a user or email associated.")

    mark_orders_as_complete.short_description = "Mark selected orders as Complete"

    class Media:
        js = ('js/admin/format_order_amount_paid.js',)

class PaymentMethodAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register all models with their respective admin classes
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
