from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    image=models.FileField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    price=models.CharField(max_length=100, null=True, blank=True)
    discount = models.CharField(max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name+self.category.name

class Carousel(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product.name+" "+self.product.category.name
    
class UserProfile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile=models.CharField(max_length=100, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    image=models.FileField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product=models.TextField(default={'objects':[]}, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
