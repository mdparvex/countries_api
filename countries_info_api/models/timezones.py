from django.db import models

class Timezone(models.Model):
    timezone_id = models.BigAutoField(primary_key=True)
    zone = models.CharField(max_length=15)

    def __str__(self):
        return self.zone