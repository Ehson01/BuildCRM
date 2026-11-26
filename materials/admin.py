from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'min_quantity', 'unit', 'price', 'created_at']
    search_fields = ['name']
    list_filter = ['unit', 'created_at']
    ordering = ['name']