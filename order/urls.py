from rest_framework.routers import DefaultRouter
from .views import CartViewSet

app_name = "order"
router = DefaultRouter()
router.register(r'orders', CartViewSet, basename='order')

urlpatterns = router.urls