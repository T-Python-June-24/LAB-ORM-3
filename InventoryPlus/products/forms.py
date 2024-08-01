from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = "__all__"
         
        widgets = {
            'suppliers': forms.SelectMultiple(attrs={'class': 'select2'}),
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()