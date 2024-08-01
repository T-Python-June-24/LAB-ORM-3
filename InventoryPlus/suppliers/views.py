from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from products.models import Product

def supplier_list(request):
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        if 'add_supplier' in request.POST:
            form = SupplierForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('suppliers:supplier_list')
        elif 'edit_supplier' in request.POST:
            supplier_id = request.POST.get('supplier_id')
            supplier = get_object_or_404(Supplier, pk=supplier_id)
            form = SupplierForm(request.POST, request.FILES, instance=supplier)
            if form.is_valid():
                form.save()
                return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers, 'form': form})

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = Product.objects.filter(productSupplier=supplier)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier, 'products': products})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_list.html', {'form': form, 'suppliers': Supplier.objects.all()})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers:supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})
