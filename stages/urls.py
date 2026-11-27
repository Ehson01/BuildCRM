
from django.urls import path

from . import views

app_name = "stages"

urlpatterns = [
    path(
        "project/<int:project_id>/create/",
        views.StageCreateView.as_view(),
        name="stage_create"
    ),

    path(
        "<int:pk>/edit/",
        views.StageUpdateView.as_view(),
        name="stage_edit"
    ),

    path(
        "<int:pk>/reports/create/",
        views.StageReportCreateView.as_view(),
        name="report_create"
    ),
]
