from django.db import models
from .idd import Idd

class IddSuffix(models.Model):
    suffix_id = models.BigAutoField(primary_key=True)
    suffix = models.CharField(max_length=10)
    idd = models.ForeignKey(Idd, on_delete=models.CASCADE, related_name='suffixes')

    def __str__(self):
        return self.suffix