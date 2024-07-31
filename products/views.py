from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from .models import Product, Category, Supplier
import csv
from .forms import ProductForm, ProductSearchForm
from .utils import check_product_status, send_product_notification
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)
    return decorated_view_func

@staff_required
def chart_data(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    # The stats that will appear on the top of the page
    total_products = products.count()
    total_quantity = products.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_suppliers = suppliers.count()
    low_stock_products = products.filter(quantity__lte=F('low_stock_threshold')).count()
    total_value = products.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

    # Category Distribution
    category_distribution = products.values('category__name').annotate(count=Count('id'))
    total_count = sum(item['count'] for item in category_distribution)
    category_distribution = {
        item['category__name']: {
            'count': item['count'],
            'percentage': (item['count'] / total_count) * 100
        }
        for item in category_distribution
    }

    # Top 10 Products by Quantity
    top_products = products.order_by('-quantity')[:10]
    top_products_data = {
        product.name: {
            'quantity': product.quantity,
            'percentage': (product.quantity / total_quantity) * 100
        }
        for product in top_products
    }

    # monthly spending
    monthly_sales = products.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_sales=Sum(F('price') * F('quantity'))
    ).order_by('month')

    monthly_sales_trend = {
        item['month'].strftime('%Y-%m'): float(item['total_sales'])
        for item in monthly_sales
    }

    # Supplier Distribution
    supplier_distribution = products.values('supplier__name').annotate(count=Count('id'))
    supplier_distribution = {
        item['supplier__name']: {
            'count': item['count'],
            'percentage': (item['count'] / total_count) * 100
        }
        for item in supplier_distribution
    }
    
    # Latest products added to the inventory
    latest_products = list(Product.objects.order_by('-created_at')[:5].values(
        'name', 'quantity', 'created_at',
        'category__name', 'supplier__name'
    ))

    for product in latest_products:
        product['category'] = product.pop('category__name')
        product['supplier'] = product.pop('supplier__name')

    data = {
        'top_stats': {
            'total_products': total_products,
            'total_quantity': total_quantity,
            'low_stock_products': low_stock_products,
            'total_value': float(total_value),
            'total_suppliers': total_suppliers,
        },
        'category_distribution': {
            'data': category_distribution,
            'description': "This chart shows the distribution of products across different categories. It helps identify which categories have the most products."
        },
        'top_products': {
            'data': top_products_data,
            'description': "This chart displays the top 10 products by quantity. It helps identify the most stocked items in the inventory."
        },
        'monthly_sales_trend': {
            'data': monthly_sales_trend,
            'description': "This chart shows the monthly sales trend over time. It helps visualize sales performance and identify patterns or seasonality."
        },
        'supplier_distribution': {
            'data': supplier_distribution,
            'description': "This chart illustrates the distribution of products among different suppliers. It helps understand the diversity of your supply chain."
        },
        'latest_products': {
            'data': latest_products,
        },
    }

    return JsonResponse(data)

@staff_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    form = ProductForm()
    search_form = ProductSearchForm(request.GET)

    if request.method == 'POST':
        if 'update' in request.POST:
            product = get_object_or_404(Product, pk=request.POST.get('product_id'))
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                updated_product = form.save()
                messages.success(request, f'Product "{updated_product.name}" has been successfully updated.')
                send_product_notification(updated_product)  
                return redirect('product_list')
            else:
                messages.error(request, 'Product was not updated successfully, check the form again')
        elif 'create' in request.POST:
            form = ProductForm(request.POST)
            if form.is_valid():
                new_product = form.save()
                messages.success(request, f'Product "{new_product.name}" has been successfully created.')
                send_product_notification(new_product)  
                return redirect('product_list')
            else:
                messages.error(request, 'Product was not created successfully, check the form again')

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        category = search_form.cleaned_data.get('category')
        sort_by = search_form.cleaned_data.get('sort_by')
        stock_status = search_form.cleaned_data.get('stock_status')

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category:
            products = products.filter(category=category)

        if sort_by:
            if sort_by == 'name_asc':
                products = products.order_by('name')
            elif sort_by == 'name_desc':
                products = products.order_by('-name')
            elif sort_by == 'quantity_high':
                products = products.order_by('-quantity')
            elif sort_by == 'quantity_low':
                products = products.order_by('quantity')
            elif sort_by == 'price_high':
                products = products.order_by('-price')
            elif sort_by == 'price_low':
                products = products.order_by('price')
            elif sort_by == 'expiry':
                products = products.order_by('expiry_date')

        if stock_status:
            if stock_status == 'in_stock':
                products = products.filter(quantity__gt=F('low_stock_threshold'))
            elif stock_status == 'low_stock':
                products = products.filter(quantity__lte=F('low_stock_threshold'), quantity__gt=0)
            elif stock_status == 'out_of_stock':
                products = products.filter(quantity=0)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'categories': categories,
        'form': form,
        'search_form': search_form,
        'now': timezone.now().date(),
    }
    if not products.exists():
        messages.error(request, 'No products found.')
    return render(request, 'products/product_list.html', context)

@staff_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        if 'update' in request.POST:
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                updated_product = form.save()
                messages.success(request, f'Product "{updated_product.name}" has been successfully updated.')
                send_product_notification(updated_product)  
                return redirect('product_detail', pk=updated_product.pk)
            else:
                messages.error(request, 'Failed to update product. Please check the form and try again.')
        elif 'delete' in request.POST:
            product_name = product.name
            product.delete()
            messages.success(request, f'Product "{product_name}" has been successfully deleted.')
            return redirect('product_list')

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)

@staff_required
def check_product_status_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    status = check_product_status(product)
    return JsonResponse(status)

@staff_required
def import_products_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('product_list')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        required_columns = {'name', 'description', 'category', 'price', 'supplier', 'quantity', 'expiry_date', 'created_at'}
        if not required_columns.issubset(map(str.lower, reader.fieldnames)):
            messages.error(request, 'CSV file must contain Name, Description, Category, Price, Supplier, Quantity, Expiry Date, and Created At columns matching the Product model.')
            return redirect('product_list')

        try:
            products_created = 0
            products_updated = 0
            for row in reader:
                category, _ = Category.objects.get_or_create(name=row['category'])
                supplier, _ = Supplier.objects.get_or_create(name=row['supplier'])
                product, created = Product.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'description': row['description'],
                        'category': category,
                        'price': float(row['price']),
                        'supplier': supplier,
                        'quantity': int(row['quantity']),
                        'expiry_date': datetime.strptime(row['expiry_date'], '%Y-%m-%d').date(),
                        'created_at': datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
                    }
                )
                if created:
                    products_created += 1
                    send_product_notification(product)  
                else:
                    products_updated += 1
                    send_product_notification(product)  
            
            messages.success(request, f'CSV import successful. {products_created} products created, {products_updated} products updated.')
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
            return redirect('product_list')

    return redirect('product_list')

@staff_required
def product_delete(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product_name = product.name
            product.delete()
            messages.success(request, f'Product "{product_name}" has been successfully deleted.')
            return redirect('product_list')
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    return render(request, 'products/product_list.html', {'product': product})

@staff_required
def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Category', 'Price', 'Supplier', 'Quantity', 'Expiry Date'])

    products = Product.objects.all()
    for product in products:
        writer.writerow([
            product.name,
            product.description,
            product.category.name,
            product.price,
            product.supplier.name if product.supplier else '',
            product.quantity,
            product.expiry_date
        ])

    messages.success(request, 'Products have been successfully exported to CSV.')
    return response
