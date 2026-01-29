from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_amount",
        "order_status",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "order_status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "user",
        "total_amount",
        "created_at",
    )

    inlines = [OrderItemInline]

    ordering = ("-created_at",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
    )

    list_filter = (
        "product",
    )

    search_fields = (
        "order__id",
        "product__name",
    )
