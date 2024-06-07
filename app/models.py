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

# abcddef