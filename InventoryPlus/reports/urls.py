from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
  path('reports/', views.inventory_report, name='inventory_report'),
]