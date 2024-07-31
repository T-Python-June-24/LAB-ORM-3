from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='suppliers/', blank=True)
    last_active = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()