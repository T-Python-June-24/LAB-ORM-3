

from django.core.mail import send_mail
from django.conf import settings


def send_low_stock_alert(product):
    subject = f'Low Stock Alert: {product.name}'
    message = f'The stock level for {product.name} is low. Only {product.stock} items left in stock.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ray.nasser.f@gmail.com', 'ray.nasser@outlook.com']
    send_mail(subject, message, email_from, recipient_list)



# def send_expiry_alert(expiring_products):
#     product_list = "\n".join([f"{p.name}: {p.expiry_date}" for p in expiring_products])
#     send_mail(
#         'Expiry Date Alert',
#         f'The following products are nearing expiry:\n{product_list}',
#         'from@....com',
#         ['to@....com']
#     )