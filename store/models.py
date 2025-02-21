from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model): 
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True, related_name='+')
    
class Products(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete= models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name='products')

class Customer(models.Model):
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'

    MEMBERSHIP_CHOICE = [
        (BRONZE_MEMBERSHIP, 'BRONZE'),
        (SILVER_MEMBERSHIP, 'SILVER'),
        (GOLD_MEMBERSHIP, 'GOLD')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICE, default=BRONZE_MEMBERSHIP)
    
    class Meta:  
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
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
    payment_status = models.CharField(max_length= 1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_CHOICES )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

