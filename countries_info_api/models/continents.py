from django.db import models

class Continent(models.Model):
    continent_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name