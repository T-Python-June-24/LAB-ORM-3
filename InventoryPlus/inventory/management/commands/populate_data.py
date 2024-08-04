from django.core.management.base import BaseCommand
from inventory.models import Category, Supplier, Product

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            'Smartphones', 'Laptops', 'Tablets', 'Televisions', 'Cameras', 'Audio Equipment', 
            'Accessories', 'Smartwatches', 'Gaming Consoles', 'Headphones', 'Printers', 
            'Monitors', 'Networking Devices', 'Home Appliances'
        ]
        for name in categories:
            Category.objects.get_or_create(name=name)
        
        # Create suppliers
        suppliers = [
            {
                'name': 'Tech World',
                'contact_email': 'info@techworld.com',
                'website': 'https://www.techworld.com',
                'phone_number': '+1 800 123 4567',
                'address': '123 Tech Street, San Francisco, CA',
            },
            {
                'name': 'Gadget Hub',
                'contact_email': 'sales@gadgethub.com',
                'website': 'https://www.gadgethub.com',
                'phone_number': '+1 800 234 5678',
                'address': '456 Gadget Avenue, New York, NY',
            },
            {
                'name': 'ElectroMart',
                'contact_email': 'support@electromart.com',
                'website': 'https://www.electromart.com',
                'phone_number': '+1 800 345 6789',
                'address': '789 Electro Boulevard, Chicago, IL',
            },
        ]

        for supplier_data in suppliers:
            Supplier.objects.get_or_create(**supplier_data)

        # Create products
        products = [
            {
                'name': 'iPhone 13',
                'category': 'Smartphones',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 100,
                'price': 999.99,
                'description': 'Latest Apple smartphone with advanced features.',
            },
            {
                'name': 'Samsung Galaxy S21',
                'category': 'Smartphones',
                'suppliers': ['Gadget Hub', 'ElectroMart'],
                'stock': 90,
                'price': 799.99,
                'description': 'High-performance Android smartphone with an impressive camera system.',
            },
            {
                'name': 'Google Pixel 6',
                'category': 'Smartphones',
                'suppliers': ['Tech World'],
                'stock': 80,
                'price': 699.99,
                'description': 'Google\'s flagship smartphone with pure Android experience.',
            },
            {
                'name': 'OnePlus 9 Pro',
                'category': 'Smartphones',
                'suppliers': ['ElectroMart'],
                'stock': 70,
                'price': 899.99,
                'description': 'High-end smartphone with fast charging and smooth performance.',
            },
            {
                'name': 'Sony Xperia 1 III',
                'category': 'Smartphones',
                'suppliers': ['Gadget Hub'],
                'stock': 50,
                'price': 1199.99,
                'description': 'Premium smartphone with a 4K display and professional-grade camera.',
            },
            {
                'name': 'MacBook Pro',
                'category': 'Laptops',
                'suppliers': ['Tech World', 'ElectroMart'],
                'stock': 50,
                'price': 1999.99,
                'description': 'High-performance laptop for professionals.',
            },
            {
                'name': 'Dell XPS 13',
                'category': 'Laptops',
                'suppliers': ['Tech World'],
                'stock': 60,
                'price': 1499.99,
                'description': 'Compact and powerful ultrabook with an edge-to-edge display.',
            },
            {
                'name': 'HP Spectre x360',
                'category': 'Laptops',
                'suppliers': ['Gadget Hub'],
                'stock': 70,
                'price': 1399.99,
                'description': 'Versatile 2-in-1 laptop with a stunning design and long battery life.',
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon',
                'category': 'Laptops',
                'suppliers': ['ElectroMart'],
                'stock': 40,
                'price': 1599.99,
                'description': 'Durable and powerful business laptop with excellent keyboard.',
            },
            {
                'name': 'Asus ROG Zephyrus G14',
                'category': 'Laptops',
                'suppliers': ['Gadget Hub'],
                'stock': 30,
                'price': 1799.99,
                'description': 'High-performance gaming laptop with a sleek design.',
            },
            {
                'name': 'Samsung Galaxy Tab S7',
                'category': 'Tablets',
                'suppliers': ['Gadget Hub', 'ElectroMart'],
                'stock': 75,
                'price': 649.99,
                'description': 'Versatile tablet with a powerful processor and large display.',
            },
            {
                'name': 'Sony Bravia 55" TV',
                'category': 'Televisions',
                'suppliers': ['Tech World'],
                'stock': 30,
                'price': 899.99,
                'description': 'Ultra HD smart TV with vibrant colors and smart features.',
            },
            {
                'name': 'Canon EOS R5 Camera',
                'category': 'Cameras',
                'suppliers': ['ElectroMart'],
                'stock': 20,
                'price': 3899.99,
                'description': 'High-resolution mirrorless camera for professional photography.',
            },
            {
                'name': 'Bose QuietComfort 35 II',
                'category': 'Audio Equipment',
                'suppliers': ['Gadget Hub'],
                'stock': 60,
                'price': 299.99,
                'description': 'Noise-cancelling headphones with superior sound quality.',
            },
            {
                'name': 'USB-C to HDMI Adapter',
                'category': 'Accessories',
                'suppliers': ['Tech World', 'Gadget Hub', 'ElectroMart'],
                'stock': 150,
                'price': 19.99,
                'description': 'Adapter for connecting USB-C devices to HDMI displays.',
            },
            {
                'name': 'Apple Watch Series 6',
                'category': 'Smartwatches',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 80,
                'price': 399.99,
                'description': 'Advanced smartwatch with health tracking and connectivity features.',
            },
            {
                'name': 'Samsung Galaxy Watch 3',
                'category': 'Smartwatches',
                'suppliers': ['Gadget Hub', 'ElectroMart'],
                'stock': 60,
                'price': 349.99,
                'description': 'Stylish smartwatch with fitness tracking and long battery life.',
            },
            {
                'name': 'PlayStation 5',
                'category': 'Gaming Consoles',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 40,
                'price': 499.99,
                'description': 'Next-gen gaming console with immersive gaming experience.',
            },
            {
                'name': 'Xbox Series X',
                'category': 'Gaming Consoles',
                'suppliers': ['ElectroMart'],
                'stock': 35,
                'price': 499.99,
                'description': 'Powerful gaming console with stunning graphics and fast load times.',
            },
            {
                'name': 'Sony WH-1000XM4',
                'category': 'Headphones',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 90,
                'price': 349.99,
                'description': 'Industry-leading noise-cancelling headphones with superior sound quality.',
            },
            {
                'name': 'Jabra Elite 85h',
                'category': 'Headphones',
                'suppliers': ['ElectroMart'],
                'stock': 70,
                'price': 249.99,
                'description': 'Wireless headphones with excellent battery life and noise cancellation.',
            },
            {
                'name': 'HP OfficeJet Pro 9015',
                'category': 'Printers',
                'suppliers': ['Tech World'],
                'stock': 50,
                'price': 229.99,
                'description': 'All-in-one printer with wireless printing and scanning capabilities.',
            },
            {
                'name': 'Canon PIXMA TR8520',
                'category': 'Printers',
                'suppliers': ['Gadget Hub'],
                'stock': 40,
                'price': 199.99,
                'description': 'Compact all-in-one printer perfect for home office use.',
            },
            {
                'name': 'Dell UltraSharp 27 Monitor',
                'category': 'Monitors',
                'suppliers': ['Tech World', 'ElectroMart'],
                'stock': 60,
                'price': 399.99,
                'description': 'High-resolution monitor with vibrant colors and sharp details.',
            },
            {
                'name': 'LG 34WN80C-B UltraWide Monitor',
                'category': 'Monitors',
                'suppliers': ['Gadget Hub'],
                'stock': 45,
                'price': 699.99,
                'description': 'UltraWide monitor ideal for multitasking and immersive viewing.',
            },
            {
                'name': 'Netgear Nighthawk X6S',
                'category': 'Networking Devices',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 75,
                'price': 229.99,
                'description': 'High-performance router with tri-band Wi-Fi and advanced security features.',
            },
            {
                'name': 'TP-Link Archer AX6000',
                'category': 'Networking Devices',
                'suppliers': ['ElectroMart'],
                'stock': 65,
                'price': 299.99,
                'description': 'Next-gen Wi-Fi 6 router with fast speeds and extensive coverage.',
            },
            {
                'name': 'Dyson V11 Vacuum Cleaner',
                'category': 'Home Appliances',
                'suppliers': ['Tech World', 'Gadget Hub'],
                'stock': 30,
                'price': 599.99,
                'description': 'Powerful cordless vacuum cleaner with advanced filtration.',
            },
            {
                'name': 'Instant Pot Duo 7-in-1',
                'category': 'Home Appliances',
                'suppliers': ['ElectroMart'],
                'stock': 50,
                'price': 99.99,
                'description': 'Versatile pressure cooker with multiple cooking functions.',
            },
        ]

        for product_data in products:
            category = Category.objects.get(name=product_data.pop('category'))
            suppliers = product_data.pop('suppliers')
            product, created = Product.objects.get_or_create(name=product_data['name'], defaults={
                'category': category,
                'stock': product_data['stock'],
                'price': product_data['price'],
                'description': product_data['description'],
            })
            if created:
                for supplier_name in suppliers:
                    supplier = Supplier.objects.get(name=supplier_name)
                    product.suppliers.add(supplier)
