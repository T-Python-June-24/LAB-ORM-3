from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from .models import Product
from suppliers.models import Supplier
from categories.models import Category
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
import pandas as pd
from django. contrib import messages

# Create your views here.
def products_view(request:HttpRequest):
    products=Product.objects.all()
    return render(request,"products/product.html",{"products":products})
def add_product_view(request:HttpRequest)->render:
    try:
            product=Product.objects.all()
            suppliers=Supplier.objects.all()
            categories=Category.objects.all()
            if request.method=="POST":
                name=request.POST['name']
                description=request.POST["description"]
                stock_level=request.POST['stock_level']
                if request.POST["expirment_date"]=="":
                    expirment=None
                else:
                    expirment=request.POST["expirment_date"]
                
                price=request.POST["price"]
                category=Category.objects.get(pk=request.POST["category"]) if request.POST["category"] !="" else None
                
                new_product=Product(name=name,description=description,stock_level=stock_level,expirment=expirment,price=price,category=category)
                new_product.save()
                if "supplier" in  request.POST:
                    new_product.supplier.set(request.POST.getlist("supplier"))
                response = redirect('products:products_view')
                messages.success(request,"The product added successfully","success")
                return response
    except Exception as e:
        messages.error(request,"there's something went wrong colu't remove the product ","error")



    return render(request,"products/add_product.html",{"suppliers":suppliers,"categories":categories,"product":product})

def update_product(request,product_id):
    try:
        product=Product.objects.get(pk=product_id)
        suppliers=Supplier.objects.all()
        categories=Category.objects.all()
        if request.method=="POST":
            product.name=request.POST['name']
            product.description=request.POST["description"]
            product.stock_level=request.POST['stock_level']
            if request.POST["expirment_date"]=="":
                product.expirment=None
            else:
                product.expirment=request.POST["expirment_date"]
            
            product.price=request.POST["price"]
            product.category=Category.objects.get(pk=request.POST["category"]) if "category" in request.POST else None
            product.save()
            product.supplier.set(request.POST.getlist("supplier"))
            response = redirect(request.GET.get("next", "/"))
            messages.success(request,"Succussfully the product updtaed","success")
            return response
    except Exception as e:
            messages.error("there's something went wrong could't update a product","error")

    return render(request,"products/update_product.html",{"product":product,"suppliers":suppliers,"categories":categories})
    
def delete_product(request:HttpRequest,product_id):
    try:
        product=Product.objects.get(pk=product_id)
        product.delete()
        response = redirect(request.GET.get("next", "/"))
        messages.success(request,"product delteded succfully")
        return response
    except Exception as e:
        messages.error(request,"something went wrong coldun't delete a product","error")

def import_data(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'products/import_form.html', {'error': 'No file uploaded'})

        file = request.FILES['file']
        print("File uploaded successfully")

        if not file.name.endswith('.csv'):
            return render(request, 'products/import_form.html', {'error': 'File is not a CSV'})
        print("File is a CSV")

        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            print("CSV read into DataFrame successfully")

            # Validate required columns
            required_columns = ['name', 'description', 'category', 'supplier', 'stock_level', 'expirment', 'price']
            for col in required_columns:
                if col not in df.columns:
                    error_message = f'Missing column: {col}'
                    print(error_message)
                    return render(request, 'products/import_form.html', {'error': f'Missing column: {col}'})
            print("All required columns are present")

            # Process the DataFrame
            for index, row in df.iterrows():
                print(f"Processing row {index + 1}: {row.to_dict()}")
                
                # Get or create category
                category, created = Category.objects.get_or_create(name=row['category'])
                print(f"Category '{row['category']}' - {'created' if created else 'retrieved'}")

                # Get or create suppliers
                supplier_names = row['supplier'].split(';')
                suppliers = []
                for supplier_name in supplier_names:
                    supplier, created = Supplier.objects.get_or_create(name=supplier_name)
                    suppliers.append(supplier)
                    print(f"Supplier '{supplier_name}' - {'created' if created else 'retrieved'}")

                # Handle the expirment field with different date formats
                expirment_value = None
                date_formats = ['%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y']
                for date_format in date_formats:
                    try:
                        expirment_value = pd.to_datetime(row['expirment'], format=date_format, errors='raise').date()
                        print(f"Expirment value parsed successfully: {expirment_value}")
                        break
                    except (ValueError, TypeError):
                        continue
                if expirment_value is None:
                    print(f"Expirment value is None or invalid for row {index + 1}")

                # Create or update product
                try:
                    product, created = Product.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'category': category,
                            'stock_level': int(row['stock_level']),
                            'expirment': expirment_value,
                            'price': int(row['price']),
                        }
                    )
                    
                    if created:
                        print(f"Created new product: {product.name}")
                    else:
                        print(f"Updated existing product: {product.name}")

                    # Add suppliers to the product
                    product.supplier.set(suppliers)
                    product.save()
                    print(f"Suppliers assigned to product: {product.name}")
                except Exception as e:
                    print(f"Error creating/updating product '{row['name']}': {e}")

            print("All data processed and saved")
            return redirect('products:products_view')

        except Exception as e:
            print(f"Error processing file: {e}")
            return render(request, 'products/import_form.html', {'error': str(e)})

    return redirect('products:products_view')

def export_data(request):
    # Get all products
    products = Product.objects.all()

    # Create a list of dictionaries from the queryset
    data = []
    for product in products:
        suppliers = ', '.join([supplier.name for supplier in product.supplier.all()])
        data.append({
            'name': product.name,
            'description': product.description,
            'category': product.category.name if product.category else '',
            'supplier': suppliers,
            'stock_level': product.stock_level,
            'expirment': product.expirment,
            'price': product.price,
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Convert the DataFrame to a CSV string
    csv_data = df.to_csv(index=False)

    # Create an HTTP response with the CSV data
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=products.csv'

    return response