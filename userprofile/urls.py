from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'), 
    path('initialize-profile/', views.initialize_profile, name='initialize_profile'),
    path('profile/add-address/', views.add_shipping_address, name='add_shipping_address'),
    path('profile/edit-address/<int:address_id>/', views.edit_shipping_address, name='edit_shipping_address'),
    path('profile/delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('update-user-info/', views.update_user_info, name='update_user_info'), 
    path('update-user-password/', views.update_user_password, name='update_user_password'), 
]