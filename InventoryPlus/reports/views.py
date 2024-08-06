from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
from products.models import Product
from django.http import HttpRequest
from suppliers.models import Supplier

# Create your views here.


def inventory_report(request: HttpRequest):
    
    # Inventory Report
    products = Product.objects.all()
    product_names = [product.name for product in products]
    stock_levels = [product.stock_quantity for product in products]

    inventory_fig = go.Figure(
        data=[go.Bar(x=product_names, y=stock_levels)],
        layout_title_text="Inventory Report"
    )
    inventory_plot_div = plot(inventory_fig, output_type='div')

    # Supplier Report
    suppliers = Supplier.objects.all()
    supplier_names = [supplier.name for supplier in suppliers]
    product_counts = [Product.objects.filter(supplier=supplier).count() for supplier in suppliers]

    supplier_fig = go.Figure(
        data=[go.Bar(x=supplier_names, y=product_counts)],
        layout_title_text="Supplier Report"
    )
    supplier_plot_div = plot(supplier_fig, output_type='div')

    return render(request, 'reports/reports.html', context={
        'inventory_plot_div': inventory_plot_div,
        'supplier_plot_div': supplier_plot_div
    })