from itertools import product

from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory Strength'
    parameter_name = 'IS(<|>)'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('<50', 'Ok')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10' :
            return queryset.filter(inventory__lt=10)
        elif self.value() == '<50' :
            return queryset.filter(inventory__lt=50)

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''

@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    search_fields = ['title']
    # fields = ['slug', 'title'] "fields to include in the form"
    #exclude = ['slug'] #"fields to exclude in the form"
    prepopulated_fields = {
        'slug': ['title']
    }
    # readonly_fields = ['slug'] #"fields that can't be edited just read only"
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} Products were successfully updated',
            messages.SUCCESS
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }

# class OrderItemInLine(admin.StackedInline):
class OrderItemInLine(admin.TabularInline):

    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 4

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInLine]
    list_display = ['id','placed_at','payment_status','customer']
    list_selected_related = ['customer']
    list_per_page = 10


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'user__last_name', 'membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
            'order__id': str(customer.id)
        }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_products_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )

#admin.site.register(models.Promotion)
@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'discount']
