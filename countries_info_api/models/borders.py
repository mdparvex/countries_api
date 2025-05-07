from django.db import models

class Border(models.Model):
    border_id = models.BigAutoField(primary_key=True)
    border_with = models.CharField(max_length=10)

    def __str__(self):
        return self.border_with