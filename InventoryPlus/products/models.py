from django.db import models
from suppliers.models import Supplier

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    product_name = models.TextField()
    description = models.TextField()
    expiry_date = models.DateField(blank=True,null=True)
    stock_level = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    suppliers = models.ManyToManyField(Supplier)
    image = models.ImageField(upload_to= 'images/',default= 'images/default.jpg')
   

    def __str__(self) -> str:
        return self.product_name
    

    