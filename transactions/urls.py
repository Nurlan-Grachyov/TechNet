from rest_framework.routers import DefaultRouter

from transactions.apps import TransactionsConfig
from transactions.views import TransactionViewSet

app_name = TransactionsConfig.name

router = DefaultRouter()
router.register(r"transaction", TransactionViewSet, basename="transaction")
urlpatterns = [] + router.urls
