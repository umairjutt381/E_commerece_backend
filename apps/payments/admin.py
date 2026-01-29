from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "stripe_payment_intent_id",
        "amount",
        "currency",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "stripe_payment_intent_id",
        "order__id",
        "order__user__username",
        "order__user__email",
    )

    readonly_fields = (
        "order",
        "stripe_payment_intent_id",
        "amount",
        "currency",
        "created_at",
    )

    ordering = ("-created_at",)
