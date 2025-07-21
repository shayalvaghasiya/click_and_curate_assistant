from django.db import models

class Category(models.Model):
    """Represents a pre-defined product category."""
    name = models.CharField(max_length=100, unique=True)
    urls = models.URLField(max_length=1024, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Represents a product fetched from the Amazon API."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    asin = models.CharField(max_length=20, unique=True, help_text="Amazon Standard Identification Number")
    title = models.CharField(max_length=255)
    image_url = models.URLField(max_length=1024)
    
    def __str__(self):
        return self.title

class PinIdea(models.Model):
    """Represents a curated Pin, ready to be posted."""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    ai_title = models.CharField(max_length=255)
    ai_description = models.TextField()
    affiliate_link = models.URLField(max_length=1024)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pin Idea for: {self.product.title}"