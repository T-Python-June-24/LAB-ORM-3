from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Supplier
from django.contrib import messages
from django.db.models import Count, Avg

# Create your views here.


def add_supplier_view(request: HttpRequest):
    if request.method == 'POST':
      try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        phone_number = request.POST.get('phone_number')
        logo = request.FILES.get('logo')

        Supplier.objects.create(name=name, email=email, website=website, phone_number=phone_number, logo=logo)

        messages.success(request, "Supplier added successfully.")
        return redirect('suppliers:suppliers_list')
      except Exception as e:
          messages.error(request, f"An error occurred while adding the supplier: {e}")
    return render(request, 'suppliers/add_supplier.html')


def edit_supplier_view(request: HttpRequest, supplier_id):
    
    supplier = Supplier.objects.get(pk=supplier_id)

    if request.method == 'POST':
      try:  
          supplier.name = request.POST.get('name')
          supplier.email = request.POST.get('email')
          supplier.website = request.POST.get('website')
          supplier.phone_number = request.POST.get('phone_number')
          if request.FILES.get('logo'):
              supplier.logo = request.FILES.get('logo')
          supplier.save()

          messages.success(request, "supplier updated successfully.")
          return redirect('suppliers:suppliers_list')
      except Exception as e:
          messages.error(request, f"An error occurred while updating the supplier: {e}")
    return render(request, 'suppliers/edit_supplier.html', {'supplier': supplier})



def delete_supplier_view(request: HttpRequest, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    if request.method == 'POST':
        try: 
          supplier.delete()
          messages.success(request, "Supplier deleted successfully.")
        except Exception as e:
          messages.error(request, f"An error occurred while deleting the supplier: {e}")
        return redirect('suppliers:suppliers_list')



def suppliers_list_view(request: HttpRequest):
    suppliers = Supplier.objects.annotate(
      product_count = Count('products'),
      average_price=Avg('products__price')
    )
    return render(request, 'suppliers/suppliers_list.html', {'suppliers': suppliers})



def supplier_detail_view(request: HttpRequest, supplier_id):
    supplier = Supplier.objects.annotate(
      product_count=Count('products'),
      average_price=Avg('products__price')
    ).get(pk=supplier_id)
    return render(request, 'suppliers/supplier_detail.html', {'supplier': supplier})

