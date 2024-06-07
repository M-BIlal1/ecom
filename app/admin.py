from django.contrib import admin

# Register your models here.
from app.models import category,subCategory,product
admin.site.register(category)
admin.site.register(subCategory)
admin.site.register(product)