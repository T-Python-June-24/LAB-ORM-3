from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def check_product_status(product):
    status = {
        'is_low_stock': False,
        'is_out_of_stock': False,
        'is_expired': False,
        'is_about_to_expire': False,

    }
    
    now = timezone.now().date()
    
    # Check if the product is out of stock
    if product.quantity == 0:
        status['is_out_of_stock'] = True
    # Check if the product is low on stock
    elif product.quantity <= product.low_stock_threshold:
        status['is_low_stock'] = True
        logger.debug(f"Product {product.name} marked as low stock. Quantity: {product.quantity}, Threshold: {product.low_stock_threshold}")
    
    # Check if the product has expired
    if product.expiry_date and product.expiry_date <= now:
        status['is_expired'] = True
    
    # Check if the product is about to expire (e.g., within 30 days)
    expiry_warning_days = getattr(settings, 'EXPIRY_WARNING_DAYS', 5)
    if product.expiry_date and product.expiry_date <= (now + timedelta(days=expiry_warning_days)):
        status['is_about_to_expire'] = True
    return status

def send_product_notification(product):
    status = check_product_status(product)
    
    if status['is_expired']:
        send_styled_email(
            subject=f'URGENT: Product Expired - {product.name}',
            content=get_expired_email_content(product),
            recipient_list=[settings.MANAGER_EMAIL]
        )
    elif status['is_about_to_expire']:
        send_styled_email(
            subject=f'Warning: Product Expiring Soon - {product.name}',
            content=get_expiring_soon_email_content(product),
            recipient_list=[settings.MANAGER_EMAIL]
        )
    elif status['is_out_of_stock']:
        send_styled_email(
            subject=f'Alert: Product Out of Stock - {product.name}',
            content=get_out_of_stock_email_content(product),
            recipient_list=[settings.MANAGER_EMAIL]
        )
    elif status['is_low_stock']:
        send_styled_email(
            subject=f'Notice: Low Stock - {product.name}',
            content=get_low_stock_email_content(product),
            recipient_list=[settings.MANAGER_EMAIL]
        )


def send_styled_email(subject, content, recipient_list):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #4a90e2;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 30px;
            }}
            h1 {{
                color: #4a90e2;
                margin-top: 0;
            }}
            .highlight {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .action {{
                display: inline-block;
                background-color: #4a90e2;
                color: #ffffff;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
                transition: background-color 0.3s ease;
            }}
            .action:hover {{
                background-color: #357abd;
            }}
            .footer {{
                background-color: #f8f8f8;
                padding: 15px;
                text-align: center;
                font-size: 0.9em;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{subject}</h1>
            </div>
            <div class="content">
                {content}
            </div>
            <div class="footer">
                This is an automated message from your Inventory Management System.
            </div>
        </div>
    </body>
    </html>
    """
    
    send_mail(
        subject=subject,
        message='',
        html_message=html_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )

def get_expired_email_content(product):
    return f"""
    <h2>Product Expired</h2>
    <p>The following product has expired:</p>
    <p><span class="highlight">{product.name}</span></p>
    <p><strong>Expiry Date:</strong> {product.expiry_date}</p>
    <p>Please take immediate action to remove this product from inventory.</p>
    <a href="https://ims.ahmed-haz.com/products/{product.id}/" class="action">View Product</a>
    """

def get_expiring_soon_email_content(product):
    return f"""
    <h2>Product Expiring Soon</h2>
    <p>The following product is about to expire:</p>
    <p><span class="highlight">{product.name}</span></p>
    <p><strong>Expiry Date:</strong> {product.expiry_date}</p>
    <p>Please take action to manage this product before it expires.</p>
    <a href="https://ims.ahmed-haz.com/products/{product.id}/" class="action">View Product</a>
    """

def get_out_of_stock_email_content(product):
    return f"""
    <h2>Product Out of Stock</h2>
    <p>The following product is now out of stock:</p>
    <p><span class="highlight">{product.name}</span></p>
    <p><strong>Current Quantity:</strong> 0</p>
    <p>Please reorder this product as soon as possible.</p>
    <a href="https://ims.ahmed-haz.com/products/{product.id}/" class="action">Reorder Product</a>
    """

def get_low_stock_email_content(product):
    return f"""
    <h2>Low Stock Alert</h2>
    <p>The following product is running low on stock:</p>
    <p><span class="highlight">{product.name}</span></p>
    <p><strong>Current Quantity:</strong> {product.quantity}</p>
    <p><strong>Low Stock Threshold:</strong> {product.low_stock_threshold}</p>
    <p>Consider reordering this product soon.</p>
    <a href="https://ims.ahmed-haz.com/products/{product.id}/" class="action">View Product</a>
    """
