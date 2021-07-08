import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drmozzarella.settings")
django.setup()

from products.models import Product, ProductCategory, Category, Menu, Image, Option, Nutrition
from events.models   import CategoryEvent, ProductEvent
from orders.models   import OrderStatus, ItemStatus

PATH = '/Users/hj/Downloads/drmozza_db'
CSV_PATH_MENU            = os.path.join(PATH, 'menus.csv')
CSV_PATH_PRODUCT         = os.path.join(PATH, 'products.csv')
CSV_PATH_NUTRITION       = os.path.join(PATH, 'nutritions.csv')
CSV_PATH_PRODUCTEVENT    = os.path.join(PATH, 'product_events.csv')
CSV_PATH_PRODUCTCATEGORY = os.path.join(PATH, 'products_categories.csv')
CSV_PATH_OPTION          = os.path.join(PATH, 'options.csv')
CSV_PATH_IMAGE           = os.path.join(PATH, 'images.csv')
CSV_PATH_CATEGORYEVENT   = os.path.join(PATH, 'category_events.csv')
CSV_PATH_CATEGORY        = os.path.join(PATH, 'categories.csv')
CSV_PATH_ORDERSTATUS     = os.path.join(PATH, 'order_status.csv')
CSV_PATH_ITEMSTATUS      = os.path.join(PATH, 'item_status.csv')

with open(CSV_PATH_MENU) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Menu.objects.create(
            name = row[1]
        )

with open(CSV_PATH_CATEGORY) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Category.objects.create(
            menu        = Menu.objects.get(id=row[4]),
            name        = row[1],
            image_url   = row[2],
            description = row[3]
        )

with open(CSV_PATH_NUTRITION) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Nutrition.objects.create(
            calories            = row[1], 
            total_fat           = row[2],
            saturated_fat       = row[3],
            trans_fat           = row[4],
            cholestrol          = row[5],
            sodium              = row[6],
            total_carbohydrates = row[7],
            dietary_fiber       = row[8],
            sugars              = row[9],
            protein             = row[10], 
            vitamin_a           = row[11],
            vitamin_c           = row[12],
            calcium             = row[13],
            iron                = row[14],
        )

with open(CSV_PATH_PRODUCT) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Product.objects.create(
            name                  = row[1],
            description           = row[2],
            sales                 = row[3],
            stocks                = row[4],
            score                 = row[5],
            thumbnail_image_url   = row[6],
            hover_image_url       = row[7],
            description_image_url = row[8],
            status                = row[9],
            nutrition             = Nutrition.objects.get(id=row[10])
        ) 

with open(CSV_PATH_PRODUCTCATEGORY) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        ProductCategory.objects.create(
            product  = Product.objects.get(id=row[1]),
            category = Category.objects.get(id=row[2])
        )

with open(CSV_PATH_IMAGE) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Image.objects.create(
            product = Product.objects.get(id=row[1]),
            image_url = row[2]
        )

with open(CSV_PATH_OPTION) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        Option.objects.create(
            product = Product.objects.get(id=row[3]),
            weight = row[1],
            price = row[2]
        )

with open(CSV_PATH_CATEGORYEVENT) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        CategoryEvent.objects.create(
            image_url = row[1],
            category = Category.objects.get(id=row[2]),
            title = row[3],
            description = row[4]
        )

with open(CSV_PATH_PRODUCTEVENT) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        ProductEvent.objects.create(
            image_url = row[1],
            product = Product.objects.get(id=row[2])
        )

with open(CSV_PATH_ORDERSTATUS) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        OrderStatus.objects.create(
            status_name = row[1]
        )

with open(CSV_PATH_ITEMSTATUS) as f:
    data = csv.reader(f)
    next(data)

    for row in data:
        ItemStatus.objects.create(
            status_name = row[1]
        )
