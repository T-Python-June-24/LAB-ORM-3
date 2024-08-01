from django.db import models
from suppliers.models import Supplier
from categories.models import Category

# - As an Inventory Manager, I want to view a list of all inventory supplied by a supplier so that I can track how much business we do with the supplier.

class Product(models.Model):
    productName = models.CharField(max_length=128)
    productDescription = models.TextField()
    productImage = models.ImageField(upload_to='images/')
    productPrice = models.FloatField(default=0) # يحدده البائع 
    productionDate = models.DateField() 
    expirationDate = models.DateField()
    productStock = models.IntegerField(default=0) #بالبدايه راح تتعبى القيمه من السبلايرز في صفحة تسجيل المنتج 
    unitPrice = models.FloatField(default=0.0)
    totalPriceOfunits = models.FloatField(default=0.0)
    supplierDiscount = models.SmallIntegerField(default=0)
    productCategory = models.ForeignKey(Category, on_delete=models.PROTECT,null=True) # المفترض تكون سيلكت اوبشن ويختار منها المدير 
    productSupplier =  models.ManyToManyField(Supplier) # should be select options 
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName

