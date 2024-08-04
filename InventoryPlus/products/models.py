from django.db import models
from suppliers.models import Supplier
from categories.models import Category
from django.core.mail import EmailMessage
from django.conf import settings


class Product(models.Model):
    productName = models.CharField(max_length=128)
    productDescription = models.TextField()
    productPrice = models.FloatField(default=0) # يحدده البائع 
    expirationDate = models.DateField()
    productStock = models.IntegerField(default=0) #بالبدايه راح تتعبى القيمه من السبلايرز في صفحة تسجيل المنتج 
    unitPrice = models.FloatField(default=0.0)
    productCategory = models.ForeignKey(Category, on_delete=models.PROTECT,null=True) # المفترض تكون سيلكت اوبشن ويختار منها المدير 
    productSupplier =  models.ManyToManyField(Supplier) # should be select options 
    productImage = models.ImageField(upload_to='images/')
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
    
    def calculateTotalPriceOfunits(self):
       return self.unitPrice * float(self.productStock)
    
