from django.db import models
from django.utils.timezone import now
from datetime import date
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=120,unique=True)
    added=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name