from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
