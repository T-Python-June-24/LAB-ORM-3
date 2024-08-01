from django.core.mail import send_mail
from django.utils import timezone
from products.models import Product

def check_stock_and_expiry():
    low_stock_threshold = 10
    expiry_warning_days = 7

    today = timezone.now().date()
    
    low_stock_products = Product.objects.filter(stock_quantity__lte=low_stock_threshold)

    approaching_expiry_products = Product.objects.filter(
        expiry_date__lte=today + timezone.timedelta(days=expiry_warning_days)
    )

    message = "Low Stock Products:\n"
    for product in low_stock_products:
        message += f"{product.name} - Stock Quantity: {product.stock_quantity}\n"

    message += "\nApproaching Expiry Products:\n"
    for product in approaching_expiry_products:
        message += f"{product.name} - Expiry Date: {product.expiry_date}\n"

    
    send_mail(
        'Inventory Notifications',
        message,
        'your-email@gmail.com',  # From email
        ['manager-email@example.com'],  # To email
        fail_silently=False,
    )
