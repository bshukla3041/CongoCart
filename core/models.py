from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField


LABEL_CHOICES = (
    ('SALE', 'sale'),
    ('NEW', 'new'),
    ('PROMOTION', 'promotion')
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=9)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField(upload_to='product')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=5)
    total_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Address(models.Model):
    congo_user = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.congo_user.phone_number)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    congo_user = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.congo_user)


class Order(models.Model):
    buyer = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.buyer)
