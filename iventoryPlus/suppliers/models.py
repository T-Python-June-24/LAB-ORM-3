from django.db import models
from django.utils.timezone import now
from datetime import date
# Create your models here.
class Supplier(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="images/",default="images/no-logo-png-6.png")
    email=models.EmailField()
    website=models.URLField()
    phone=models.CharField(max_length=10)
    country=models.CharField(max_length=100)
    added=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name
