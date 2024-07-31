from django.db import models
from Supplier.models import Supplier
from Category.models import Category


# Create your models here.

class Product(models.Model):
    Name_Product = models.CharField(max_length=255)
    Status_Product = models.BooleanField()
    Quantity_Product = models.PositiveIntegerField()
    Price_Product = models.FloatField()
    Expiration_date = models.DateField(null=True)
    Created_at = models.DateField(auto_now_add=True)
    Images_Product = models.ImageField(default='images_product/default.png' , upload_to='images_Product/')
    Description_product = models.TextField(null=True)
    Category_product = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='products')
    Supplier_product = models.ManyToManyField(Supplier)
    Notifications = models.BooleanField(default=False)
