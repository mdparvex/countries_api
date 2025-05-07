from django.db import models

class Region(models.Model):
    region_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name