from django.core.management.base import BaseCommand
from stocks.utils import check_stock_and_expiry

class Command(BaseCommand):
    help = 'Check for low stock and approaching expiry dates and send notifications.'

    def handle(self, *args, **kwargs):
        check_stock_and_expiry()
        self.stdout.write(self.style.SUCCESS('Notifications sent successfully.'))