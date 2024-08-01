from django.db import models
from product.models import Product

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField()
    status = models.BooleanField()
    create_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {'In Stock' if self.status else 'Out of Stock'}"