from django.db import models

class SubRegion(models.Model):
    subregion_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name