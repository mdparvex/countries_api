from django.db import models
from rest_framework import serializers

class Language(models.Model):
    language_id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code', 'name']