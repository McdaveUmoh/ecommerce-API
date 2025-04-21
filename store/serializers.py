from decimal import Decimal
from itertools import product
from .signals import order_created
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.db import transaction
from rest_framework import serializers
from .models import Products, Collection, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage


# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ['id', 'title', 'description', 'inventory','price', 'price_with_tax', 'collection', 'images']
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
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'title', 'inventory', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many= True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class AddCartItemSerialzer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Products.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except:
            self.instance = CartItem.objects.create(cart_id= cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model=CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    # customer = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID. ')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic(): #provides a fail safe if the code breaks in transmission
            # print(self.validated_data['cart_id'])
            # print(self.context['user_id'])
            cart_id =  self.validated_data['cart_id']

            customer = Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects \
                                 .select_related('product') \
                                 .filter(cart_id = cart_id)

            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    # unit_price = item.product.unit_price
                    quantity = item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
