from django.db import models

# Create your models here.

class Lead(models.Model):
    Status = [
        ('new','new'),
        ('in_progress','in_progress'),
        ('contract','contract'),
        ('rejected','rejected'),
    ]
    house = models.ForeignKey('projects.HouseType',on_delete=models.PROTECT,related_name='leads')
    client = models.ForeignKey('contracts.Client', on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(blank=True,verbose_name='email')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=Status,default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'
        ordering = ['-created_at']

        
    def __str__(self):
        return self.name
