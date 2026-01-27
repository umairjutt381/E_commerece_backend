from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.permissions import IsCustomer
from .models import Cart, CartItem
from apps.products.models import Product


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsCustomer]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        data = []
        for item in cart.items.all():
            data.append({
                'id': item.id,
                'product': item.product.name,
                'quantity': item.quantity,
                'price': item.price_snapshot
            })
        return Response(data)

    def create(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(
            Product, id=request.data.get('product_id')
        )
        qty = int(request.data.get('quantity', 1))
        if qty > product.stock_quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=400
            )
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': 0,
                'price_snapshot': product.price
            }
        )
        if cart_item.quantity + qty > product.stock_quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=400
            )
        cart_item.quantity += qty
        cart_item.price_snapshot = product.price
        cart_item.save()
        return Response({
            'message': 'Cart updated',
            'product': product.name,
            'quantity': cart_item.quantity,
            'price_snapshot': cart_item.price_snapshot
        })
    def destroy(self, request, pk=None):
        CartItem.objects.filter(id=pk).delete()
        return Response({'message': 'Removed'})