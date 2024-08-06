from django.shortcuts import render
from django.http import HttpRequest
from products.models import Product
from suppliers.models import Supplier
from django.utils.timezone import now
import plotly.graph_objs as go
import plotly.io as pio


# Create your views here.

def home_view(request: HttpRequest):
  # Product overview
  total_products = Product.objects.count()
  low_stock_items = Product.objects.filter(stock_quantity__lt=10).count()
  expired_items = Product.objects.filter(expiry_date__lt=now().date()).count()

  # Supplier overview
  total_suppliers = Supplier.objects.count()
  products_supplied = Product.objects.values('supplier').distinct().count()

  # Chart overview
  data = [
    go.Scatter(
      x=['Total Products', 'Low Stock Items', 'Expired Items'],
      y=[total_products, low_stock_items, expired_items],
      mode='lines+markers'
    )
  ]
  layout = go.Layout(
    title='Stock Statistics'
  )
  fig = go.Figure(data=data, layout=layout)
  plot_div = pio.to_html(fig, full_html=False)

  context = {
    'total_products': total_products,
    'low_stock_items': low_stock_items,
    'expired_items': expired_items,
    'total_suppliers': total_suppliers,
    'products_supplied': products_supplied,
    'plot_div': plot_div,
  }

  return render(request, "main/index.html", context)