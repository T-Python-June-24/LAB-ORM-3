from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import csv
from django.db.models import Q, Max, ExpressionWrapper, BooleanField
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Supplier
from .forms import SupplierForm
from products.models import Product
from django.contrib.auth.decorators import user_passes_test

def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff, login_url='login')(view_func)
    return decorated_view_func

@staff_required
def supplier_list(request):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    suppliers = Supplier.objects.annotate(
        highest_quantity_supplied=Max('product__quantity'),
        is_active=ExpressionWrapper(
            Q(last_active__gte=thirty_days_ago),
            output_field=BooleanField()
        ),
        is_best_seller=ExpressionWrapper(
            Q(highest_quantity_supplied__gte=1000),
            output_field=BooleanField()
        )
    )
    
    search_query = request.GET.get('search_query')
    sort_by = request.GET.get('sort_by')
    status_filter = request.GET.get('status_filter')
    quantity_filter = request.GET.get('quantity_filter')

    if search_query:
        suppliers = suppliers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    if status_filter:
        if status_filter == 'active':
            suppliers = suppliers.filter(is_active=True)
        elif status_filter == 'inactive':
            suppliers = suppliers.filter(is_active=False)
        elif status_filter == 'best_seller':
            suppliers = suppliers.filter(is_best_seller=True)

    if quantity_filter:
        if quantity_filter == 'high':
            suppliers = suppliers.filter(highest_quantity_supplied__gt=1000)
        elif quantity_filter == 'medium':
            suppliers = suppliers.filter(highest_quantity_supplied__range=(100, 1000))
        elif quantity_filter == 'low':
            suppliers = suppliers.filter(highest_quantity_supplied__lt=100)

    if sort_by:
        if sort_by == 'name_asc':
            suppliers = suppliers.order_by('name')
        elif sort_by == 'name_desc':
            suppliers = suppliers.order_by('-name')
        elif sort_by == 'quantity_high':
            suppliers = suppliers.order_by('-highest_quantity_supplied')
        elif sort_by == 'quantity_low':
            suppliers = suppliers.order_by('highest_quantity_supplied')

    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'suppliers': suppliers,
        'form': SupplierForm(),
    }
    return render(request, 'suppliers/supplier_list.html', context)

@staff_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier_products = Product.objects.filter(supplier=supplier)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier, 'supplier_products': supplier_products})

@staff_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Supplier was created successfully')
            return redirect('supplier_detail', pk=supplier.id)
    else:
        form = SupplierForm()
        messages.error(request, 'Supplier was not created successfully')
    return redirect('supplier_list')

@staff_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.last_active = timezone.now()
            supplier.save()
            messages.success(request, 'Supplier was updated successfully')
            return redirect('supplier_list')
        else:
            messages.error(request, 'Supplier was not updated successfully')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'supplier': supplier})

@staff_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier was deleted successfully')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})

@staff_required
def import_suppliers_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('supplier_list')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        required_columns = {'name', 'email', 'phone', 'address', 'website'}
        if not required_columns.issubset(map(str.lower, reader.fieldnames)):
            messages.error(request, 'CSV file must contain Name, Email, Phone, Address, and Website columns matching the Supplier model.')
            return redirect('supplier_list')

        try:
            for row in reader:
                Supplier.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'email': row['email'],
                        'phone': row['phone'],
                        'address': row['address'],
                        'website': row['website']
                    }
                )
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {str(e)}')
            return redirect('supplier_list')

        messages.success(request, 'Suppliers imported successfully.')
    return redirect('supplier_list')

@staff_required
def export_suppliers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="suppliers_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Address', 'Website'])

    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        writer.writerow([supplier.name, supplier.email, supplier.phone, supplier.address, supplier.website])

    messages.success(request, 'Suppliers exported successfully.')
    return response

@staff_required
def update_last_active(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.last_active = timezone.now()
    supplier.save()
    return JsonResponse({'success': True, 'last_active': supplier.last_active.isoformat()})

