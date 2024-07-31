from django import forms
from .models import Product

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()