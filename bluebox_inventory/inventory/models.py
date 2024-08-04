
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    website = models.URLField()
    image = models.ImageField(upload_to='supplier_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def is_expiring_soon(self):
        if self.expiry_date:
            return self.expiry_date <= timezone.now().date() + timedelta(days=5)
        return False

    def is_low_stock(self):
        return self.stock_quantity <= 5

    def __str__(self):
        return self.name

