from django.shortcuts import redirect
import pandas as pd
from openpyxl.drawing.image import Image
import io
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import csv
from django.utils import timezone
from django.http import HttpResponse , HttpRequest
from product.models import Product
from Category.models import Category
from Supplier.models import Supplier
import matplotlib.pyplot as plt
# Create your views here.

def upload_csv(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                data = file.read().decode('utf-8')
                csv_file = io.StringIO(data)
                reader = csv.reader(csv_file)
                
                header = next(reader)  
                if len(header) != 9:
                    return HttpResponse("CSV file header format is incorrect. Expected 9 columns.")
                
                for row in reader:
                    if len(row) == 9:
                        name, description, category_id, supplier_ids, price, quantity, expiration_date, image_url, status = row
                        
                        
                        status = status.lower() in ['true', '1', 'yes']
                        
                        try:
                            category = Category.objects.get(id=int(category_id))
                            supplier_ids = list(map(int, supplier_ids.split(',')))  
                            suppliers = Supplier.objects.filter(id__in=supplier_ids)
                            if image_url:
                                response = requests.get(image_url)
                                if response.status_code == 200:
                                    image_name = image_url.split('/')[-1]
                                    image_path = default_storage.save(f'images_Product/{image_name}', ContentFile(response.content))
                                else:
                                    image_path = 'images_product/default.png'
                            else:
                                image_path = 'images_product/default.png'
                            product = Product.objects.create(
                                Name_Product=name,
                                Description_product=description,
                                Category_product=category,
                                Price_Product=float(price),
                                Quantity_Product=int(quantity),
                                Expiration_date=expiration_date if expiration_date else None,
                                Images_Product=image_url,
                                Status_Product=status  
                            )
                            
                            
                            product.Supplier_product.set(suppliers)
                            
                        except Category.DoesNotExist:
                            return HttpResponse(f"Category with id {category_id} does not exist.")
                        except Supplier.DoesNotExist:
                            return HttpResponse(f"One or more Suppliers with the given IDs do not exist.")
                        except ValueError as e:
                            return HttpResponse(f"Invalid value: {e}.")
                    else:
                        return HttpResponse("Row format is incorrect. Expected 9 columns.")
                
                return redirect("Manger:Manger")
            else:
                return HttpResponse("Unsupported file type. Please upload a CSV file.")
        else:
            return HttpResponse("No file uploaded.")
    else:
        return redirect("Manger:Manger")

def download_sample(request):
    
    fields = ['Name_Product', 'Description_product', 'Category_id', 'Supplier_ids', 'Price_Product', 'Quantity_Product', 'Expiration_date', 'Image_URL', 'Status_Product']
    
   
    data = [
        ['Sample Product', 'This is a sample product', '1', '1,2', '19.99', '10', '2025-12-31', 'https://example.com/sample_image.jpg', 'True'],
    ]
    
  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sample_products.csv'
    
    writer = csv.writer(response)
    writer.writerow(fields)
    writer.writerows(data)
    
    return response

def generate_report(request:HttpRequest):
    metrics_data = {
        'Metric': [
            'Total Products', 
            'Total Suppliers', 
            'Total Categories', 
            'Expired Products', 
            'Total Products Expired'
        ],
        'Value': [
            Product.objects.count(),
            Supplier.objects.count(),
            Category.objects.count(),
            Product.objects.filter(Expiration_date__lt=timezone.now()).count(),
            Product.objects.filter(Quantity_Product=0).count()
        ]
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    
    products_data = Product.objects.all().values(
        'Name_Product', 'Status_Product', 'Quantity_Product', 
        'Price_Product', 'Expiration_date', 'Created_at', 
        'Images_Product', 'Description_product', 
        'Category_product__name_Category', 'Supplier_product__name_Supplier'
    )
    products_df = pd.DataFrame(products_data)
    
    suppliers_data = Supplier.objects.all().values(
        'name_Supplier', 'logo_Supplier', 'email_supplier', 
        'number_phone', 'address_Supplier', 'website_Supplier'
    )
    suppliers_df = pd.DataFrame(suppliers_data)
    
    categories_data = Category.objects.all().values(
        'name_Category', 'description_Category'
    )
    categories_df = pd.DataFrame(categories_data)
    
    fig, ax = plt.subplots()
    ax.bar(metrics_data['Metric'], metrics_data['Value'], color='skyblue')
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    ax.set_title('Product Report Metrics')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = buf.getvalue() 
    buf.close()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report.xlsx'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
        
    
        products_df.to_excel(writer, sheet_name='Products', index=False)
        
   
        suppliers_df.to_excel(writer, sheet_name='Suppliers', index=False)
        
        categories_df.to_excel(writer, sheet_name='Categories', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['Metrics']
        
        image_buf = io.BytesIO(image_data)
        image = Image(image_buf)
        worksheet.add_image(image, 'E5')  
    
    return response
def download_suppliers_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=suppliers_report.csv'
    
    writer = csv.writer(response)
    
    writer.writerow([
        'ID', 
        'Name', 
        'Logo URL', 
        'Email', 
        'Phone Number', 
        'Address', 
        'Website'
    ])
    
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        writer.writerow([
            supplier.id, 
            supplier.name_Supplier, 
            supplier.logo_Supplier.url if supplier.logo_Supplier else 'No logo',
            supplier.email_supplier,
            supplier.number_phone,
            supplier.address_Supplier,
            supplier.website_Supplier or 'No website'
        ])
    
    return response