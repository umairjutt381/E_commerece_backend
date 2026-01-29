from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "sku",
        "price",
        "stock_quantity",
        "status",
        "category",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "description",
    )

    list_editable = (
        "price",
        "stock_quantity",
        "status",
    )

    ordering = ("-created_at",)
