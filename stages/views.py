
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import ConstructionProject

from .forms import StageForm, StageReportForm
from .models import Stage


def check_project_access(request, project):
    if not request.user.is_staff and project.foreman_id != request.user.id:
        raise PermissionDenied


@login_required
def stage_create(request, project_id):
    project = get_object_or_404(
        ConstructionProject,
        pk=project_id
    )

    check_project_access(request, project)

    form = StageForm(request.POST or None)

    if form.is_valid():
        stage = form.save(commit=False)
        stage.project = project
        stage.save()

        return redirect("projects:project_detail", pk=project.pk)

    return render(
        request,
        "stages/stage_form.html",
        {"form": form, "project": project}
    )


@login_required
def stage_edit(request, pk):
    stage = get_object_or_404(
        Stage.objects.select_related("project"),
        pk=pk
    )

    check_project_access(request, stage.project)

    form = StageForm(
        request.POST or None,
        instance=stage
    )

    if form.is_valid():
        form.save()

        return redirect(
            "projects:project_detail",
            pk=stage.project.pk
        )

    return render(
        request,
        "stages/stage_form.html",
        {"form": form, "stage": stage}
    )


@login_required
def report_create(request, pk):
    stage = get_object_or_404(
        Stage.objects.select_related("project"),
        pk=pk
    )

    check_project_access(request, stage.project)

    form = StageReportForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        report = form.save(commit=False)
        report.stage = stage
        report.save()

        return redirect(
            "projects:project_detail",
            pk=stage.project.pk
        )

    return render(
        request,
        "stages/report_form.html",
        {"form": form, "stage": stage}
    )
