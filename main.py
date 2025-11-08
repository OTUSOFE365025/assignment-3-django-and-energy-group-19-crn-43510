############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# setup django environment
import django
django.setup()

# Import your models for use in your script
from db.models import *

############################################################################
## START OF APPLICATION
############################################################################

# populate with products
products = [
    {"upc_code": "12345678910", "name": "apple", "price": "1.99"},
    {"upc_code": "12345678911", "name": "banana", "price": "2.99"},
    {"upc_code": "12345678912", "name": "orange", "price": "4.99"},
    {"upc_code": "12345678913", "name": "grapes", "price": "7.99"},
    {"upc_code": "12345678914", "name": "milk", "price": "5.00"},
]

for p in products:
    Product.objects.create(
        upc_code=p["upc_code"], 
        name=p["name"], 
        price=p["price"]
        )

print("products have been created and added to database")