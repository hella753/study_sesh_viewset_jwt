from django.db.models import F
from django.db.models.functions import Round
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import CartItem
from order.serializers import CartItemSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = CartItem.objects.annotate(
            total_price=Round(
                F("product_quantity") * F("product__product_price")
            )
        ).filter(cart__user_id=self.request.user.id)
        return queryset.select_related("product")
