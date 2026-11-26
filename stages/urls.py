
from django.urls import path

from . import views

app_name = "stages"

urlpatterns = [
    path(
        "project/<int:project_id>/create/",
        views.stage_create,
        name="stage_create"
    ),

    path(
        "<int:pk>/edit/",
        views.stage_edit,
        name="stage_edit"
    ),

    path(
        "<int:pk>/reports/create/",
        views.report_create,
        name="report_create"
    ),
]
