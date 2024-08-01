from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import Category
from django. contrib import messages
from products.models import Product
# Create your views here.
def all_categories(request:HttpRequest):
    categories=Category.objects.all()
    return render(request,"categories/category.html",{"categories":categories})

def add_category(request:HttpRequest):
    try:
        if request.method=="POST":
            name=request.POST["name"]
            new_category=Category(name=name)
            new_category.save()
            messages.success(request,"the category added successfully",'success')
    except Exception as e:
        messages.error(request,"the category could't added","error")

    return render(request,"categories/add_category.html")

def delete_category(request,category_id):
    try:
        category=Category.objects.get(pk=category_id)
        product_update=Product.objects.filter(category=category)
        product_update.update(category=None)
        category.delete()
        messages.success(request,"the product deleted successfully","success")
    except Exception as e:
        messages.error(request,"there is something went wrong could't delete category ","error")
    return redirect("categories:all_categories")
def update_category(request:HttpRequest,category_id):
    category=Category.objects.get(pk=category_id)
    try:
        if request.method=="POST":
            category.name=request.POST["name"]
            category.save()
            messages.success(request,"the categeory is updated now ","success")
    except Exception as e:
        messages.error(request,"the category could't updated","error")
        return redirect("categories:all_categories")
    return render(request,"categories/update_category.html",{"category":category})
    
def related_products(request:HttpRequest,category_id)->render:
    category=Category.objects.get(pk=category_id)
    products=Product.objects.filter(category=category)
    return render (request,"categories/related_products.html",{"category":category,"products":products})