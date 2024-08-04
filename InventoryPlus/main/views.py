from django.shortcuts import render
from inventory.models import Product, Category, Supplier
from django.db.models import Count, Sum




def home(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10)
    stock_by_category = Product.objects.values('category__name').annotate(total_stock=Sum('stock')).order_by('category__name')


    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'low_stock_products': low_stock_products,
        'stock_by_category': stock_by_category,
    }
    return render(request, 'main/home.html', context)
