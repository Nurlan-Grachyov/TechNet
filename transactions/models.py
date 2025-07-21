from django.db import models

from connections.models import NetworkNode
from products.models import Product


class Transaction(models.Model):
    """Запись транзакций покупок (приобретений товаров)"""
    buyer = models.ForeignKey(NetworkNode, on_delete=models.PROTECT, related_name="purchases")
    seller = models.ForeignKey(NetworkNode, on_delete=models.PROTECT, related_name="sales")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        """Общая стоимость сделки"""
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.buyer.title} купил у {self.seller.title}: {self.product.name} x {self.quantity}"

    def process_transaction(self):
        """Обрабатываем сделку и обновляем задолженность"""
        print("process_transaction")
        amount = self.total_amount
        self.buyer.debt_to_supplier += amount
        self.buyer.save()
