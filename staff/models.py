from django.db import models


class Brigade(models.Model):
    name = models.CharField(max_length=100)
    foreman = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='brigades'
    )
   

    def __str__(self):
        return self.name