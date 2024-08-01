from django.shortcuts import render
from django.db.models import Sum
from products.models import Order, Payment, Product
from suppliers.models import Supplier

# Create your views here.

def inventory_report(request):
    total_stock = Product.objects.aggregate(total_stock=Sum('stock_quantity'))['total_stock'] or 0
    total_value = Product.objects.aggregate(total_value=Sum('price'))['total_value'] or 0

    products = Product.objects.all()

    context = {
        'total_stock': total_stock,
        'total_value': total_value,
        'products': products,
    }
    return render(request, 'reports/inventory_report.html', context)

def supplier_report(request):
    total_amount_paid = Payment.objects.aggregate(total_amount_paid=Sum('amount'))['total_amount_paid']

    # Retrieve suppliers
    suppliers = Supplier.objects.all()

    supplier_data = []
    for supplier in suppliers:
        total_orders = Order.objects.filter(supplier=supplier).count()
        total_payments = Payment.objects.filter(supplier=supplier).aggregate(total_payments=Sum('amount'))['total_payments'] or 0

        supplier_data.append({
            'name': supplier.name,
            'email': supplier.email,
            'phone': supplier.phone,
            'total_orders': total_orders,
            'total_payments': total_payments,
        })

    context = {
        'suppliers': supplier_data,
        'total_amount_paid': total_amount_paid,
    }
    return render(request, 'reports/supplier_report.html', context)
