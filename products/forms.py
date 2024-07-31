from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'supplier', 'quantity', 'expiry_date', 'low_stock_threshold']

class ProductSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', 'Sort By'),
            ('name_asc', 'Name (A-Z)'),
            ('name_desc', 'Name (Z-A)'),
            ('quantity_high', 'Quantity (High to Low)'),
            ('quantity_low', 'Quantity (Low to High)'),
            ('price_high', 'Price (High to Low)'),
            ('price_low', 'Price (Low to High)'),
            ('expiry', 'Expiry Date (Soonest)'),
        ],
        required=False
    )
    stock_status = forms.ChoiceField(
        choices=[
            ('', 'All Stock Status'),
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        required=False
    )