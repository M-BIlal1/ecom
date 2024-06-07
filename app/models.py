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

# class UserManager(BaseUserManager):
#   def create_user(self, email,username = 'NULL' ,password=None):
#       """
#       Creates and saves a User with the given email, name, tc and password.
#       """
#       if not email:
#           raise ValueError('User must have an email address')

#       user = self.model(
#           email=self.normalize_email(email),username = username
#       )

#       user.set_password(password)
#       user.save(using=self._db)
#       return user

#   def create_superuser(self, email,name, password=None):
#       """
#       Creates and saves a superuser with the given email, name, tc and password.
#       """
#       user = self.create_user(
#           email,
#           password=password
#       )
#       user.is_admin = True
#       user.save(using=self._db)
#       return user

# #  Custom User Model
# class User(AbstractBaseUser):
#   email = models.EmailField(
#       verbose_name='Email',
#       max_length=255,
#       unique=True,
#   )
#   name = models.CharField(max_length=200)
#   username = models.CharField(max_length=200,default="none")
#   is_active = models.BooleanField(default=True)
#   is_admin = models.BooleanField(default=False)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

#   objects = UserManager()

#   USERNAME_FIELD = 'username'
#   REQUIRED_FIELDS = ['name',]

#   def __str__(self):
#       return self.email

#   def has_perm(self, perm, obj=None):
#       "Does the user have a specific permission?"
#       # Simplest possible answer: Yes, always
#       return self.is_admin

#   def has_module_perms(self, app_label):
#       "Does the user have permissions to view the app `app_label`?"
#       # Simplest possible answer: Yes, always
#       return True

#   @property
#   def is_staff(self):
#       "Is the user a member of staff?"
#       # Simplest possible answer: All admins are staff
#       return self.is_admin