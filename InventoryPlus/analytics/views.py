from django.shortcuts import render
from inventory.models import Product, Supplier, Category
# from django.utils import timezone
# from datetime import timedelta
from django.http import JsonResponse
from django.db.models import Sum




def inventory_report(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category__id=selected_category)
    else:
        products = Product.objects.all()
    low_stock_products = Product.objects.filter(stock__lt=10)
    stock_by_category = Product.objects.values('category__name').annotate(total_stock=Sum('stock')).order_by('category__name')

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'products': products,
        'low_stock_products': low_stock_products,
        'stock_by_category': stock_by_category,
    }
    return render(request, 'analytics/inventory_report.html', context)



def category_details(request):
    category_name = request.GET.get('category')
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    labels = [f"{product.name} ({product.category.name})" for product in products]
    data = [product.stock for product in products]
    return JsonResponse({'labels': labels, 'data': data})




def supplier_report(request):
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'analytics/supplier_report.html', context)




def low_stock_alerts(request):
    low_stock_products = Product.objects.filter(stock__lt=10)
    context = {
        'low_stock_products': low_stock_products,
    }
    return render(request, 'analytics/low_stock_alerts.html', context)



# def expiry_date_alerts(request):
#     today = timezone.now()
#     expiry_date_threshold = today + timedelta(days=30)
#     expiring_soon_products = Product.objects.filter(expiry_date__lte=expiry_date_threshold)
#     context = {
#         'expiring_soon_products': expiring_soon_products,
#     }
#     return render(request, 'analytics/expiry_date_alerts.html', context)
