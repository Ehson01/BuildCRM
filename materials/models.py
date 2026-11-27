from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=10)
    unit = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    

class MaterialRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(
        'projects.ConstructionProject',
        on_delete=models.CASCADE,
        related_name='material_requests'
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='requests'
    )

    quantity = models.PositiveIntegerField()

    requested_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='material_requests'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.material.name} - {self.quantity}'
