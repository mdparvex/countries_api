from django.db import models
from rest_framework import serializers

class Currency(models.Model):
    currency_id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.code
    
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']