from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from product.models import Product
from category.models import Category
from supplier.models import Supplier


# Create your views here.
def index_view(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'main/index.html', {'products': products, 'categories': categories, 'suppliers': suppliers})
