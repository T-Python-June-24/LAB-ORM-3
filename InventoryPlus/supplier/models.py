from django.db import models

class Supplier(models.Model):

    name = models.CharField(max_length=255)
    email =  models.EmailField()
    phone = models.IntegerField(max_length=13)



    def __str__(self):
        return self.name