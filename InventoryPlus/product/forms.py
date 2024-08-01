from django import forms
from django.forms import DateInput

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'expiry_date': DateInput(attrs={'type': 'date'}),
        }
