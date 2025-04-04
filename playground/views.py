from django.shortcuts import render
from django.db import transaction, connection
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, Count
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Products, OrderItem, Customer, Collection, Order
from tags.models import TaggedItems
# Create your views here.

# @transaction.atomic()
def say_hello(request):
    # query_set = Products.objects.all()
    # product = Products.objects.get(pk=1) 
    # exists = Products.objects.filter(pk=0).exists()
    # queryset = Products.objects.filter(unit_price__range=(30,70))
    # queryset = Products.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Products.objects.filter(inventory=F('unit_price'))
    # queryset = Products.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))
    # product1 = Products.objects.order_by('unit_price')[0]
    # product = Products.objects.earliest('unit_price')
    # product = Products.objects.latest('unit_price') 
    # queryset = Products.objects.order_by('unit_price', '-title')
    # queryset = Products.objects.all()[:5]
    # queryset = Products.objects.values('id', 'title', 'collection__title')
    # queryset = Products.objects.filter(id__in = OrderItem.objects.values('product_id').distinct().order_by('title'))
    # queryset = Products.objects.only('id', 'title')
    # queryset = Products.objects.defer('description')
    # queryset = Products.objects.select_related('collection').all()
    # queryset = Customer.objects.annotate(is_new = Value(True))
    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F('first_name'), Value(' '),
    #                    F('last_name'), function='CONCAT')
    # )
    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name= Concat('first_name', Value(' '), 'last_name')
    # )
    #

    # for product in query_set:
        # print(product)
    # content_type = ContentType.objects.get_for_model(Products)
    #
    # queryset = (TaggedItems.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    # ))
    # TaggedItems.objects.get_tags_for(Products, 1)

    # queryset = Products.objects.all()
    # list(queryset)
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Products(pk=1)
    # collection.save()
    # collection.id

    # Collection.objects.create(title='CDS', featured_product_id = 1)

    # Collection.objects.filter(pk=11).update(title="Games", featured_product_id=None)

    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    # Collection.objects.filter(id__gt = 5).delete()
    # collection.delete()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id =  1
    #     order.save()
    #
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    queryset = Products.objects.raw('SELECT * FROM store_products')
    with connection.cursor() as cursor:
        cursor.execute('SELECT title FROM store_products')
        cursor.callproc('get_customer', [1,3,6])




    return render(request, 'hello.html', {'name': 'Mcdave', 'results': list(queryset)})
