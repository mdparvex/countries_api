from django.db import models
from .countries import Country

class Capital(models.Model):
    capital_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='capitals')

    def __str__(self):
        return self.name