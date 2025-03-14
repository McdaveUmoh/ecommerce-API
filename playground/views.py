from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, Count
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Products, OrderItem, Customer
# Create your views here.

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
    queryset = Customer.objects.annotate(
        # CONCAT
        full_name= Concat('first_name', Value(' '), 'last_name')
    )
    

    # for product in query_set:
        # print(product)

    return render(request, 'hello.html', {'name': 'Mcdave','products': list(queryset)})
