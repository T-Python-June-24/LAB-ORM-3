from django.shortcuts import render
from .utils import send_notification_email
from .models import Notification

def send_alerts(request):
    subject = "Inventory Alert"
    message = "This is a test alert message."
    recipient_list = ['manager-email@example.com']
    send_notification_email(subject, message, recipient_list)
    return render(request, 'notifications/notification_sent.html')


def notification_list(request):
    notifications = Notification.objects.all()
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})