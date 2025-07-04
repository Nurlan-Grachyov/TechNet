from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from connections.models import NetworkNode
from connections.permissions import IsActiveStaff
from connections.serializers import NetworkNodeSerializer


class NetworkNodeViewSet(ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contacts__country']

    def perform_update(self, serializer):
        if 'debt_to_supplier' in serializer.validated_data:
            del serializer.validated_data['debt_to_supplier']
        serializer.save()
