from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='images/', blank=True, null=True)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name