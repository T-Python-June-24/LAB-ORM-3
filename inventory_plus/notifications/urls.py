from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('send-alerts/', views.send_alerts, name='send_alerts'),

]
