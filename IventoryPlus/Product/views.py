import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from Suppliers.models import Supplier
from Categories.models import Category
from .models import Product
from .forms import ProductForm
from django.contrib import messages
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from datetime import datetime
from Notifications.utils import send_alerts
from django.utils.dateparse import parse_datetime, parse_date
from django.contrib import messages

def login(request:HttpResponse):
    return render(request, 'Product/login.html')

def signup(request:HttpResponse):
    return render(request, 'Product/signup.html')

def thanksPage(request:HttpResponse):
    return render(request,'Product/thanks_page.html')


def product_list(request:HttpResponse):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__id=category_filter)

    paginator = Paginator(products, 8)  #! Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
    }
    return render(request, 'Product/product_list.html', context)

def product_detail(request:HttpResponse, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Product/product_detail.html', {'product': product})


def product_create(request:HttpResponse):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Product:thanks')
    else:
        form = ProductForm()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    
    return render(request, 'Product/add_product.html', {'form': form, 'categories': categories, 'suppliers': suppliers, 'product': None})

def product_update(request:HttpResponse, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            send_alerts()
            return redirect('Product:thanks')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ProductForm(instance=product)
    
    category = Category.objects.all()
    suppliers = Supplier.objects.all()

    return render(request, 'Product/update_product.html', {'form': form, 'category': category, 'suppliers': suppliers, 'product': product})


def product_delete(request:HttpResponse, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Product:thanks')
    return render(request, 'Product/product_confirm_delete.html', {'product': product})



def product_search(request):
    query = request.GET.get('query')
    products = Product.objects.all()
    
    if query:
        products_name = Product.objects.filter(name__icontains=query)
        products_category = Product.objects.filter(category__name__icontains=query)
        products_supplier = Product.objects.filter(suppliers__name__icontains=query)
        products = (products_name | products_category | products_supplier).distinct()
        count = products.count()
    else:
        products = Product.objects.all()
        count = products.count()

    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'Product/search_product.html', {'products': products, 'count': count, 'query': query})



def stock_status(request:HttpResponse):
    products = Product.objects.all()
    return render(request, 'Product/stock_status.html', {'products': products})



def stock_status(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 8)  # Show 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'Product/stock_status.html', {'products': products})

def update_stock(request:HttpResponse, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        stock_quantity = request.POST.get('stock_quantity')
        if stock_quantity:
            try:
                product.stock_quantity = int(stock_quantity)
                product.save()
                send_alerts()  #! Send alerts after updating stock quantity
                return redirect('Product:stock_status')  
            except ValueError:
                print("Invalid stock quantity provided.")
        else:
            print("No stock quantity provided.")
    return render(request, 'Product/update_stock.html', {'product': product})



def export_products_csv(request:HttpResponse):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_and_suppliers.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow([
        'Product ID', 'Product Name', 'Product Image URL', 'Product Description', 'Product Price',
        'Product Stock Quantity', 'Product Category', 'Product Suppliers', 'Product Created At',
        'Supplier ID', 'Supplier Name', 'Supplier Email', 'Supplier Logo URL', 'Supplier Phone Number',
        'Supplier Website', 'Supplier Contact Person Name', 'Supplier Contact Person Job Title',
        'Supplier Country', 'Supplier City', 'Supplier Active', 'Supplier Supplied Products',
 
    ])

    # Write data rows
    products = Product.objects.all()
    for product in products:
        for supplier in product.suppliers.all():
            writer.writerow([
                product.id,
                product.name,
                product.product_image.url,
                product.description,
                product.price,
                product.stock_quantity,
                product.category.name,
                ", ".join(supplier.name for supplier in product.suppliers.all()),
                product.created_at,
                supplier.id,
                supplier.name,
                supplier.email,
                supplier.logo.url,
                supplier.phone_number,
                supplier.website,
                supplier.contact_person_name,
                supplier.contact_person_job_title,
                supplier.country,
                supplier.city,
                supplier.active,
                supplier.supplied_products,
            ])
    
    return response





def export_products_excel(request:HttpResponse):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Products and Suppliers'

    headers = [
        'Product ID', 'Product Name', 'Product Image URL', 'Product Description', 'Product Price',
        'Product Stock Quantity', 'Product Category', 'Product Suppliers', 'Product Created At',
        'Supplier ID', 'Supplier Name', 'Supplier Email', 'Supplier Logo URL', 'Supplier Phone Number',
        'Supplier Website', 'Supplier Contact Person Name', 'Supplier Contact Person Job Title',
        'Supplier Country', 'Supplier City', 'Supplier Active', 'Supplier Supplied Products',
        'Supplier Services Offered'
    ]
    worksheet.append(headers)

    products = Product.objects.all()
    for product in products:
        for supplier in product.suppliers.all():
            product_created_at = product.created_at
            if isinstance(product_created_at, datetime):
                product_created_at = product_created_at.replace(tzinfo=None)
            
            row = [
                product.id,
                product.name,
                product.product_image.url,
                product.description,
                product.price,
                product.stock_quantity,
                product.category.name,
                ", ".join(supplier.name for supplier in product.suppliers.all()),
                product_created_at,
                supplier.id,
                supplier.name,
                supplier.email,
                supplier.logo.url,
                supplier.phone_number,
                supplier.website,
                supplier.contact_person_name,
                supplier.contact_person_job_title,
                supplier.country,
                supplier.city,
                supplier.active,
                supplier.supplied_products,
                supplier.services_offered
            ]
            worksheet.append(row)

    with NamedTemporaryFile() as tmp:
        workbook.save(tmp.name)
        tmp.seek(0) 
        output = tmp.read()

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="products_and_suppliers.xlsx"'
    return response



def import_products_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file. Please upload a valid CSV file.')
            return render(request, 'Product/import_products.html')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        error_occurred = False

        for row in reader:
            try:
                category, created = Category.objects.get_or_create(name=row['category'])
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {e}')
                error_occurred = True
                break

            suppliers_names = row['suppliers'].split(';')
            suppliers = Supplier.objects.filter(name__in=suppliers_names)

            if not suppliers.exists():
                messages.error(request, f'One or more suppliers with names {row["suppliers"]} do not exist.')
                error_occurred = True
                continue

            try:
                product, created = Product.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'product_image': row['product_image'],
                        'description': row['description'],
                        'price': row['price'],
                        'stock_quantity': row['stock_quantity'],
                        'category': category,
                        'created_at': parse_datetime(row['created_at']),
                        'expiration_date': parse_date(row['expiration_date']),
                    }
                )
                product.suppliers.set(suppliers)
                product.save()

                if created:
                    messages.success(request, f'Product {row["name"]} was successfully created.')
                else:
                    messages.warning(request, f'Product {row["name"]} already exists and was updated.')

            except Exception as e:
                messages.error(request, f'Error saving product {row["name"]}: {e}')
                error_occurred = True
                continue

        if not error_occurred:
            messages.success(request, 'Products imported successfully.')
        
        return redirect('Product:import_products_csv')

    return render(request, 'Product/import_products.html')