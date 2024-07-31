from django.shortcuts import render , redirect
from django.http import HttpRequest 
from product.models import Product
from Category.models import Category
from Supplier.models import Supplier
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum , Count
# Create your views here.
def search_manger(request:HttpRequest):
    if request.method == 'GET':
        search_by = request.GET.get('search_by', '')
        word_search = request.GET.get('search_term', '')

        if search_by == 'product':
           
            products = Product.objects.filter(Name_Product__icontains=word_search)
            count_product = products.count()
            return render(request, 'pages/views_search.html', {
                'views_product': products,
                'count_product': count_product,
                'word_search': word_search
            })
        
        elif search_by == 'Category':
            
            categories = Category.objects.filter(name_Category__icontains=word_search)
            count_category = categories.count()
            
            
            products_in_categories = Product.objects.filter(Category_product__in=categories)
            count_products_in_categories = products_in_categories.count()

            return render(request, 'pages/views_search.html', {
                'category': categories,
                'views_product': products_in_categories,
                'count_category': count_category,
                'count_products_in_categories': count_products_in_categories,
                'word_search': word_search
            })
        
        elif search_by == 'Supplier':
          
            suppliers = Supplier.objects.filter(name_Supplier__icontains=word_search)
            count_supplier = suppliers.count()

           
            products_in_suppliers = Product.objects.filter(Supplier_product__in=suppliers)
            count_products_in_suppliers = products_in_suppliers.count()

            return render(request, 'pages/views_search.html', {
                'supplier': suppliers,
                'views_product': products_in_suppliers,
                'count_supplier': count_supplier,
                'count_products_in_suppliers': count_products_in_suppliers,
                'word_search': word_search
            })
    
    return redirect('Manger:search_manger')
def Manger(request:HttpRequest):
    Quantity_product = Product.objects.filter(Quantity_Product__lt = 2).exclude(Quantity_Product=0)
    out_product = Product.objects.filter(Status_Product = 0)
    update_product = Product.objects.all().order_by('-Created_at')
    number_product = Product.objects.count()
    number_Supplier = Supplier.objects.count()
    number_Category = Category.objects.count()
    sold_out_product = Product.objects.filter(Quantity_Product=0).count()
    running_out_product = Product.objects.filter(Quantity_Product__lt=2).exclude(Quantity_Product=0).count()
    category = Category.objects.all()
    num_prosuct = update_product.aggregate(Sum('Price_Product'))

    if number_product == 0:
        sold = 0
        running = 0
    else:
        sold = (sold_out_product / number_product )*100
        running = (running_out_product / number_product )*100

    return render(request , 'pages/pages_manger.html' ,
                  {"Quantity_product":Quantity_product ,
                   "out_product":out_product , 
                   "update_product":update_product,
                   "number_product":number_product,
                   "number_supplier":number_Supplier,
                   "number_category":number_Category,
                   'sold':sold,
                   "running":running,
                   "num_prosuct":num_prosuct['Price_Product__sum']
                   
                   })


def manger_product(request:HttpRequest):
    category = Category.objects.all()
    views_supplier = Supplier.objects.all()
    views_product = Product.objects.all().select_related('Category_product').prefetch_related('Supplier_product').annotate(supplier_count=Count('Supplier_product'))

    page_number = request.GET.get('page', 1)
    page_product = Paginator(views_product , 3)
    product_page = page_product.get_page(page_number)
    views_product = views_product.annotate(supplier_count = Count('Supplier_product'))
    return render(request , "pages/views_product.html" , {"views_product":product_page,"category":category , "views_supplier":views_supplier})

def manger_Category(request:HttpRequest):
    category = Category.objects.all()
    return render(request , "pages/views_category.html" , {"categorys":category})
def manger_supplier(request:HttpRequest):
    supplier = Supplier.objects.all()
    
    return render(request , 'pages/views_supplier.html' ,{'suppliers':supplier})
    
def search(request: HttpRequest):
    if request.method == 'GET':
        type_search = request.GET.get('type_search', '')
        if type_search == 'product':
            word_search = request.GET.get('search', '')
            products = Product.objects.filter(Name_Product__icontains=word_search)
            count_product = products.count()
            return render(request, 'pages/views_product.html', {
                'views_product': products,
                'count_product': count_product,
                'word_search': word_search
            })
        elif type_search == 'Category':
            word_search = request.GET.get('search', '')
            category = Category.objects.filter(name_Category__icontains=word_search)
            count_category = category.count()
            return render(request, 'pages/views_category.html', {
                'category': category,
                'count_category': count_category,
                'word_search': word_search
            })
        elif  type_search =="Supplier":
            word_search = request.GET.get('search', '')
            supplier = Supplier.objects.filter(name_Supplier__icontains=word_search)
            count_Supplier = supplier.count()
            return render(request, 'pages/views_Supplier.html', {
                'supplier': supplier,
                'count_Supplier': count_Supplier,
                'word_search': word_search
            })
            
    return redirect('Manger:manger_product')
def info_supplier(request:HttpRequest , supplier_id):
    view_supplier = Supplier.objects.get(pk=supplier_id)
    products = Product.objects.filter(Supplier_product__id=supplier_id)
    return render(request , 'pages/views_info_supplier.html' , {"supplier":view_supplier , "products":products})