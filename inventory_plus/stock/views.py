from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Stock
from .utils import check_stock_and_expiry

def stock_list(request):
    stocks = Stock.objects.all()
    total_stock_quantity = stocks.aggregate(total_stock_quantity=Sum('quantity'))['total_stock_quantity'] #aggregation
    context = {
        'stocks': stocks,
        'total_stock_quantity': total_stock_quantity if total_stock_quantity else 0,
    }
    return render(request, 'stock/stock_list.html', context)

def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    context = {'stock': stock}
    return render(request, 'stock/stock_detail.html', context)

def stock_dashboard(request):
    check_stock_and_expiry()
    stocks = Stock.objects.all()
    context = {'stocks': stocks}
    return render(request, 'inventory_plus/home.html', context)
