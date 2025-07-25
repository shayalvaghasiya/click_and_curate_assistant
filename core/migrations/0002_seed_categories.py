# Generated by Django

from django.db import migrations

# Define our list of pre-defined categories
CATEGORIES = [
    "Home Office Decor",
    "Kitchen Gadgets",
    "Fitness & Wellness",
    "Sustainable Living",
    "Pet Supplies",
    "DIY & Crafting",
    "Tech & Gadgets",
    "Outdoor & Adventure",
    "Fashion & Accessories",
    "Beauty & Skincare",
]

def add_category_data(apps, schema_editor):
    """
    This function is called when we run the migration.
    It gets the Category model and creates our pre-defined categories.
    """
    Category = apps.get_model('core', 'Category')
    for category_name in CATEGORIES:
        # This creates a new category and saves it to the database.
        # get_or_create prevents creating duplicates if we run it again.
        Category.objects.get_or_create(name=category_name)

def remove_category_data(apps, schema_editor):
    """
    This function is called if we ever need to "un-apply" or reverse the migration.
    It safely deletes the categories we created.
    """
    Category = apps.get_model('core', 'Category')
    for category_name in CATEGORIES:
        try:
            category_instance = Category.objects.get(name=category_name)
            category_instance.delete()
        except Category.DoesNotExist:
            # If the category doesn't exist, do nothing.
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # This tells Django to run our custom Python functions.
        migrations.RunPython(add_category_data, remove_category_data),
    ]