# core/migrations/0002_seed_initial_data.py
from django.db import migrations

# The full list of categories and their bestseller URLs
CATEGORIES_DATA = {
    "Amazon Launchpad": "https://www.amazon.in/gp/bestsellers/boost",
    "Amazon Renewed": "https://www.amazon.in/gp/bestsellers/amazon-renewed",
    "Apps & Games": "https://www.amazon.in/gp/bestsellers/mobile-apps",
    "Baby Products": "https://www.amazon.in/gp/bestsellers/baby",
    "Bags, Wallets and Luggage": "https://www.amazon.in/gp/bestsellers/luggage",
    "Beauty": "https://www.amazon.in/gp/bestsellers/beauty",
    "Books": "https://www.amazon.in/gp/bestsellers/books",
    "Car & Motorbike": "https://www.amazon.in/gp/bestsellers/automotive",
    "Clothing & Accessories": "https://www.amazon.in/gp/bestsellers/apparel",
    "Computers & Accessories": "https://www.amazon.in/gp/bestsellers/computers",
    "Electronics": "https://www.amazon.in/gp/bestsellers/electronics",
    "Garden & Outdoors": "https://www.amazon.in/gp/bestsellers/garden",
    "Gift Cards": "https://www.amazon.in/gp/bestsellers/gift-cards",
    "Grocery & Gourmet Foods": "https://www.amazon.in/gp/bestsellers/grocery",
    "Health & Personal Care": "https://www.amazon.in/gp/bestsellers/hpc",
    "Home & Kitchen": "https://www.amazon.in/gp/bestsellers/kitchen",
    "Home Improvement": "https://www.amazon.in/gp/bestsellers/home-improvement",
    "Industrial & Scientific": "https://www.amazon.in/gp/bestsellers/industrial",
    "Jewellery": "https://www.amazon.in/gp/bestsellers/jewelry",
    "Kindle Store": "https://www.amazon.in/gp/bestsellers/digital-text",
    "Movies & TV Shows": "https://www.amazon.in/gp/bestsellers/dvd",
    "Music": "https://www.amazon.in/gp/bestsellers/music",
    "Musical Instruments": "https://www.amazon.in/gp/bestsellers/musical-instruments",
    "Office Products": "https://www.amazon.in/gp/bestsellers/office-products",
    "Pet Supplies": "https://www.amazon.in/gp/bestsellers/pet-supplies",
    "Shoes & Handbags": "https://www.amazon.in/gp/bestsellers/shoes",
    "Software": "https://www.amazon.in/gp/bestsellers/software",
    "Sports, Fitness & Outdoors": "https://www.amazon.in/gp/bestsellers/sports",
    "Toys & Games": "https://www.amazon.in/gp/bestsellers/toys",
    "Video Games": "https://www.amazon.in/gp/bestsellers/videogames",
    "Watches": "https://www.amazon.in/gp/bestsellers/watches",
}

def seed_data(apps, schema_editor):
    """Seeds the database with the initial category data."""
    Category = apps.get_model('core', 'Category')
    for name, url in CATEGORIES_DATA.items():
        # update_or_create finds a category by name and updates it,
        # or creates it if it doesn't exist. This is a very robust method.
        Category.objects.update_or_create(name=name, defaults={'urls': url})

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_category_urls'),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]