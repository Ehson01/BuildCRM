
from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("houses/", views.house_list, name="house_list"),
    path("houses/<int:pk>/", views.house_detail, name="house_detail"),
    path("houses/create/", views.house_create, name="house_create"),
    path("houses/<int:pk>/edit/", views.house_edit, name="house_edit"),
    path("houses/<int:pk>/delete/", views.house_delete, name="house_delete"),

    path("", views.ProjectListView.as_view(), name="project_list"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),

    path("my/", views.foreman_projects, name="foreman_projects"),
]
