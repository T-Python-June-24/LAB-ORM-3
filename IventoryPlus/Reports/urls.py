from . import views
from django.urls import path

app_name = 'Reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]