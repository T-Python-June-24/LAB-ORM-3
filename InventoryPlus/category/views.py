from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from category.models import Category


def all_Categories_view(request: HttpRequest):
    category = Category.objects.all()
    return render(request , "allCategory.html" , {"categories": category})

def add_Category_view(request: HttpRequest):
    category = Category.objects.all()
    if request.method == "POST":
        new_Category = Category(name=request.POST['name'], description=request.POST['description'])
        new_Category.save()

    return render(request, "addCategory.html",  {"categories": category})

def delete_Category_view(request:HttpRequest, category_id: int):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect("category:all_Categories_view")


def update_Category_view(request:HttpRequest, category_id: int):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        category.name = request.POST["name"]
        category.description = request.POST["description"]
        category.save()
        return redirect('category:all_Categories_view')
    
    return render("updateCategory.html", {"categories":category})