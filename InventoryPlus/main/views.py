from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from product.models import Product
from supplier.models import Supplier
from inventory.models import Inventory
from django.db.models import Sum



def dashboard_view(request:HttpRequest):
    product = Product.objects.all()
    inventory = Inventory.objects.all()
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_inventory_items = Inventory.objects.count()
    products_with_quantity = Product.objects.annotate(
        total_quantity=Sum('inventory__quantity')
    )


    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_inventory_items': total_inventory_items,
        'products_with_quantity': products_with_quantity,
        'products': product,
        'inventories':inventory
    }

    return render(request, 'index.html', context)


