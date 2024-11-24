from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from .models import Profile

# Unregister the default User model
admin.site.unregister(User)

class ProfileInline(StackedInline):
    model = Profile

@admin.register(User)

class UserAdmin(BaseUserAdmin, ModelAdmin):
    inlines = [ProfileInline]
    
    base_fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
    )

    permission_fieldset = (
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),     
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(self.base_fieldsets)
        if request.user.is_staff or request.user.is_superuser:
            fieldsets += list(self.permission_fieldset)
        return fieldsets

# Unregister the default Group model admin
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

    # Optional: Define the fieldsets if you want custom grouping of fields
    fieldsets = (
        (None, {
            'fields': ('name', 'permissions'),
        }),
    )