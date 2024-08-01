from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from products.models import Product

def home(request):
    low_stock_threshold = 5
    
    expiry_threshold_date = timezone.now() + timedelta(days=30)

    low_stock_products = Product.objects.filter(stock_quantity__lte=low_stock_threshold)
    
    approaching_expiry_products = Product.objects.filter(expiry_date__lte=expiry_threshold_date)

    context = {
        'low_stock_products': low_stock_products,
        'approaching_expiry_products': approaching_expiry_products,
    }
    
    return render(request, 'home.html', context)
