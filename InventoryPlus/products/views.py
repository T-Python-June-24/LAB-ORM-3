from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .forms import ProductForm
from .models import Category,Supplier,Product
from django.core.mail import send_mail
import csv
from .forms import CSVUploadForm
from django.contrib import messages
from django.core.files.storage import default_storage




# Create your views here.


def add_product_view(request:HttpRequest):

    product_form = ProductForm()

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('main:home_view')
        else:
            print("not valid form", product_form.errors)
        # category = Category.objects.get(id=request.POST["category"])
        # new_product = Product(product_name=request.POST["product_name"], description=request.POST["description"], category=category, stock_level=request.POST["stock_level"], expiry_date=request.POST["expiry_date"], image=request.FILES["image"])
        # new_product.save()
        # new_product.suppliers.set(request.POST.getlist("suppliers"))
        # return redirect('main:home_view')
    
    return render(request, "products/add_product.html", {"product_form":product_form, "categories":categories, "suppliers": suppliers})

def all_products_view(request:HttpRequest, type, product_param):
    # products = Product.objects.filter(stock_level__gte=3).order_by("-expiry_date")
    # products = Product.objects.filter(stock_level__gte=3).exclude(product_name__contains="iphon11").order_by("-expiry_date")
    
    # if  Category.objects.filter(supplier_name=supplier_name).exists():
    #     products = Product.objects.filter(suppliers__supplier_name__in=[supplier_name]).order_by("-expiry_date")
    # elif supplier_name == "all":
    #     products = Product.objects.all().order_by("-expiry_date")
    # else:
    #     products = []

    if product_param == "all":
        products = Product.objects.all().order_by("-expiry_date")
        return render(request, "products/all_products.html", {"products":products, "product_param":product_param, 'type':type})
    elif type =="category_name":
        products = Product.objects.filter(category__name = product_param).order_by("-expiry_date")
        return render(request, "products/all_products.html", {"products":products, "product_param":product_param, 'type':type})
    elif type == "supplier_id":
        products = Product.objects.filter(suppliers__id__in=[product_param]).order_by("-expiry_date")
        supplier  = Supplier.objects.get(pk=product_param)
        return render(request, "products/all_products.html", {"products":products, "product_param":product_param, 'type':type, 'supplier':supplier})
    


def product_detail_view(request:HttpRequest, product_id:int):

    product = Product.objects.get(pk=product_id)
    

    return render(request, 'products/product_detail.html', {"product" : product})


def update_product_view(request:HttpRequest, product_id:int):

    product = Product.objects.get(pk=product_id)
    product_suppliers = product.suppliers.all()
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()
    

    low_stock_products = Product.objects.filter(stock_level__lte=10)
    product.save()
    flag =True
    if low_stock_products.exists() :
        product_names = ', '.join(product.product_name for product in low_stock_products)
        send_mail(
            subject='Low Stock Alert',
            message=f'The following products are low on stock: {product_names}.',
            from_email='ifonei@hotmail.com',  #a valid sender email
            recipient_list=['ifonei100@gmail.com'],
            fail_silently=False,
        )


    if request.method == "POST":
        #using ProductForm for updating
        product_form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if product_form.is_valid():
             product_form.save()
        else:
            print( product_form.errors)
        ##basic update
        # product.name = request.POST["name"]
        # product.description = request.POST["description"]
        # product.expiry_date = request.POST["expiry_date"]
        # product.supplier = request.POST["supplier"]
        # if "image" in request.FILES: product.image = request.FILES["image"]
        # product.save()

        return redirect("products:product_detail_view", product_id=product.id)

    return render(request, "products/update_product.html", {"product":product,"suppliers": suppliers ,"product_suppliers": product_suppliers, "categories": categories})

def delete_product_view(request:HttpRequest, product_id:int):

    product = Product.objects.get(pk=product_id)
    product.delete()

    return redirect("main:home_view")


def search_products_view(request:HttpRequest):

    if "search" in request.GET and len(request.GET["search"]) >= 2:
        products = Product.objects.filter(product_name__contains=request.GET["search"])

        if "order_by" in request.GET and request.GET["order_by"] == "stock_level":
            products = products.order_by("-stock_level")
        elif "order_by" in request.GET and request.GET["order_by"] == "expiry_date":
            products = products.order_by("-expiry_date")
    else:
        products = []


    return render(request, "products/search_products.html", {"products" : products})



def export_products_csv_view(request):
    # Create the HttpResponse object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['product_name', 'description', 'expiry_date', 'stock_level', 'category', 'suppliers', 'image'])

    # Write the product data
    products = Product.objects.all()
    for product in products:
        writer.writerow([
            product.product_name,
            product.description,
            product.expiry_date,
            product.stock_level,
            product.category.name if product.category else '',  # Ensure category field is correctly handled
            ', '.join([supplier.supplier_name for supplier in product.suppliers.all()]),  
            product.image.url if product.image else ''
        ])

    return response





def import_products_csv_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'The uploaded file is not a CSV file.')
                return redirect('products:csv_products.html')
            
            try:
                file_content = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(file_content)

                for row in reader:
                    category = Category.objects.get(id=row['category']) if row['category'] else None
                    suppliers = Supplier.objects.filter(id__in=row['suppliers'].split(',')) if row['suppliers'] else Supplier.objects.none()

                    product = Product(
                        product_name=row['product_name'],
                        description=row['description'],
                        expiry_date=row['expiry_date'] or None,
                        stock_level=row['stock_level'],
                        category=category,
                        image=row['image']
                    )
                    product.save()
                    product.suppliers.set(suppliers)
                    product.save()
                
                messages.success(request, 'Products imported successfully!')
            except Exception as e:
                messages.error(request, f'Error importing products: {e}')
            
            return redirect('products:import_products_csv_view')
    else:
        form = CSVUploadForm()

    return render(request,'products:csv_products.html', {'form': form})

