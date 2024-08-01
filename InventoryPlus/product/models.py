from django.db import models
from category.models import Category
from supplier.models import Supplier
from django.db.models import Sum

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="images/")
    suppliers = models.ManyToManyField(Supplier, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,related_name='products')

    def __str__(self):
        return self.name