from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    shipping_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
