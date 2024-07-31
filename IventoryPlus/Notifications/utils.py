from django.core.mail import send_mail
from datetime import datetime, timedelta
from Product.models import Product
from .models import EmailRecipient 
import os

def check_low_stock():
    low_stock_threshold = 10  
    low_stock_products = Product.objects.filter(stock_quantity__lte=low_stock_threshold)
    return low_stock_products

def check_expiry_dates():
    today = datetime.today().date()
    upcoming_expiry_products = Product.objects.filter(expiration_date__lte=today + timedelta(days=7))
    return upcoming_expiry_products

def send_alerts():
    low_stock_products = check_low_stock()
    upcoming_expiry_products = check_expiry_dates()
    
    if low_stock_products.exists() or upcoming_expiry_products.exists():
        message = """
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    color: #333;
                    line-height: 1.6;
                }
                .title {
                    background-color: blue;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                }
                h2 {
                    color: #444;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background-color: #f9f9f9;
                    margin: 5px 0;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="title">Saqer™</div>
            <div>
        """
        
        if low_stock_products.exists():
            message += "<h2>Low Stock Alerts:</h2>"
            message += "<ul>"
            for product in low_stock_products:
                message += f"<li>{product.name}: {product.stock_quantity} units remaining</li>"
            message += "</ul>"
        
        if upcoming_expiry_products.exists():
            message += "<h2>Expiry Date Alerts:</h2>"
            message += "<ul>"
            for product in upcoming_expiry_products:
                message += f"<li>{product.name}: expires on {product.expiration_date}</li>"
            message += "</ul>"
        
        message += """
            </div>
        </body>
        </html>
        """
        
        recipients = [recipient.email for recipient in EmailRecipient.objects.all()]
        send_mail(
            'Inventory Alerts',
            message,
            os.getenv('DEFAULT_FROM_EMAIL'),
            recipients,
            fail_silently=False,
            html_message=message,
        )
