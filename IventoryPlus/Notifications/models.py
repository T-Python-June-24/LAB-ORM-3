# models.py

from django.db import models

class EmailRecipient(models.Model):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email
