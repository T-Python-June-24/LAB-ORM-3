from django.db import models
from suppliers.models import Supplier

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    suppliers = models.ManyToManyField('suppliers.Supplier')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)   #pic

    def __str__(self):
        return self.name
    
class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    # Other fields for Order
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.id} from {self.supplier.name}"

class Payment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Payment {self.id} to {self.supplier.name}"
    
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_items')
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
        