from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from products.models import Product  # Make sure to import the Product model
from .forms import CategoryForm

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories/all_categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories:all_categories')
    else:
        form = CategoryForm()
    return render(request, 'categories/add_category.html', {'form': form})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = category.product_set.all()
    return render(request, 'categories/category_detail.html', {'category': category, 'products': products})

def category_update(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories:all_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/update_category.html', {'form': form})

def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories:all_categories')
    return render(request, 'categories/delete_category.html', {'category': category})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        category_id = product.productCategory.id
        product.delete()
        return redirect('categories:category_detail', category_id=category_id)
    return render(request, 'categories/delete_product.html', {'product': product})
