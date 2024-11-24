from django.urls import path, include
from . import views
from store.views import product_detail_view

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('product/<int:product_id>/', product_detail_view, name='product-details-view'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
]