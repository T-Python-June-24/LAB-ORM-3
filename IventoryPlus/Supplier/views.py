from django.shortcuts import render , redirect
from django.http import HttpRequest
from .models import Supplier
from .forms import SupplierForms
import os
# Create your views here.


def Add_Supplier(request:HttpRequest):
    if request.method == 'POST':
        supplier_form = SupplierForms(request.POST, request.FILES)
        if supplier_form.is_valid():
            supplier_form.save()
            return redirect('Manger:manger_supplier')  
        else:
            print('Error:', supplier_form.errors)
    else:
        supplier_form = SupplierForms()

    return render(request, 'index.html', {'form': supplier_form})



def Update_Supplier(request: HttpRequest, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)  
    if request.method == 'POST':
        supplier_form = SupplierForms(request.POST, request.FILES, instance=supplier)
        if supplier_form.is_valid():
            supplier_form.save()
            return redirect('Manger:manger_supplier')
        else:
            print('Error:', supplier_form.errors)
            return redirect('Manger:manger_supplier')
def delet_supplier(request:HttpRequest , supplier_id):
    del_supplier = Supplier.objects.get(pk=supplier_id)
    if del_supplier.logo_Supplier:
        if os.path.isfile(del_supplier.logo_Supplier.path):
            os.remove(del_supplier.logo_Supplier.path)
    del_supplier.delete()
    return redirect('Manger:manger_supplier')

