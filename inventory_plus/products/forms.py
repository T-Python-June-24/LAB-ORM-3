from django import forms
from .models import Product
from suppliers.models import Supplier
from categories.models import Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    suppliers = forms.ModelMultipleChoiceField(
    queryset= Supplier.objects.all(),
    widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Product
        fields = ['name', 'category', 'suppliers', 'description', 'price', 'stock_quantity', 'expiry_date', 'image']  #pic
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
