from django.shortcuts import render 
from django.http import HttpRequest
from product.models import Product
from Category.models import Category

# Create your views here.

def home(request:HttpRequest):
    views_product = Product.objects.all()
    return render(request , 'pages/index.html' , {'views_product':views_product})
def pay_product(request:HttpRequest , product_id):
    views_product = Product.objects.all()
    get_product = Product.objects.get(pk = product_id)
    Quantity = get_product.Quantity_Product
    if Quantity>0:
        Quantity = Quantity - 1
        get_product.Quantity_Product = Quantity
        get_product.save()
    for prodect in views_product:
        if prodect.Quantity_Product == 0:
            prodect.Status_Product = 0
            prodect.save() 
    Notifications = True
    return render(request , 'pages/index.html' , {'Notifications':Notifications ,'views_product':views_product})
def views_product_category(request:HttpRequest , id_Category):
    get_category = Category.objects.get(pk = id_Category)
    get_product = Product.objects.filter(Category_product_id = id_Category)
    return render(request , 'pages/all_product.html' , {'product':get_product , 'category':get_category})