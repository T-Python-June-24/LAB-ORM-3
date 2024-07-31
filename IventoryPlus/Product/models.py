from django.db import models
from Categories.models import Category
from Suppliers.models import Supplier

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='images/', default='images/default.jpg')
    description = models.TextField()
    price = models.FloatField()
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField(Supplier)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)  

    def __str__(self):
        return self.name
