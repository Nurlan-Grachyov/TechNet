from platform import release

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from connections.permissions import IsActiveStaff
from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaff]

    def create(self, request, *args, **kwargs):
        try:
            obj, created = Product.objects.get_or_create(
                name=request.data["name"],
                model=request.data["model"],
                release_date=request.data["release_date"]
            )

            serializer = self.get_serializer(obj)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
                            headers=headers)

        except Exception as e:
            return Response({"detail": f"Ошибка при создании продукта: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
