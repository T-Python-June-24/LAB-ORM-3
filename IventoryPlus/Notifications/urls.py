# Notifications/urls.py

from django.urls import path
from Notifications import views

app_name = 'Notifications'

urlpatterns = [
    path('add-email/', views.add_email, name='add_email'),
]
