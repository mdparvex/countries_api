from django.db import models
from .countries import Country

class Tld(models.Model):
    tld_id = models.BigAutoField(primary_key=True)
    domain_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tlds')

    def __str__(self):
        return self.domain_name