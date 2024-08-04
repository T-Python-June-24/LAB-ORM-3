from django import forms
from .models import Product, Category, Supplier
import imghdr



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'suppliers': forms.SelectMultiple(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 0, 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required.')
        return name

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required.')
        return category

    def clean_suppliers(self):
        suppliers = self.cleaned_data.get('suppliers')
        if not suppliers:
            raise forms.ValidationError('This field is required.')
        return suppliers

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError('This field is required.')
        if price < 0:
            raise forms.ValidationError('Price must be a positive number.')
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise forms.ValidationError('This field is required.')
        if stock < 0:
            raise forms.ValidationError('Stock must be a non-negative integer.')
        return stock

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and self.instance.pk:
            return self.instance.image
        if not image:
            raise forms.ValidationError('This field is required.')
        
        try:
            image_type = imghdr.what(image)
            if image_type not in ['jpeg', 'png', 'gif']:
                raise forms.ValidationError('Only JPEG, PNG, and GIF images are allowed.')
        except:
            raise forms.ValidationError('Invalid image.')

        return image

    




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required.')
        if self.instance.pk is None and Category.objects.filter(name=name).exists():
            raise forms.ValidationError('A category with this name already exists.')
        return name



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required.')
        if self.instance.pk is None and Supplier.objects.filter(name=name).exists():
            raise forms.ValidationError('A supplier with this name already exists.')
        return name

    def clean_contact_email(self):
        contact_email = self.cleaned_data.get('contact_email')
        if not contact_email:
            raise forms.ValidationError('This field is required.')
        return contact_email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('This field is required.')
        return phone_number

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise forms.ValidationError('This field is required.')
        return address







class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
