from django.contrib import admin
from .models import Category, Product, PinIdea

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'asin')
    list_filter = ('category',)

@admin.register(PinIdea)
class PinIdeaAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'product__category')
    readonly_fields = ('created_at', 'affiliate_link')