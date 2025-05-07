from django.db import models
from .countries import Country

class Idd(models.Model):
    idd_id = models.BigAutoField(primary_key=True)
    root = models.CharField(max_length=10)
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='idd')

    def __str__(self):
        return self.root