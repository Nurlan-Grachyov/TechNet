from rest_framework import serializers

from connections.models import NetworkNode
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from products.models import Product
from products.serializers import ProductSerializer


class NetworkNodeSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()
    products = ProductSerializer(many=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=NetworkNode.objects.all(), allow_null=True)

    class Meta:
        model = NetworkNode
        fields = [
            'title',
            'contacts',
            'products',
            'supplier',
            'debt_to_supplier',
            'level'
        ]
        read_only_fields = ('debt_to_supplier', 'level')

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')

        network_node = NetworkNode.objects.create(**validated_data)

        contact = Contact.objects.create(**contacts_data)
        network_node.contacts = contact
        network_node.save()

        for product_data in products_data:
            product = Product.objects.create(**product_data)
            network_node.products.add(product)

        return network_node

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.supplier = validated_data.get('supplier', instance.supplier)

        contacts_data = validated_data.pop('contacts', {})
        if contacts_data:
            contact_serializer = ContactSerializer(instance.contacts, data=contacts_data)
            if contact_serializer.is_valid():
                contact_serializer.save()

        products_data = validated_data.pop('products', [])
        instance.products.clear()
        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            instance.products.add(product)

        instance.save()
        return instance
