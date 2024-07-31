from django.shortcuts import render
from Categories.models import Category
from Suppliers.models import Supplier
from Product.models import Product
from django.db import models
import plotly.graph_objs as go
import json

def dashboard(request):
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_categories = Category.objects.count()
    
    stock_status = sum([product.stock_quantity for product in Product.objects.all()]) / total_products if total_products else 0
    total_revenue = sum([product.price * product.stock_quantity for product in Product.objects.all()])
    average_product_price = Product.objects.aggregate(average_price=models.Avg('price'))['average_price'] or 0
    highest_price_product = Product.objects.order_by('-price').first()
    lowest_price_product = Product.objects.order_by('price').first()
    
    top_category = Category.objects.annotate(total_products=models.Count('product')).order_by('-total_products').first()
    lower_category = Category.objects.annotate(total_products=models.Count('product')).order_by('total_products').first()
    top_supplier = Supplier.objects.annotate(total_supplied=models.Count('product')).order_by('-total_supplied').first()
    category_distribution = Category.objects.annotate(product_count=models.Count('product')).values('name', 'product_count')
    lower_supplier = Supplier.objects.annotate(total_supplied=models.Count('product')).order_by('total_supplied').first()

    total_products_data = [go.Bar(
        x=['Products', 'Suppliers', 'Categories'],
        y=[total_products, total_suppliers, total_categories],
    )]
    total_suppliers_data = [go.Bar(
        x=['Categories', 'Revenue'],
        y=[average_product_price, total_revenue],
    )]
    category_labels = [cat['name'] for cat in category_distribution]
    category_values = [cat['product_count'] for cat in category_distribution]

    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_categories': total_categories,
        'stock_status': stock_status,
        'total_revenue': total_revenue,
        'high_price' : highest_price_product,
        'low_price' :  lowest_price_product,
        'average_product_price': average_product_price,
        
        'top_category': top_category.name if top_category else 'N/A',
        'top_supplier': top_supplier.name if top_supplier else 'N/A',
        
        'lower_category': lower_category.name if lower_category else 'N/A',
        'lower_supplier': lower_supplier.name if lower_supplier else 'N/A',

        'total_products_data': json.dumps([trace.to_plotly_json() for trace in total_products_data]),
        'total_suppliers_data': json.dumps([trace.to_plotly_json() for trace in total_suppliers_data]),
        'category_labels': json.dumps(category_labels),
        'category_values': json.dumps(category_values)
    }

    return render(request, 'Reports/dashboard.html', context)
