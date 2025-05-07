from django.db import models
from .countries import Country

class Demonym(models.Model):
    demonym_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='demonyms')
    language_code = models.CharField(max_length=10)
    male = models.CharField(max_length=100)
    female = models.CharField(max_length=100)

    def __str__(self):
        return self.language_code