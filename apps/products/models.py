from django.db import models
from apps.master.models import BaseModel


class Unit(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.short_name


class Product(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    additional_details = models.JSONField(blank=True, null=True)  # 👈 New field

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} Image"