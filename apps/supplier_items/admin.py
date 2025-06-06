"""Supplier items admin."""
from django.contrib import admin
from apps.supplier_items.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""
    list_display = ['name', 'type', 'price', 'category', 'created_at']
    list_filter = ['type', 'category']
    search_fields = ['name', 'description']
