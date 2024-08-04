from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Supplier
from .forms import ProductForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
import ssl

def all_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(productName__icontains=query)
    else:

        products = Product.objects.all()
        
        # for product in products:
        #     if product.productStock < 2:
        #         content_html = f"Stock is low for {product.productName}"
        #         send_to = "amira799am@gmail.com"
        #         email_message = EmailMessage("Confirmation", content_html, settings.EMAIL_HOST_USER, [send_to])
        #         email_message.send()
        #         messages.success(request, "Your message is received. Thank You.", "alert-success")

        if "category" in request.GET :
            products = products.filter(productCategory=request.GET.get('category'))
        if "supplier" in request.GET :
            products = products.filter(productSupplier=request.GET.get('supplier'))
    
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    form = ProductForm()
    page_number = request.GET.get("page",1)
    paginator = Paginator(products,1)
    product_page = paginator.get_page(page_number)
    return render(request, 'products/all_products.html', {
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'form': form,
        'product_page' :product_page
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    try:

        if request.method == 'POST':
            print(request.POST['productName'])
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Added product successfully", "success")
                return redirect('products:all_products')
            else:
                print(form.errors.as_text)
                messages.error(request, "Unable to add product. Please enter valid information", "danger")

    except Exception as e :
        print("Error: ",e)
        messages.error(request, "Couldn't Add product", "danger")

    return redirect('products:all_products')

def product_update(request, product_id):
    try:

        product = Product.objects.get(pk=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('products:all_products')
            else:
                messages.error(request, "Unable to update product. Please enter valid information", "danger")

    except Exception as e :
        print("Error: ",e)
        messages.error(request, e , "danger")
    return redirect('products:all_products')

def product_delete(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        print(product.delete())
        messages.success(request, "Deleted product successfully", "success")
# add some conditions to handel certain errors 
        return redirect('products:all_products')
    except Exception as e :
        print("Error: ",e)
        messages.error(request, e , "danger")
    return redirect('products:all_products')
