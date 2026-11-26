
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
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


def house_list(request):
    houses = HouseType.objects.all()

    query = request.GET.get("q")
    floors = request.GET.get("floors")
    min_area = request.GET.get("min_area")
    max_area = request.GET.get("max_area")

    if query:
        houses = houses.filter(title__icontains=query)

    if floors:
        houses = houses.filter(floors=floors)

    if min_area:
        houses = houses.filter(area__gte=min_area)

    if max_area:
        houses = houses.filter(area__lte=max_area)

    context = {
        "houses": houses,
    }

    return render(request, "projects/house_list.html", context)


def house_detail(request, pk):
    house = get_object_or_404(HouseType, pk=pk)

    return render(
        request,
        "projects/house_detail.html",
        {"house": house}
    )


@user_passes_test(lambda user: user.is_staff)
def house_create(request):
    form = HouseTypeForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("projects:house_list")

    return render(
        request,
        "projects/house_form.html",
        {"form": form}
    )


@user_passes_test(lambda user: user.is_staff)
def house_edit(request, pk):
    house = get_object_or_404(HouseType, pk=pk)

    form = HouseTypeForm(
        request.POST or None,
        request.FILES or None,
        instance=house
    )

    if form.is_valid():
        form.save()
        return redirect("projects:house_detail", pk=house.pk)

    return render(
        request,
        "projects/house_form.html",
        {"form": form, "house": house}
    )


@user_passes_test(lambda user: user.is_staff)
def house_delete(request, pk):
    house = get_object_or_404(HouseType, pk=pk)

    if request.method == "POST":
        house.delete()
        return redirect("projects:house_list")

    return render(
        request,
        "projects/house_confirm_delete.html",
        {"house": house}
    )




class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProjectListView(ManagerRequiredMixin, ListView):
    model = ConstructionProject
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        queryset = ConstructionProject.objects.select_related(
            "house_type",
            "foreman",
            "brigade",
            "contract",
        ).annotate(
            total_stages=Count("stages"),
            completed_stages=Count(
                "stages",
                filter=Q(stages__status="completed"),
            ),
        )

        status = self.request.GET.get("status")

        if status:
            queryset = queryset.filter(status=status)

        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = ConstructionProject
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        queryset = ConstructionProject.objects.select_related(
            "house_type",
            "foreman",
            "brigade",
            "contract",
        ).prefetch_related("stages__reports")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(foreman=self.request.user)


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

    def form_valid(self, form):
        project = self.object

        if project.contract_id:
            project.status = "archived"
            project.save(update_fields=["status"])
            return redirect(self.success_url)

        return super().form_valid(form)



@login_required
def foreman_projects(request):
    projects = ConstructionProject.objects.filter(
        foreman=request.user
    ).select_related("house_type").annotate(
        total_stages=Count("stages"),
        completed_stages=Count(
            "stages",
            filter=Q(stages__status="completed"),
        ),
    )

    return render(
        request,
        "projects/foreman_projects.html",
        {"projects": projects}
    )
