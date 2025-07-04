from django.db import models
from django.utils.timezone import now

from contacts.models import Contact
from products.models import Product


class NetworkNode(models.Model):
    title = models.CharField(max_length=255)
    contacts = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=now, blank=True)
    level = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.supplier:
            self.level = 0
        elif self.supplier.level == 0:
            self.level = 1
        else:
            self.level = self.supplier.level + 1
        super().save(*args, **kwargs)

    def update_debt(self):
        """Метод для обновления суммы задолженности"""
        self.debt_to_supplier += self.products.price
        self.save(update_fields=['debt_to_supplier'])
