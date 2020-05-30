from django.db import models
from django.contrib.auth import get_user_model


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
