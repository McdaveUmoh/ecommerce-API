from django_filters.rest_framework import FilterSet
from .models import Products

class ProductFilters(FilterSet):
    class Meta:
        model = Products
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }