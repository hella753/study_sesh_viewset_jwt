import django_filters
from store.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['icontains'],
            'product_price': ['lte'],
            'tags': ['exact'],
        }