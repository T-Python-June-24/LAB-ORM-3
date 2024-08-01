from django import forms
from categories.models import Category

# Create the form class.
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
