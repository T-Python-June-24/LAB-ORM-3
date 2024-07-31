from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address', 'website', 'image']
        widgets = {
            'last_active': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SupplierSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')