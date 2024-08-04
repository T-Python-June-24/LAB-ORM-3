from django.db import models
from django.utils import timezone




class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    



class Supplier(models.Model):
    name = models.CharField(max_length=500, unique=True)
    logo = models.ImageField(upload_to='supplier_logos/', blank=True, null=True, default="images/default_image.png")
    contact_email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField(Supplier, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, default="images/default_image.png")


    def __str__(self):
        return self.name
