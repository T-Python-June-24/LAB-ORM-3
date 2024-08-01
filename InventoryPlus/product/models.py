from django.db import models
from category.models import Category
from supplier.models import Supplier
from datetime import datetime, timedelta


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    suppliers = models.ManyToManyField(Supplier, blank=True)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', default='images/default-product.jpg', blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    reorder_level = models.PositiveIntegerField()
    date_created = models.DateField(auto_now_add=True)

    def is_expiry_date_less_than_30_days(self):
        now = datetime.now()
        thirty_days_from_now = now + timedelta(days=30)
        return self.expiry_date < thirty_days_from_now

    def __str__(self):
        return self.name
