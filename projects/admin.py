
from django.contrib import admin
from .models import HouseType, ConstructionProject


@admin.register(HouseType)
class HouseTypeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "area",
        "floors",
        "price",
    )

    search_fields = ("title",)
    list_filter = ("floors",)


@admin.register(ConstructionProject)
class ConstructionProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "house_type",
        "foreman",
        "status",
        "start_date",
        "end_date",
    )

    search_fields = ("title", "address")
    list_filter = ("status",)
