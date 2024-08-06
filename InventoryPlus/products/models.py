from django.db import models
from suppliers.models import Supplier  

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=512)
  description = models.TextField()

  def __str__(self) -> str:
    return self.name

class Product(models.Model):
  name = models.CharField(max_length=512)  
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  supplier = models.ManyToManyField(Supplier, related_name='products')
  image = models.ImageField(upload_to="images/")
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock_quantity = models.IntegerField()
  expiry_date = models.DateField(null=True, blank=True)


  def __str__(self) -> str:
    return self.name

