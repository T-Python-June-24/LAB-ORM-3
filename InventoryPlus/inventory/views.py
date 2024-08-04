from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict
from .models import Product, Category, Supplier
from .forms import ProductForm, CategoryForm, SupplierForm, CSVUploadForm
from .tasks import send_low_stock_alert
import pandas as pd
import csv
from .forms import CSVUploadForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse




def product_list(request):
    category = request.GET.get('category')
    sort_by = request.GET.get('sort', 'stock')
    sort_order = request.GET.get('order', 'asc')
    paginate_by = request.GET.get('paginate_by', 5)

    products = Product.objects.all()
    if category:
        products = products.filter(category=category)

    if sort_order == 'desc':
        products = products.order_by(f'-{sort_by}')
    else:
        products = products.order_by(sort_by)

    paginator = Paginator(products, paginate_by)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    total_items = products.count()

    categories = Category.objects.all()
    return render(request, 'inventory/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'total_items': total_items,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'paginate_by': int(paginate_by),
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)
    return render(request, 'inventory/product_detail.html', {'product': product, 'related_products': related_products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:product_list')}?{query_string}")
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:product_detail', args=[product.pk])}?{query_string}")
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
        product.delete()
        messages.success(request, 'Product deleted successfully.', 'alert-success')
        return redirect(f"{reverse('inventory:product_list')}?{query_string}")
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})





# category
def category_list(request):
    sort_by = request.GET.get('sort', 'product_count')
    sort_order = request.GET.get('order', 'desc')
    paginate_by = request.GET.get('paginate_by', 3)

    categories = Category.objects.annotate(product_count=Count('product'))
    if sort_order == 'desc':
        categories = categories.order_by(f'-{sort_by}')
    else:
        categories = categories.order_by(sort_by)

    paginator = Paginator(categories, paginate_by)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    total_items = categories.count()

    return render(request, 'categories/category_list.html', {
        'categories': page_obj,
        'total_items': total_items,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'paginate_by': int(paginate_by),
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'categories/category_detail.html', {'category': category})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:category_list')}?{query_string}")
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:category_list')}?{query_string}")
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
        category.delete()
        messages.success(request, 'Category deleted successfully.', 'alert-success')
        return redirect(f"{reverse('inventory:category_list')}?{query_string}")
    return render(request, 'categories/category_confirm_delete.html', {'category': category})



# supplier
def supplier_list(request):
    sort_by = request.GET.get('sort', 'name')
    sort_order = request.GET.get('order', 'asc')
    paginate_by = request.GET.get('paginate_by', 5)

    suppliers = Supplier.objects.annotate(product_count=Count('products'))
    if sort_order == 'desc':
        suppliers = suppliers.order_by(f'-{sort_by}')
    else:
        suppliers = suppliers.order_by(sort_by)

    paginator = Paginator(suppliers, paginate_by)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    total_items = suppliers.count()

    return render(request, 'suppliers/supplier_list.html', {
        'suppliers': page_obj,
        'total_items': total_items,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'paginate_by': int(paginate_by),
    })

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = supplier.products.all()
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier, 'products': products})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:supplier_list')}?{query_string}")
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully.', 'alert-success')
            query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
            return redirect(f"{reverse('inventory:supplier_list')}?{query_string}")
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        query_string = QueryDict(request.META['QUERY_STRING']).urlencode()
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully.', 'alert-success')
        return redirect(f"{reverse('inventory:supplier_list')}?{query_string}")
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})



#search
def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
        suppliers = Supplier.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()
        suppliers = Supplier.objects.none()
    return render(request, 'inventory/search_results.html', {
        'products': products,
        'suppliers': suppliers,
        'query': query,
        'product_count': products.count(),
        'supplier_count': suppliers.count(),
    })




#email notifications
# def check_low_stock_products():
#     low_stock_products = Product.objects.filter(stock__lt=10)
#     for product in low_stock_products:
#         send_low_stock_alert(product)

# def inventory_report(request):
#     products = Product.objects.all()
#     low_stock_products = Product.objects.filter(stock__lt=10)

#     check_low_stock_products()

#     context = {
#         'products': products,
#         'low_stock_products': low_stock_products,
#     }
#     return render(request, 'analytics/inventory_report.html', context)



def check_stock_view(request):
    send_low_stock_alert()
    return render(request, 'inventory/stock_checked.html')



# CSV
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def import_csv(request, model):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                data = pd.read_csv(csv_file)
                logger.debug(f'CSV Data: {data.head()}')

                if model == 'product':
                    required_columns = ['name', 'category', 'price', 'stock', 'description', 'image']
                    if not all(column in data.columns for column in required_columns):
                        messages.error(request, f'CSV file must contain the following columns: {", ".join(required_columns)}')
                        return redirect('inventory:import_csv', model=model)

                    for index, row in data.iterrows():
                        category, _ = Category.objects.get_or_create(name=row['category'])
                        product, created = Product.objects.get_or_create(
                            name=row['name'],
                            defaults={
                                'category': category,
                                'price': row['price'],
                                'stock': row['stock'],
                                'description': row.get('description', ''),
                                'image': row.get('image', '')
                            }
                        )
                        if not created:
                            product.category = category
                            product.price = row['price']
                            product.stock = row['stock']
                            product.description = row.get('description', '')
                            product.image = row.get('image', '')
                            product.save()

                elif model == 'category':
                    required_columns = ['name', 'description']
                    if not all(column in data.columns for column in required_columns):
                        messages.error(request, f'CSV file must contain the following columns: {", ".join(required_columns)}')
                        return redirect('inventory:import_csv', model=model)

                    for index, row in data.iterrows():
                        Category.objects.get_or_create(
                            name=row['name'],
                            defaults={'description': row.get('description', '')}
                        )

                elif model == 'supplier':
                    required_columns = ['name', 'contact_email', 'phone_number']
                    if not all(column in data.columns for column in required_columns):
                        messages.error(request, f'CSV file must contain the following columns: {", ".join(required_columns)}')
                        return redirect('inventory:import_csv', model=model)

                    for index, row in data.iterrows():
                        Supplier.objects.get_or_create(
                            name=row['name'],
                            defaults={
                                'contact_email': row.get('contact_email', ''),
                                'phone_number': row.get('phone_number', '')
                            }
                        )

                messages.success(request, f'{model.capitalize()}s imported successfully.')
                return redirect(f'inventory:{model}_list')
            except Exception as e:
                logger.error(f'Error processing CSV file: {e}', exc_info=True)
                messages.error(request, f'Error processing CSV file: {e}')
                return redirect('inventory:import_csv', model=model)
    else:
        form = CSVUploadForm()
    return render(request, f'inventory/import_{model}.html', {'form': form})

def export_csv_products(request):
    products = Product.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = pd.DataFrame(list(products.values('name', 'category__name', 'price', 'stock', 'description', 'image')))
    writer.columns = ['Name', 'Category', 'Price', 'Stock', 'Description', 'Image']
    writer.to_csv(path_or_buf=response, index=False)
    return response

def export_csv_categories(request):
    categories = Category.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categories.csv"'
    writer = pd.DataFrame(list(categories.values('name', 'description')))
    writer.columns = ['Name', 'Description']
    writer.to_csv(path_or_buf=response, index=False)
    return response

def export_csv_suppliers(request):
    suppliers = Supplier.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="suppliers.csv"'
    writer = pd.DataFrame(list(suppliers.values('name', 'contact_email', 'phone_number')))
    writer.columns = ['Name', 'Contact Email', 'Phone Number']
    writer.to_csv(path_or_buf=response, index=False)
    return response
