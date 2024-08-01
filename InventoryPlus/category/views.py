from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Category
from .forms import CategoryForm
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def add_view(request: HttpRequest) -> HttpResponse:
    category_form = CategoryForm()
    if request.method == 'POST':
        try:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Added category successfully", "alert-success")
                return redirect('category:all_view')
        except Exception as e:
            print(e)
            messages.error(request, "Couldn't add category", "alert-danger")
    else:
        print("not valid form", category_form.errors)
    return render(request, 'category/add.html', {'category_form': category_form})


# Edit not functional
def edit_view(request: HttpRequest, category_id: int) -> HttpResponse:
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
        else:
            print("not valid form", category_form.errors)
        return redirect('category:all_view')
    return render(request, 'category/edit.html', {"category": category})


def all_view(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(categories, 2)
    categories_page = paginator.get_page(page_number)
    return render(request, 'category/all.html', {"categories": categories, "categories_page": categories_page})


def detail_view(request: HttpRequest, category_id: int) -> HttpResponse:
    category = Category.objects.get(id=category_id)
    return render(request, 'category/detail.html', {'category': category})


def delete_view(request: HttpRequest, category_id: int) -> HttpResponse:
    try:
        category = Category.objects.get(pk=category_id)
        category.delete()
        messages.success(request, "Deleted category successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't delete category", "alert-danger")
    return redirect('category:all_view')
