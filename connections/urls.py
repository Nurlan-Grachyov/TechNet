from rest_framework.routers import DefaultRouter

from connections.apps import ConnectionsConfig
from connections.views import NetworkNodeViewSet

app_name = ConnectionsConfig.name
router = DefaultRouter()
router.register(r"network", NetworkNodeViewSet, basename="network")
urlpatterns = [] + router.urls
