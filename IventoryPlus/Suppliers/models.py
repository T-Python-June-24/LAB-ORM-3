from django.db import models

class Supplier(models.Model):
    PRODUCT_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
        ('Tools', 'Tools'),
        ('Sports', 'Sports'),
        ('Beauty', 'Beauty'),
        ('Health', 'Health'),
        ('Other', 'Other'),
    ]
    
    RATING_CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    ]

    SERVICE_CHOICES = [
        
    ('Delivery', 'Delivery'),
    ('Installation', 'Installation'),
    ('Warranty', 'Warranty'),
    ('Support', 'Support'),
    ('Maintenance', 'Maintenance'),
    ('Repair', 'Repair'),
    ('Consultation', 'Consultation'),
    ('Customization', 'Customization'),
    ('Upgrades', 'Upgrades'),
    ('Training', 'Training'),
    ('Inspection', 'Inspection'),
    ('Other', 'Other'),
    ]

    
    RETURN_POLICY_CHOICES = [
        ('No Returns', 'No Returns'),
        ('Exchange Only', 'Exchange Only'),
        ('Refund Only', 'Refund Only'),
        ('Exchange or Refund', 'Exchange or Refund'),
        ('Other', 'Other'),

    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    logo = models.ImageField(upload_to='supplier_logos/', default='supplier_logos/default.jpg')
    phone_number = models.CharField(max_length=18)
    website = models.URLField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person_job_title = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    policy = models.CharField(max_length=50, choices=RETURN_POLICY_CHOICES, blank=True, null=True)
    supplied_products = models.CharField(max_length=50, choices=PRODUCT_CHOICES, blank=True, null=True)
    services_offered = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, null=True)

    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
