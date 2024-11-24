from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('payment_success', views.payment_success, name='payment_success'),
]

admin.site.index_template = 'admin/index.html'
admin.autodiscover()