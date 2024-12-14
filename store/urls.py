from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('', views.home_view, name="home"),
    path('products/', views.products_view, name='products-view'),  
    path('product/<int:product_id>/', views.product_detail_view, name='product-details-view'),
    path('about-us/', views.about_us_view, name='about-us'),
    path('rest-api/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('rest-api/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='api-product-detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
