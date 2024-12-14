from django.contrib import admin
from django.db import models
from .models import HomeBanner
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.widgets import UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget

@admin.register(HomeBanner)
class HomeBannerAdmin(ModelAdmin):
    list_display = ('title', 'image', 'description', "display_order", "is_active",)