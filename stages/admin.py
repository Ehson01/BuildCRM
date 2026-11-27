
from django.contrib import admin
from .models import Stage, StageReport


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "order",
    )

    list_filter = ("status",)
    search_fields = ("title",)


@admin.register(StageReport)
class StageReportAdmin(admin.ModelAdmin):
    list_display = (
        "stage",
        "created_at",
    )

    list_filter = ("created_at",)
