from django.shortcuts import render,redirect
from django.http import HttpRequest
from products.models import Product
from categories.models import Category
from suppliers.models import Supplier
import humanize
from django.utils.timezone import now
from datetime import date, timedelta, timezone
import math
from django.http import HttpRequest
import os 
from dotenv import load_dotenv
from django.core.mail import send_mail
from email.message import EmailMessage
import ssl
import smtplib
from django.db.models import Avg, Count, Min, Sum,F,Q
  
# Create your views here.
def home_view(request:HttpRequest):
    products=Product.objects.all()
    categories=Category.objects.all()
    products_count=products.count()
    suppliers_count=Supplier.objects.all().count()
    added_today_suppliers=Supplier.objects.filter(added=now().date())   
    added_today_products=products.filter(added__gte=now().date()) 
    prod=Product.objects.annotate(total_price=F("price")*F("stock_level"))
    total_sum=prod.aggregate(total_sum=Sum('total_price'))['total_sum']
    formatted_total_value = humanize.intcomma(total_sum) 


    for index, supplier in enumerate(added_today_suppliers):
        added_today_suppliers[index].percentage = math.floor((supplier.product_set.all().count()/products_count)*100)


    # tracking low stock products and alerts emails to manager about low stock 
    need_to_notify=[]
    need_to_notify_expiration = []
    products=Product.objects.all()
    for product in products:
        if product.stock_level<=10 and not product.notified:
            need_to_notify.append(product)
            product.notified=True
            product.save()
        elif product.stock_level>10 and product.notified:
            product.notified=False
            product.save()
         # Expiration alerts
        if product.expirment and product.expirment <= now().date() + timedelta(days=5) and not product.notifeied_exieration:
            need_to_notify_expiration.append(product)
            product.notifeied_exieration = True
            product.save()
        elif product.expirment and product.expirment > now().date() + timedelta(days=5) and product.notifeied_exieration:
            product.notifeied_exieration = False
            product.save()


    manager_email = os.getenv("EMAIL_MANAGER")  

    for product in need_to_notify:
        subject = f"Low Stock Alert for {product.name}"
        body = f"""
        <html>
        <body>
            <h2 style="color: #d9534f;">Low Stock Alert!</h2>
            <div style="display:flex; flex-direction:column; justfiy-content:center; align-items:center; background-color:white; color:black;"><p style="font-size: 16px;">The product <strong>{product.name}</strong> is running low on stock.</p>
            <p style="font-size: 20px;">Current stock level: <strong>{product.stock_level}</strong>.</p>
            <p style="font-size: 14px; color: #999;">Please take appropriate action to restock the product.</p><div/>
            <footer>
                <p style="font-size: 12px; color: #aaa; bacground-color:#EEEEEE">This is an automated message from InventoryPlus.</p>
            </footer>
        </body>
        </html>
        """

        try:
            send_mail(
                subject,
                "",  # Leave the plain text part empty if you are sending HTML
                os.getenv("EMAIL_HOST_USER"),
                [manager_email],
                fail_silently=False,
                html_message=body  # Use the html_message parameter to send HTML content
            )
            print("Email sent successfully. for stock level")
        
        except Exception as e:
            print(e)
            print("Failed to send email")

      
    # Send expiration notifications
    for product in need_to_notify_expiration:
        
        subject = f"Expiration Alert for {product.name}"
        print(subject)
        body = f"""
        <html>
        <body>
            <h2 style="color: #d9534f;">Expiration Alert!</h2>
            <p style="font-size: 16px;">The product <strong>{product.name}</strong> is nearing its expiration date.</p>
            <p style="font-size: 16px;">Expiration date: <strong>{product.expirment}</strong>.</p>
            <p style="font-size: 14px; color: #999;">Please review the product's status and take appropriate action.</p>
            <footer>
                <p style="font-size: 12px; color: #aaa;">This is an automated message from InventoryPlus.</p>
            </footer>
        </body>
        </html>
        """
        try:
            send_mail(
                subject,
                "",  # Leave the plain text part empty if you are sending HTML
                os.getenv("EMAIL_HOST_USER"),
                [manager_email],
                fail_silently=False,
                html_message=body
            )
            print(f"Expiration email sent successfully for {product.name}.")
        except Exception as e:
            print(e)
            print(f"Failed to send expiration email for {product.name}.")
            

    
    return render(request,"main/index.html",{
                                             "total_value":formatted_total_value,
                                             "products_count":products_count,
                                             "suppliers_count":suppliers_count,
                                             "suppliers":added_today_suppliers,
                                             "products":added_today_products,
                                             "categories":categories,
                                             })



def search_view(request: HttpRequest):
    search_words = request.GET.get("search", "")
    filter_type = request.GET.get("filter", "all")

    products_result = []
    categories_result = []
    suppliers_result = []

    if search_words:
        if filter_type == "all":
            products_result = Product.objects.filter(name__icontains=search_words)
            categories_result = Category.objects.filter(name__icontains=search_words)
            suppliers_result = Supplier.objects.filter(name__icontains=search_words)
        elif filter_type == "product":
            products_result = Product.objects.filter(name__icontains=search_words)
        elif filter_type == "supplier":
            suppliers_result = Supplier.objects.filter(name__icontains=search_words)
        elif filter_type == "category":
            categories_result = Category.objects.filter(name__icontains=search_words)

    context = {
        "products": products_result,
        "categories": categories_result,
        "suppliers": suppliers_result,
        "search": filter_type,
    }

    return render(request, "main/search.html", context)

def notifie_email(request:HttpRequest):
    need_to_notifie=[]
    products=Product.objects.all()
    for product in products:
        if product.stock_level<=10 and not product.notified:
            need_to_notifie.append(product)
            product.notified=True
            product.save()
    
