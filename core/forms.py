from django import forms
from .models import Product


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
