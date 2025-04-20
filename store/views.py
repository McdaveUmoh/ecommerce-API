from pickle import FALSE

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.core.serializers import serialize

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .ProductFilter import ProductFilters
from .models import Products, Collection, OrderItem, Review, Cart, CartItem, Customer
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerialzer, UpdateCartItemSerializer, CustomerSerializer


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilters
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']


    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be '
                                      'deleted because products are associated to it'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Products.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be '
                                      'deleted because products are associated to it'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerialzer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    # def update(self):
    #     return UpdateCartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id= self.kwargs['cart_pk']) \
            .select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be '
    #                                   'deleted because products are associated to it'},
    #                         status= status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status= status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset = Products.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
#
#     # def get_queryset(self):
#     #     return Products.objects.select_related('collection').all()
#     #
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# # class ProductList(APIView):
# #     def get(self, request):
# #         querySet = Products.objects.select_related('collection').all()
# #         serialize = ProductSerializer(
# #             querySet, many=True, context={'request': request})
# #         return Response(serialize.data)
# #
# #     def post(self, request):
# #         serializer = ProductSerializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         print(serializer.validated_data)
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     # lookup_field = 'id'
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Products, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because orders are associated to it'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)

#function based View
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         querySet = Products.objects.select_related('collection').all()
#         serialize = ProductSerializer(
#             querySet, many=True, context={'request': request})
#         return Response(serialize.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(serializer.validated_data)
#         return Response(serializer.data, status= status.HTTP_201_CREATED)
#         if serializer.is_valid():
#              serializer._validated_data
#              return Response('ok')
#          else:
#              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Products, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(serializer.data)
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because orders are associated to it'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('products'))
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because products are associated to it'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)