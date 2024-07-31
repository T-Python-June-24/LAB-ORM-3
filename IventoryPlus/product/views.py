from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Product
from Category.models import Category
from Supplier.models import Supplier
import os
import csv
from django.http import FileResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
def download_file(request:HttpRequest):
    file_path = settings.STATICFILES_DIRS[0] / 'file/product.csv'
    return FileResponse(open(file_path, 'rb'), content_type='text/csv', as_attachment=True, filename='product.csv')





def Add_product(request: HttpRequest):
   if request.method == 'POST':
        name = request.POST.get('Name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        supplier_ids = request.POST.getlist('supplier')
        status = request.POST.get('Status') == 'True'
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        expiration = request.POST.get('expiration')
        image = request.FILES.get('image')

        expiration_date = expiration if expiration else None
        new_product = Product(
            Name_Product=name,
            Description_product=description,
            Status_Product=status,
            Quantity_Product=quantity,
            Price_Product=price,
            Expiration_date=expiration_date,
            Images_Product=image
        )

        if category_id:
            new_product.Category_product = Category.objects.get(pk=category_id)
        if supplier_ids:
            suppliers = Supplier.objects.filter(pk__in=supplier_ids)
            new_product.save()  
            new_product.Supplier_product.set(suppliers) 

       
        new_product.save()
        messages.success(request , "done Add product")
        from django.core.mail import send_mail
        subject = f'The  product is about to expire'
        message = "maldfhsfd"
        from_email = settings.EMAIL_HOST_USER
        to_email = 'naif.n115811@gmail.com'
        send_mail(subject, message, from_email, [to_email])
        return redirect('Manger:manger_product')
def views_product(request:HttpRequest):
    view_product = Product.objects.all().select_related('Category_product')
    return render(request , 'index.html' , {'product':view_product})
def update_product(request:HttpRequest , product_id):
    up_product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        up_product.Name_Product = request.POST['Name']
        up_product.Status_Product = request.POST['Status']
        up_product.Quantity_Product = request.POST['quantity']
        up_product.Price_Product = request.POST['price']
        expiration = request.POST['expiration']
        up_product.Description_product = request.POST['description']
        category_id = request.POST['category']
        up_product.Expiration_date = expiration if expiration else None
        if category_id:
            up_product.Category_product = Category.objects.get(pk = category_id)
        supplier_ids = request.POST.getlist('supplier')  
        if supplier_ids:
            suppliers = Supplier.objects.filter(pk__in=supplier_ids)
            up_product.Supplier_product.set(suppliers)
        if 'image' in request.FILES:up_product.Images_Product = request.FILES['image']
        up_product.save()
        messages.success(request , "done update product")
        return redirect('Manger:manger_product')
    return render(request , 'product/update_product.html' )
def delete(request:HttpRequest , product_id):
    del_product = Product.objects.get(pk=product_id)
    if del_product.Images_Product:
        if os.path.isfile(del_product.Images_Product.path):
            os.remove(del_product.Images_Product.path)
    del_product.delete()
    messages.success(request , "done delete product")
    return redirect('Manger:manger_product')
def detail_product(request:HttpRequest , product_id):
    det_product = Product.objects.get(pk=product_id)
    return render(request , 'product/detail_product.html',{'product': det_product})