from product.models import Product
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task




@shared_task
def check_Quantity_and_date():
    
    today = datetime.now()
    products = Product.objects.all()

    for product_date in products:
        if product_date.Expiration_date:
            date = product_date.Expiration_date -  timedelta(days=3)
            if today >= date  and not product_date.Notifications:
                product_date.Notifications = True
                product_date.save()
                subject = f'The {product_date.Name_Product} product is expired'
                message =  f'The {product_date.Name_Product} product is expired'
                from_email = settings.EMAIL_HOST_USER
                to_email = 'naif.n115811@gmail.com'
                send_mail(subject, message, from_email, [to_email])
        if product_date.Quantity_Product<=2:
            
            subject = f'The {product_date.Name_Product} product is about to expire'
            message = "maldfhsfd"
            from_email = settings.EMAIL_HOST_USER
            to_email = 'naif.n115811@gmail.com'
            send_mail(subject, message, from_email, [to_email])



            



