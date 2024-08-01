from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('supplier/', views.supplier_report, name='supplier_report'),
]
