from rest_framework.viewsets import ModelViewSet

from connections.permissions import IsActiveStaff
from contacts.models import Contact
from contacts.serializers import ContactSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsActiveStaff]