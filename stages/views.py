
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from projects.models import ConstructionProject

from .forms import StageForm, StageReportForm
from .models import Stage, StageReport


class ProjectAccessMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_staff:
            return True

        if "project_id" in self.kwargs:
            project = get_object_or_404(
                ConstructionProject,
                pk=self.kwargs["project_id"]
            )
        else:
            stage = get_object_or_404(
                Stage,
                pk=self.kwargs["pk"]
            )
            project = stage.project

        return project.foreman == self.request.user




class StageCreateView(ProjectAccessMixin, CreateView):
    model = Stage
    form_class = StageForm
    template_name = "stages/stage_form.html"

    def form_valid(self, form):
        project = get_object_or_404(
            ConstructionProject,
            pk=self.kwargs["project_id"]
        )

        form.instance.project = project

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"pk": self.kwargs["project_id"]}
        )




class StageUpdateView(ProjectAccessMixin, UpdateView):
    model = Stage
    form_class = StageForm
    template_name = "stages/stage_form.html"

    def get_success_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"pk": self.object.project.pk}
        )




class StageReportCreateView(ProjectAccessMixin, CreateView):
    model = StageReport
    form_class = StageReportForm
    template_name = "stages/report_form.html"

    def form_valid(self, form):
        stage = get_object_or_404(
            Stage,
            pk=self.kwargs["pk"]
        )

        form.instance.stage = stage

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "projects:project_detail",
            kwargs={"pk": self.object.stage.project.pk}
        )
