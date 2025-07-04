from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from connections.models import NetworkNode
from contacts.models import Contact
from django.utils.safestring import mark_safe
from django.urls import reverse


class CityFilter(SimpleListFilter):
    title = _("City")
    parameter_name = "city"

    def lookups(self, request, model_admin):
        cities = set([contact.city for contact in Contact.objects.all()])
        return [(city, city) for city in sorted(cities)]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(contacts__city=value)
        return queryset


def clear_debts(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    updated_count = queryset.update(debt_to_supplier=0)
    messages.success(
        request, f"Успешно очищены задолженности у {updated_count} объектов."
    )


clear_debts.short_description = _("Очистить задолженности выбранных объектов")


#
@admin.register(NetworkNode)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ["title", "products_list", "supplier_title", "link_to_supplier"]
    search_fields = ["title"]
    ordering = ["-id"]
    list_filter = [CityFilter]
    actions = [clear_debts]

    def link_to_supplier(self, obj):
        if obj.supplier:
            url = f"supplier/{obj.supplier.id}/"
            return url
        else:
            return None

    link_to_supplier.short_description = _("Ссылка поставщика")
    link_to_supplier.allow_tags = True

    def products_list(self, obj):
        return ", ".join([prod.name for prod in obj.products.all()])

    products_list.short_description = _("Список продуктов")

    def supplier_title(self, obj):
        return str(obj.supplier) if obj.supplier else "-"

    supplier_title.short_description = _("Название поставщика")
