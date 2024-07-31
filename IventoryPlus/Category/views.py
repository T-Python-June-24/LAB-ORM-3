from django.shortcuts import render , redirect
from .models import Category
from product.models import Product
from django.http import HttpRequest
# Create your views here.

def views_Category(request:HttpRequest):
    view_Category = Category.objects.all()
    return render(request , 'Category/views_Category.html' , {'view_category':view_Category})
def add_category(request:HttpRequest):
    if request.method == 'POST':
        new_category = Category(name_Category = request.POST['name_category'] , description_Category = request.POST['description'])
        new_category.save()
        return redirect('Manger:manger_Category')
    return redirect('Manger:manger_Category')

def detail_category(request:HttpRequest , category_id):
    det_category = Category.objects.get(pk = category_id)
    pro_category = Product.objects.filter(Category_product_id=category_id)
    return render(request , "Category/detail_category.html" , {'category':det_category , 'product':pro_category})

def delete_category(request:HttpRequest , category_id):
    del_category = Category.objects.get(pk = category_id)
    del_category.delete()
    return redirect('Category:views_Category')

def update_category(request:HttpRequest , category_id):
    up_category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        up_category.name_Category = request.POST['name_category']
        up_category.description_Category = request.POST['description_caregory']
        up_category.save()
        return redirect('Category:update_category' , category_id)
    return render(request , 'category/update_category.html')
