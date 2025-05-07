from django.db import models
from .countries import Country

class Gini(models.Model):
    gini_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='gini_scores')
    year = models.CharField(max_length=10,null=True, blank=True)
    value = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.country.cca2} - {self.year}'