from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=180)
   
    def __str__(self):
        return self.name

class subCategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(category,on_delete=models.CASCADE)    

    def __str__(self):
        return self.name
    
class product(models.Model):
    category = models.ForeignKey(category,on_delete=models.CASCADE)  
    subcategory = models.ForeignKey(subCategory,on_delete=models.CASCADE)    
    image = models.ImageField(upload_to='static/images/home')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username} - {self.product.name} x {self.quantity}"

    def get_total(self):
        return self.product.price * self.quantity
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='static/profile_images/', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'    