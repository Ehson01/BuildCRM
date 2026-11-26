from django.db import models


class Stage(models.Model):

    STATUS_CHOICES = [  # noqa: RUF012
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    project = models.ForeignKey(
        "projects.ConstructionProject",
        on_delete=models.CASCADE,
        related_name="stages"
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned"
    )

    order = models.PositiveIntegerField(default=1)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.project.title}"

    class Meta:
        ordering = ["order"]  # noqa: RUF012


class StageReport(models.Model):

    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    image = models.ImageField(upload_to="stage_reports/")
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.stage.title}"
