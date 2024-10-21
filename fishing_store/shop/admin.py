from django.contrib import admin

# Register your models here.

from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'category', 'created_at', 'updated_at')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')