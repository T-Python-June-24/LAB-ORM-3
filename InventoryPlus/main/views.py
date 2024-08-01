from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from product.models import Product
from supplier.models import Supplier
from inventory.models import Inventory
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages


def dashboard_view(request:HttpRequest):
    product = Product.objects.all()
    inventory = Inventory.objects.all()
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_inventory_items = Inventory.objects.count() # count the number of products using 
    products_with_quantity = Product.objects.annotate( total_quantity=Sum('inventory__quantity'))

    page_number = request.GET.get("page", 1)
    paginator = Paginator(products_with_quantity, 2)
    product_page = paginator.get_page(page_number)



    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_inventory_items': total_inventory_items,
        'products': product_page,
        'inventories':inventory,
    }

    return render(request, 'index.html', context)


