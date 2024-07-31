from django.db import models

# Create your models here.
class Supplier(models.Model):
    name_Supplier = models.CharField(max_length=255)
    logo_Supplier = models.ImageField(default="images/default.png",upload_to="images_supplier/")
    email_supplier = models.EmailField()
    number_phone = models.CharField(max_length=9)
    address_Supplier = models.TextField( null=True )
    website_Supplier = models.URLField(null=True)
    
