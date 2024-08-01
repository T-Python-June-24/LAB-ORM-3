from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Product, Inventory


def all_inventories_view(request:HttpRequest ):
    inventory = Inventory.objects.all()
    
    return render(request, "allInventory.html", {"inventories":inventory})

def delete_inventories_view(request:HttpRequest, inventory_id: int):
    inventory = Inventory.objects.get(id=inventory_id)
    inventory.delete()
    return redirect("inventory:all_inventories_view")


def add_inventories_view(request: HttpRequest):
    inventories = Inventory.objects.all()
    products = Product.objects.all()
    
    if request.method == "POST":
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status') == 'True'
        
        product = Product.objects.get(id=product_id)
        
        new_inventory = Inventory(
            product=product,
            quantity=quantity,
            status=status
        )
        new_inventory.save()
        
        return redirect('inventory:all_inventories_view') 
    
    return render(request, "addInventory.html", {"inventories": inventories, "products": products})

def update_inventories_view(request:HttpRequest, inventory_id:int):
    inventory = Inventory.objects.get(id=inventory_id)
    if request.method == "POST":
        inventory.quantity = request.POST["quantity"]
        inventory.status = request.POST["status"]
        inventory.save()
        return redirect('inventory:all_inventories_view')
    
    return render(request, "inventory:add_inventory_view", {"inventories":inventory})
