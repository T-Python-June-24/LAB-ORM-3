from django import forms
from suppliers.models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model= Supplier
        fields = "__all__"
         
        widgets = {
            'supplier_name' : forms.TextInput({"class" : "form-control"}),
        }