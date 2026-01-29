from django.contrib import admin
from .models import Cart, CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "price_snapshot",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "product__name",
        "cart__user__username",
        "cart__user__email",
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_items",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    inlines = [CartItemInline]

    def total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    total_items.short_description = "Total Items"
