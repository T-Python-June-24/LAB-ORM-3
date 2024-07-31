from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)
