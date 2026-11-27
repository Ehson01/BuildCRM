
from django.contrib import admin
from .models import Material, MaterialRequest


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'min_quantity', 'unit', 'price', 'created_at']
    search_fields = ['name']
    list_filter = ['unit', 'created_at']
    ordering = ['name']


@admin.register(MaterialRequest)
class MaterialRequestAdmin(admin.ModelAdmin):
    list_display = ['material', 'project', 'quantity', 'requested_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
