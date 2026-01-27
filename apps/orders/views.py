from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Order, OrderItem
from .serializers import OrderSerializer
from apps.cart.models import Cart


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            cart = Cart.objects.select_for_update().get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

        if not cart.items.exists():
            return Response({"error": "Your cart is empty"}, status=400)

        shipping_address = request.data.get("shipping_address")
        if not shipping_address:
            return Response({"error": "Shipping address is required"}, status=400)

        # Create order first
        order = Order.objects.create(
            user=request.user,
            total_amount=0,
            shipping_address=shipping_address,
            order_status="pending",
            payment_status="pending",
        )

        total_amount = 0

        for item in cart.items.select_related("product"):
            product = item.product

            if item.quantity > product.stock_quantity:
                raise Exception(f"Not enough stock for {product.name}")

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price,
            )

            product.stock_quantity -= item.quantity
            product.save()

            total_amount += product.price * item.quantity

        order.total_amount = total_amount
        order.save()

        cart.items.all().delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_amount": str(total_amount),
            },
            status=status.HTTP_201_CREATED,
        )


class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_staff:
            orders = Order.objects.all().order_by("-created_at")
        else:
            orders = Order.objects.filter(user=user).order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if not request.user.is_staff and order.user != request.user:
            raise PermissionDenied("You do not have permission to view this order")

        serializer = OrderSerializer(order)
        return Response(serializer.data)
