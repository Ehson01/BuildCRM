
from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("houses/", views.HouseListView.as_view(), name="house_list"),
    path("houses/create/", views.HouseCreateView.as_view(), name="house_create"),
    path("houses/<int:pk>/", views.HouseDetailView.as_view(), name="house_detail"),
    path("houses/<int:pk>/edit/", views.HouseUpdateView.as_view(), name="house_edit"),
    path("houses/<int:pk>/delete/", views.HouseDeleteView.as_view(), name="house_delete"),

    path("", views.ProjectListView.as_view(), name="project_list"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("my/", views.ForemanProjectListView.as_view(), name="foreman_projects"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/archive/", views.ProjectArchiveView.as_view(), name="project_archive"),
]
