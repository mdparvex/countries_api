from django.db import models
from rest_framework import serializers
from .countries import Country

class Translation(models.Model):
    translation_id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(max_length=10)
    official = models.CharField(max_length=255, null=True, blank=True)
    common = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language_code} - {self.official or self.common}"
    
class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['language_code', 'official', 'common']