from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('profile/', include('userprofile.urls')),
]
