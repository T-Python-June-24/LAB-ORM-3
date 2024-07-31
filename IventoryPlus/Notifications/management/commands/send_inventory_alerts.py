#NOTE
#! This file is used to send alerts for low stock and upcoming expiry dates by running the python manage.py send_inventory_alerts command.
from django.core.management.base import BaseCommand
from Notifications.utils import send_alerts  

class Command(BaseCommand):
    help = 'Send inventory alerts for low stock and upcoming expiry dates'

    def handle(self, *args, **kwargs):
        send_alerts()
        self.stdout.write(self.style.SUCCESS('Successfully sent inventory alerts'))
