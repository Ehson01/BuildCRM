
from django.db import models
from django.conf import settings


class HouseType(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    floors = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="houses/")

    def __str__(self):
        return self.title


class ConstructionProject(models.Model):

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=150)
    address = models.CharField(max_length=255)

    house_type = models.ForeignKey(
        HouseType,
        on_delete=models.PROTECT,
        related_name="construction_projects"
    )

    foreman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="managed_projects",
        null=True,
        blank=True
    )

    contract = models.OneToOneField(
        "contracts.Contract",
        on_delete=models.PROTECT,
        related_name="construction_project",
        null=True,
        blank=True
    )

    brigade = models.ForeignKey(
        "staff.Brigade",
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
