from django import forms
from .models import Product, OrderItem, Address


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',
                  'image',
                  'price',
                  'label',
                  'description_short',
                  'description_long',
                  'category',)


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('apartment_address',
                  'street_address',
                  'country',
                  'zip',)
