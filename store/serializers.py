from decimal import Decimal
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from rest_framework import serializers
from .models import Products, Collection, Review


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'title', 'inventory','price', 'price_with_tax', 'collection']
        # fields = '__all__'

    # class ProductSerializer(serializers.Serializer):

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    price =  serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset= Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )

    def calculate_tax(self, product: Products):
        return product.unit_price * Decimal(1.1)

    # def create(self, validated_data):
    #     product = Products(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    #
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'product', 'description']