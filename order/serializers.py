from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from order.models import CartItem
from store.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"

    def validate(self, data):
        validated_data = super().validate(data)
        product: Product = validated_data.get("product")
        quant = product.product_quantity

        try:
            user = self.context.get('request').user
            cart_item = CartItem.objects.get(product=product, cart__user=user)
        except CartItem.DoesNotExist:
            if quant < validated_data.get("product_quantity"):
                raise ValidationError(
                    f"Product more than {quant} cannot be added"
                )
        else:
            if cart_item.product_quantity < quant:
                cart_item.product_quantity = (
                        cart_item.product_quantity + validated_data.get("product_quantity")
                )
                cart_item.save()
            else:
                raise ValidationError(
                    f"Product of {validated_data.get("product_quantity")} cannot be added"
                )

        return super().validate(data)


