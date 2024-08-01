from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from supplier.models import Supplier


def all_suppliers_view(request:HttpRequest ):
    suppliers = Supplier.objects.all()
    return render(request, "allSupplier.html", {"suppliers":suppliers})

def delete_suppliers_view(request:HttpRequest, supplier_id: int):
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.delete()
    return redirect("supplier:all_suppliers_view")

def add_suppliers_view(request: HttpRequest):
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        new_Category = Supplier(name=request.POST['name'], email=request.POST['email'], phone=request.POST['phone'])
        new_Category.save()
    return render(request, "addSupplier.html",  {"suppliers": suppliers})

def update_suppliers_view(request:HttpRequest, supplier_id:int):
    suppliers = Supplier.objects.get(id=supplier_id)
    if request.method == "POST":
        suppliers.name = request.POST["name"]
        suppliers.email = request.POST["email"]
        suppliers.phone = request.POST["phone"]
        suppliers.save()
        return redirect('supplier:all_suppliers_view')
    
    return render(request, "supplier:add_suppliers_view", {"suppliers":suppliers})
