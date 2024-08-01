from django.db import models

# Create your models here.
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=128, null=False)
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    logo = models.ImageField(upload_to= 'images/',default= 'images/default.jpg')

    def __str__(self) -> str:
        return self.supplier_name