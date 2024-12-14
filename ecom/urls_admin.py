# urls_admin.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views 

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('apply-sale-collection/', views.apply_sale_collection, name='apply_sale_collection'),
    path('get-subcategories/', views.get_subcategories, name='get-subcategories'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
