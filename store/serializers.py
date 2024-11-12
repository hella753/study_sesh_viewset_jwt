from django.core.mail import EmailMessage
from rest_framework import serializers
from store.models import Category, Product, ShopReviews, ProductReviews, ProductTags


class ContactSerializer(serializers.Serializer):
    sender_name = serializers.CharField(max_length=100)
    sender_email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        sender_name = self.validated_data["sender_name"]
        sender_email = self.validated_data["sender_email"]
        message = self.validated_data["message"]
        mail = EmailMessage(
            f"New Message from {sender_name}",
            body=message,
            from_email=sender_email,
            to=["kristigaphrindashvili@gmail.com"],
        )
        mail.reply_to = [sender_email]
        mail.send(fail_silently=False)


class ProductTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTags
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["lft", "rght", "tree_id", "level", "category_name"]


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        exclude = ["product"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["product_name"]


class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReviews
        fields = "__all__"


