

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Product
from .utils import send_low_stock_alert#, send_expiry_alert




@shared_task
def send_low_stock_alerts_task():
    low_stock_products = Product.objects.filter(stock__lt=10)
    for product in low_stock_products:
        send_low_stock_alert(product)





# @shared_task
# def send_expiry_alerts_task():
#     expiry_date = timezone.now() + timedelta(days=30)
#     expiring_products = Product.objects.filter(expiry_date__lte=expiry_date)
#     if expiring_products.exists():
#         send_expiry_alert(expiring_products)
