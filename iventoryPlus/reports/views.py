from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.
from products.models import Product
from categories.models import Category
from suppliers.models import Supplier 
def reports_view(request:HttpRequest):
    suppliers=Supplier.objects.all()
    No_products=[]
    products=Product.objects.all()
    for supplier in suppliers:
        numbers=Product.objects.filter(supplier=supplier).count()
        if numbers:
            No_products.append(numbers)

    data={"suppliers":suppliers,"No_products":No_products,"products":products}
    return render(request,"reports/report.html",data)