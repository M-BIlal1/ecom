from app.models import product, category, subCategory
from datetime import datetime

# Define the data for the categories
categories_data = [
    {'name': 'SPORTSWEAR'},
    {'name': 'MENS'},
    {'name': 'WOMENS'},
    {'name': 'KIDS'},
    {'name': 'FASHION'},
    {'name': 'HOUSEHOLDS'},
    {'name': 'INTERIORS'},
    {'name': 'CLOTHING'},
    {'name': 'BAGS'},
    {'name': 'SHOES'}
]

# Create Category instances and save them to the database
for category_info in categories_data:
    category = category.objects.create(**category_info)
    category.save()

print("Categories added successfully.")




# Define the data for the products
products_data = [
    {'image': 'static/images/home/outline.png', 'name': 'bizaibo', 'price': 120, 'date': datetime(2024, 5, 7),
     'category_id': 1, 'subcategory_id': 2},
    {'image': 'static/images/home/product1.jpg', 'name': 'Woman Sunglass', 'price': 12, 'date': datetime(2024, 5, 7),
     'category_id': 1, 'subcategory_id': 1},
    {'image': 'static/images/home/product3.jpg', 'name': 'Man Sunglass', 'price': 13, 'date': datetime(2024, 5, 7),
     'category_id': 1, 'subcategory_id': 5},
    {'image': 'static/images/home/product4.jpg', 'name': 'Formal Shirt', 'price': 14, 'date': datetime(2024, 5, 7),
     'category_id': 3, 'subcategory_id': 5},
    {'image': 'static/images/home/product5.jpg', 'name': 'T-shirt Black', 'price': 15, 'date': datetime(2024, 5, 7),
     'category_id': 8, 'subcategory_id': 11},
    {'image': 'static/images/home/product5.jpg', 'name': 'Astüs Gamming Laptop With 1tb rom', 'price': 11, 'date': datetime(2024, 5, 7),
     'category_id': 2, 'subcategory_id': 14},
    {'image': 'static/images/home/product2.jpg', 'name': 'Mi Powerbank 10000mAh', 'price': 21, 'date': datetime(2024, 5, 7),
     'category_id': 6, 'subcategory_id': 14},
    {'image': 'static/images/home/product2.jpg', 'name': 'Mi Powerbank 10000mAh', 'price': 21, 'date': datetime(2024, 5, 7),
     'category_id': 6, 'subcategory_id': 14},
    {'image': 'static/images/home/product1.jpg', 'name': 'Oneplus 6t Cover', 'price': 22, 'date': datetime(2024, 5, 7),
     'category_id': 10, 'subcategory_id': 14},
    {'image': 'static/images/home/product3.jpg', 'name': 'Iphone 10 Stylish Case and Cover', 'price': 33, 'date': datetime(2024, 5, 7),
     'category_id': 1, 'subcategory_id': 14}
]

# Create Product instances and save them to the database
for product_info in products_data:
    category_id = product_info.pop('category_id')
    subcategory_id = product_info.pop('subcategory_id')
    category = category.objects.get(pk=category_id)
    subcategory = subcategory.objects.get(pk=subcategory_id)
    product_info['category'] = category
    product_info['subcategory'] = subcategory
    product = product.objects.create(**product_info)
    product.save()

print("Products added successfully.")


subcategories_data = [
    {'name': 'NIKE', 'category_id': 1},
    {'name': 'UNDER ARMOUR', 'category_id': 1},
    {'name': 'ADIDAS', 'category_id': 1},
    {'name': 'PUMA', 'category_id': 1},
    {'name': 'ASICS', 'category_id': 1},
    {'name': 'FENDI', 'category_id': 2},
    {'name': 'GUESS', 'category_id': 2},
    {'name': 'VALENTINO', 'category_id': 2},
    {'name': 'DIOR', 'category_id': 2},
    {'name': 'VERSACE', 'category_id': 2},
    {'name': 'ARMANI', 'category_id': 2},
    {'name': 'PRADA', 'category_id': 2},
    {'name': 'DOLCE AND GABBANA', 'category_id': 2},
    {'name': 'CHANEL', 'category_id': 2},
    {'name': 'GUCCI', 'category_id': 2},
    {'name': 'FENDI', 'category_id': 3},
    {'name': 'GUESS', 'category_id': 3},
    {'name': 'VALENTINO', 'category_id': 3},
    {'name': 'DIOR', 'category_id': 3},
    {'name': 'VERSACE', 'category_id': 3}
]

# Create Subcategory instances and save them to the database
for subcategory_info in subcategories_data:
    category_id = subcategory_info.pop('category_id')
    category = category.objects.get(pk=category_id)
    subcategory_info['category'] = category
    subcategory = subcategory.objects.create(**subcategory_info)
    subcategory.save()

print("Subcategories added successfully.")