from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Supplier
from .forms import ProductForm, CategoryForm, SupplierForm
from django.http import HttpResponse
import pandas as pd
import csv
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Product views

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Error creating product.')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Error updating product.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)  # Show 5 products per page

    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(total_stock=Count('stock_quantity'))['total_stock']

    context = {
        'page_obj': page_obj,
        'total_products': total_products,
        'total_stock': total_stock,
    }
    return render(request, 'products/product_list.html', context)

# Category views

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('category_list')
        else:
            messages.error(request, 'Error creating category.')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
        else:
            messages.error(request, 'Error updating category.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})

def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)  # Show 5 categories per page

    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'category/category_list.html', context)

# Supplier views
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully!')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Error creating supplier. Please correct the errors below.')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_detail', pk=supplier.pk)
        else:
            messages.error(request, 'Error updating supplier. Please correct the errors below.')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})



def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})
#######################################
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    # Stock data for chart
    stock_data = {
        'labels': [product.name for product in Product.objects.all()],
        'data': [product.stock_quantity for product in Product.objects.all()]
    }

    # Recent activities (for example purposes, replace with actual activities)
    recent_activities = [
        "Product A was added",
        "Product B stock updated",
        "Supplier X added a new product"
    ]

    # Alerts for low stock and expiring products
    low_stock_products = Product.objects.filter(stock_quantity__lte=5)
    expiring_soon_products = Product.objects.filter(expiry_date__lte=timezone.now().date() + timedelta(days=5))

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'stock_data': stock_data,
        'recent_activities': recent_activities,
        'low_stock_products': low_stock_products,
        'expiring_soon_products': expiring_soon_products
    }

    return render(request, 'inventory/dashboard.html', context)


def export_csv(request, model_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_type}_data.csv"'

    writer = csv.writer(response)

    if model_type == 'products':
        writer.writerow(['Product Name', 'Category', 'Supplier', 'Price', 'Stock Quantity'])
        products = Product.objects.all()
        for product in products:
            writer.writerow([product.name, product.category.name, product.supplier.name, product.price, product.stock_quantity])
    
    elif model_type == 'suppliers':
        writer.writerow(['Supplier Name', 'Email', 'Phone', 'Address', 'Website'])
        suppliers = Supplier.objects.all()
        for supplier in suppliers:
            writer.writerow([supplier.name, supplier.email, supplier.phone, supplier.address, supplier.website])
    
    elif model_type == 'categories':
        writer.writerow(['Category Name'])
        categories = Category.objects.all()
        for category in categories:
            writer.writerow([category.name])
    
    return response

############


def analysis(request):
    # Product stock data for chart
    product_stock_data = {
        'labels': [product.name for product in Product.objects.all()],
        'data': [product.stock_quantity for product in Product.objects.all()]
    }

    # Supplier stock data for chart
    supplier_stock_data = {
        'labels': [supplier.name for supplier in Supplier.objects.all()],
        'data': [sum(product.stock_quantity for product in supplier.product_set.all()) for supplier in Supplier.objects.all()]
    }

    # Category stock data for chart
    category_stock_data = {
        'labels': [category.name for category in Category.objects.all()],
        'data': [sum(product.stock_quantity for product in category.product_set.all()) for category in Category.objects.all()]
    }

    context = {
        'product_stock_data': product_stock_data,
        'supplier_stock_data': supplier_stock_data,
        'category_stock_data': category_stock_data
    }

    return render(request, 'inventory/analysis.html', context)
