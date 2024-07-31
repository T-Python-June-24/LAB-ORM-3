from django.http import HttpResponse
from Notifications.utils import send_alerts
from django.shortcuts import render, redirect
from .models import EmailRecipient
from .forms import EmailForm


def send_alerts_view(request:HttpResponse):
    send_alerts()
    return HttpResponse('Alerts sent successfully')

def add_email(request:HttpResponse):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            EmailRecipient.objects.create(email=email)
            return redirect('Product:thanks') 
    else:
        form = EmailForm()
    return render(request, 'Notifications/add_email.html', {'form': form})


