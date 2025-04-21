from uuid import uuid4
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CASCADE


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    class Meta:
        permissions = [
            ('cancel_promotion', 'can cancel promotion')
        ]

    def __str__(self):
        return self.description

class Collection(models.Model): 
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Products(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators= [MinValueValidator(1)]
    )
    inventory = models.IntegerField(validators= [MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete= models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, related_name='products', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Customer(models.Model):
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'

    MEMBERSHIP_CHOICE = [
        (BRONZE_MEMBERSHIP, 'BRONZE'),
        (SILVER_MEMBERSHIP, 'SILVER'),
        (GOLD_MEMBERSHIP, 'GOLD')
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICE, default=BRONZE_MEMBERSHIP)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return  f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        permissions = [
            ('view_history', 'can view history')
        ]

class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETED = 'C'
    STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length= 1, choices=PAYMENT_STATUS_CHOICES, default= STATUS_PENDING )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'can cancel order')
        ]

    def __str__(self):
        return self.payment_status


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    
class Cart(models.Model):
    id = models.UUIDField(primary_key= True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
