from django.db import models

class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryDescription = models.TextField(blank=True, null=True)
    categoryImage = models.ImageField(upload_to="images/", default="images/default.jpg")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoryName

    def product_count(self):
        return self.product_set.count()
