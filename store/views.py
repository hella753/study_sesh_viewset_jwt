from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.utils.filtersets import ProductFilter
from store.utils.paginators import CustomPaginator
from store.serializers import *


@method_decorator(cache_page(60*1), name='dispatch')
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = CustomPaginator
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    lookup_field = "slug"
    ordering_fields = ["product_price"]
    ordering = ["product_price"]


    def get_queryset(self):
        if self.action == 'list':
            category_slug = self.request.query_params.get('category')
            if category_slug:
                category = Category.objects.filter(slug=category_slug)
                categories = category.get_descendants(include_self=True)
                queryset = (
                    Product.objects
                    .filter(product_category__in=categories)
                )
            else:
                queryset = (
                    Product.objects.all()
                )
            return queryset.prefetch_related(
                "product_category",
                "tags",
                "product_reviews",
                "product_category__parent"
            )
        elif self.action == 'retrieve':
            return Product.objects.prefetch_related("product_category", "tags")

        return super().get_queryset()


    @action(
        detail=False,
        serializer_class=ContactSerializer,
        methods=["post"],
        url_path="send-email"
    )
    def send_email(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(
        detail=False,
        serializer_class=ShopReviewSerializer,
        url_path="shop-reviews"
    )
    def shop_reviews(self, request):
        queryset = ShopReviews.objects.select_related("user")
        serializer = ShopReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(
        detail=False,
        serializer_class=ProductTagsSerializer,
        url_path="product-tags"
    )
    def product_tags(self, request):
        queryset = ProductTags.objects.all()
        serializer = ProductTagsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(
        detail=False,
        serializer_class=CategorySerializer
    )
    def categories(self, request):
        queryset = Category.objects.select_related("parent")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

