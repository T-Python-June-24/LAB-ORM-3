from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Supplier
from .forms import SupplierForm


# Create your views here.
def add_view(request: HttpRequest) -> HttpResponse:
    supplier_form = SupplierForm()
    if request.method == 'POST':
        try:
            supplier_form = SupplierForm(request.POST)
            if supplier_form.is_valid():
                supplier_form.save()
                messages.success(request, "Added supplier successfully", "alert-success")
                return redirect('supplier:all_view')
        except Exception as e:
            print(e)
            messages.error(request, "Couldn't add supplier", "alert-danger")
    else:
        print("not valid form", supplier_form.errors)
    return render(request, 'supplier/add.html', {'supplier_form': supplier_form})


# Edit not functional
def edit_view(request: HttpRequest, supplier_id: int) -> HttpResponse:
    supplier = Supplier.objects.get(id=supplier_id)
    # supplier_form = SupplierForm(instance=supplier)
    return render(request, 'supplier/edit.html', {'supplier': supplier})


def all_view(request: HttpRequest) -> HttpResponse:
    suppliers = Supplier.objects.all()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(suppliers, 2)
    suppliers_page = paginator.get_page(page_number)
    return render(request, 'supplier/all.html', {'suppliers': suppliers, 'suppliers_page': suppliers_page})


def detail_view(request: HttpRequest, supplier_id: int) -> HttpResponse:
    supplier = Supplier.objects.get(id=supplier_id)
    suppliers = supplier.supplier_set.all()
    return render(request, 'supplier/detail.html', {'supplier': supplier, 'suppliers': suppliers})


def delete_view(request: HttpRequest, supplier_id: int) -> HttpResponse:
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        messages.success(request, "Deleted supplier successfully", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't delete supplier", "alert-danger")
    return redirect('supplier:all_view')


# Search not functional
def search_view(request: HttpRequest) -> HttpResponse:
    if "search" in request.GET and len(request.GET["search"]) >= 3:
        suppliers = Supplier.objects.filter(name__contains=request.GET["search"])
    else:
        suppliers = []
    return render(request, 'supplier/search.html', {'suppliers': suppliers})
