from django import forms
from suppliers.models import Supplier

# Create the form class.
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
