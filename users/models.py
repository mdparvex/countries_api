from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        if self.first_name is None or self.first_name== "":
            return str(self.user_id)
        elif self.last_name is None:
            return self.first_name
        else:
            return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['-user_id']

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name"]
