from django.db import models


# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    website = models.URLField()
    email = models.EmailField()
    logo = models.ImageField(upload_to='images/', default='images/default-supplier.png', blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
