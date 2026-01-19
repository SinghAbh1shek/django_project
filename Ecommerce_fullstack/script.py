import csv
import requests
from django.core.files.base import ContentFile
from accounts.models import Shopkeeper
from products.models import *
from django.contrib.auth.models import User
from decimal import Decimal


import random
import string
from datetime import datetime



def generate_bmp_id():
    year = datetime.now().year
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BMP-{year}-{random_part}"



def generate_aadhaar_number():
    return ''.join(random.choices(string.digits, k=12))

def generate_gst_number():
    state_code = random.randint(1, 37)
    state_code = f"{state_code:02d}"

    pan_part = ''.join(random.choices(string.ascii_uppercase, k=5)) + \
               ''.join(random.choices(string.digits, k=4)) + \
               random.choice(string.ascii_uppercase)

    entity = random.choice(string.digits)
    checksum = random.choice(string.digits + string.ascii_uppercase)

    return f"{state_code}{pan_part}{entity}Z{checksum}"



csv_path = 'dataset.csv'
MAX_PRODUCTS_PER_CATEGORY = 10

def get_or_create_category(name, parent = None):
    if not name:
        return None
    
    category, _ = Category.objects.get_or_create(category_name = name.strip(), parent = parent)

    return category

def download_image(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return ContentFile(response.content)




def run():
    category_count = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
            
                cat1 = get_or_create_category(row['category_1'])
                cat2 = get_or_create_category(row['category_2'], parent=cat1)
                cat3 = get_or_create_category(row['category_3'], parent=cat2)

                category = cat3 or cat2 or cat1
                if not category:
                    print("skipped no category")
                    continue
                
                current_count = category_count.get(category.id, 0)
                if current_count >= MAX_PRODUCTS_PER_CATEGORY:
                    print("limit reached")
                    continue

                product, created = Product.objects.get_or_create(
                    title = row['title'],
                    defaults={
                        'description': row.get('description', ''),
                        'highlight': row.get('highlights', ''),
                        'product_rating': safe_float(row.get('product_rating')),
                        'mrp': clean_price(row.get('mrp')),
                        'category': category,
                    }
                )

                if created:
                    category_count[category.id] = current_count + 1

                seller_name = row.get('seller_name', 'default_name')
                
                username = username = seller_name.replace(" ", "_").lower()
                user, _ = User.objects.get_or_create(
                    username = username
                )


                shopkeeper, _ = Shopkeeper.objects.get_or_create(
                    user = user,
                    defaults={
                        'shop_name':seller_name,
                        'verification_status': 'verified',
                        "gst_number": generate_gst_number(),
                        "adhar_number": generate_aadhaar_number(),
                        "bmp_id": generate_bmp_id(),
                    }    
                )

                VendorProduct.objects.get_or_create(
                    shopkeeper = shopkeeper,
                    product = product,
                    defaults={
                        'vendor_rating': safe_float(row.get('seller_rating')),
                        'vendor_selling_price': clean_price(row.get('selling_price')),
                        'is_active': True
                    }
                )

                image_links = row.get('image_links', '')
                if image_links:
                    for idx, img_url in enumerate(image_links.split(',')):
                        if not ProductImage.objects.filter(product=product).exists():
                            try:
                                image_content = download_image(img_url.strip())
                                ProductImage.objects.create(
                                    product = product,
                                    image = ContentFile(
                                        image_content.read(),
                                        name=f"product_{product.id}_{idx}.jpg"
                                    )
                                )
                            except Exception as e:
                                print(f'image failed: {img_url} -> {e}')
                print(f'Imported: {product.title}')
            except Exception as e:
                print(f"failed row: {row.get('title')} -> {e}")

def safe_float(value):
    try:
        return float(value)
    except:
        return None
    

def clean_price(value):
    if not value:
        return Decimal('0.00')
    return Decimal(value.replace('₹', '').replace(',', '').strip())