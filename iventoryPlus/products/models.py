from django.db import models
from suppliers.models import Supplier
from categories.models import Category 

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    supplier=models.ManyToManyField(Supplier,null=True)
    added=models.DateTimeField(auto_now_add=True)
    stock_level=models.IntegerField()
    expirment=models.DateField(null=True)
    price=models.IntegerField()
    notified=models.BooleanField(default=False)
    notifeied_exieration=models.BooleanField(default=False)
    