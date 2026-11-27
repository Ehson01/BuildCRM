
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ConstructionProjectForm, HouseTypeForm
from .models import ConstructionProject, HouseType



class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff




class HouseListView(ListView):
    model = HouseType
    template_name = "projects/house_list.html"
    context_object_name = "houses"


class HouseDetailView(DetailView):
    model = HouseType
    template_name = "projects/house_detail.html"
    context_object_name = "house"


class HouseCreateView(ManagerRequiredMixin, CreateView):
    model = HouseType
    form_class = HouseTypeForm
    template_name = "projects/house_form.html"
    success_url = reverse_lazy("projects:house_list")


class HouseUpdateView(ManagerRequiredMixin, UpdateView):
    model = HouseType
    form_class = HouseTypeForm
    template_name = "projects/house_form.html"
    success_url = reverse_lazy("projects:house_list")


class HouseDeleteView(ManagerRequiredMixin, DeleteView):
    model = HouseType
    template_name = "projects/house_confirm_delete.html"
    success_url = reverse_lazy("projects:house_list")




class ProjectListView(LoginRequiredMixin, ListView):
    model = ConstructionProject
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        if self.request.user.is_staff:
            return ConstructionProject.objects.all()

        return ConstructionProject.objects.filter(
            foreman=self.request.user
        )


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = ConstructionProject
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        if self.request.user.is_staff:
            return ConstructionProject.objects.all()

        return ConstructionProject.objects.filter(
            foreman=self.request.user
        )


class ProjectCreateView(ManagerRequiredMixin, CreateView):
    model = ConstructionProject
    form_class = ConstructionProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")


class ProjectUpdateView(ManagerRequiredMixin, UpdateView):
    model = ConstructionProject
    form_class = ConstructionProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")


class ProjectDeleteView(ManagerRequiredMixin, DeleteView):
    model = ConstructionProject
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project_list")




class ForemanProjectListView(LoginRequiredMixin, ListView):
    model = ConstructionProject
    template_name = "projects/foreman_projects.html"
    context_object_name = "projects"

    def get_queryset(self):
        return ConstructionProject.objects.filter(
            foreman=self.request.user
        )
