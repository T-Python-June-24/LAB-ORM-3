from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Product
from category.models import Category
from supplier.models import Supplier
from .forms import ProductForm
from django.db.models import Count, Avg, Sum, Max, Min


# Create your views here.
def add_view(request: HttpRequest) -> HttpResponse:
    product_form = ProductForm()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        try:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, "Added product successfully", "alert-success")
                return redirect('product:all_view')
        except Exception as e:
            print(e)
            messages.error(request, "Couldn't add product", "alert-danger")
    else:
        print("not valid form", product_form.errors)
    return render(request, 'product/add.html',
                  {'product_form': product_form, 'categories': categories, 'suppliers': suppliers})


# Edit not functional
def edit_view(request: HttpRequest, product_id: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        product_form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if product_form.is_valid():
            product_form.save()
        else:
            print("not valid form", product_form.errors)
        return redirect('product:detail_view', product_id=product_id)

    return render(request, 'product/edit.html', {'product': product, 'categories': categories, 'suppliers': suppliers})


def all_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(products, 2)
    products_page = paginator.get_page(page_number)
    num_products = products.aggregate(Count('id'))
    avg_price = products.aggregate(Avg('price'))
    expensive_price = products.aggregate(Max('price'))
    cheap_price = products.aggregate(Min('price'))
    price_total = products.aggregate(Sum('price'))

    return render(request, 'product/all.html', {'products': products, 'products_page': products_page})


def detail_view(request: HttpRequest, product_id: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/detail.html', {'product': product})


def delete_view(request: HttpRequest, product_id: int) -> HttpResponse:
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Deleted product successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't delete product", "alert-danger")
    return redirect('product:all_view')


# Search not functional
def search_view(request: HttpRequest) -> HttpResponse:
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        products = Product.objects.filter(name__contains=request.GET["search"])
    else:
        products = []
    return render(request, 'product/search.html', {'products': products})
