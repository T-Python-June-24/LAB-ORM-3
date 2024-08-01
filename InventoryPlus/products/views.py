# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Supplier
from .forms import ProductForm

def all_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(productName__icontains=query)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    form = ProductForm()
    return render(request, 'products/all_products.html', {
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'form': form,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:all_products')
    return redirect('products:all_products')

def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:all_products')
    return redirect('products:all_products')

def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('products:all_products')
    return redirect('products:all_products')
