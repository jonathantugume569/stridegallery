from django.db import models
from cloudinary.models import CloudinaryField   # ✅ ADD THIS

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='categories/')   # ✅ CHANGE

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = CloudinaryField('image', folder='products/')   # ✅ CHANGE
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # ✅ Optional description

    def __str__(self):
        return self.name