from decimal import Decimal

from rest_framework import serializers

from store.models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "inventory",
            "slug",
            "description",
            "unit_price",
            "price_with_tax",
            "collection",
        ]

    price_with_tax = (
        serializers.SerializerMethodField(method_name="calculate_tax")
    )
    # collection = CollectionSerializer()
    # # Serializer examples
    # price = (
    #     serializers.DecimalField(
    #         max_digits=6,
    #         decimal_places=2,
    #         source="unit_price")
    # )
    collection = (
        serializers.PrimaryKeyRelatedField(
            queryset=Collection.objects.all())
        )
    # collection = serializers.StringRelatedField()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="collection-detail"
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    def validate(self, data):
        return super().validate(data)
