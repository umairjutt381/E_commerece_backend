from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.users.permissions import IsAdmin

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdmin()]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
