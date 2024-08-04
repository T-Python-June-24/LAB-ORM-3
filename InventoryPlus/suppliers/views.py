from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from products.models import Product
from django.contrib import messages

def supplier_list(request):
    
    suppliers = Supplier.objects.all()
    if not suppliers :

        messages.error(request, "No suppliers to display. Add the first one now!", "info")

    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

def supplier_add(request):
    
    try:

        if request.method == 'POST':

            form = SupplierForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Added supplier successfully", "success")
                return redirect('suppliers:supplier_list')
            else:
                messages.error(request, "Unable to add supplier. Please enter valid information", "danger")

    except Exception as e :
        print("Error: ",e)
        messages.error(request, "Couldn't Add supplier", "danger")

    return render(request, 'suppliers/supplier_add.html')


def supplier_detail(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    products = Product.objects.filter(productSupplier=supplier)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier, 'products': products})

def supplier_update(request, supplier_id):

    try:

        supplier = Supplier.objects.get(pk=supplier_id)
        if request.method == 'POST':
            form = SupplierForm(instance=supplier ,data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "update supplier successfully", "success")
                return redirect('suppliers:supplier_detail',supplier_id=supplier.id)
            else:
                messages.error(request, "Unable to update supplier. Please enter valid information", "danger")

            
    except  Exception as e :
        print("Error: ",e)
        messages.error(request,e, "danger")

    return render(request, 'suppliers/supplier_update.html', {'supplier': supplier})

def supplier_delete(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        if request.method == 'POST':
            supplier.delete()
            messages.success(request, "Deleted supplier successfully", "success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete supplier", "danger")
    return redirect('suppliers:supplier_list')
    # return render(request, 'suppliers/supplier_delete.html', {'supplier': supplier})
