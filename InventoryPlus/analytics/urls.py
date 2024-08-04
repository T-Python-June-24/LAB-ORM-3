from django.urls import path
from . import views



app_name = 'analytics'


urlpatterns = [
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('category-details/', views.category_details, name='category_details'),
    path('supplier/', views.supplier_report, name='supplier_report'),
    path('low-stock/', views.low_stock_alerts, name='low_stock_alerts'),
]
