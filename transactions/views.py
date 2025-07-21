from rest_framework.viewsets import ModelViewSet

from connections.permissions import IsActiveStaff
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsActiveStaff]
