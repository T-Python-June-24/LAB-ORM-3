from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    # csv related
    path('import/', views.import_products_csv, name='import_products_csv'),
    path('export/', views.export_products_csv, name='export_products_csv'),
    # apis
    path('api/chart-data/', views.chart_data, name='chart_data'),
    path('check-status/<int:pk>/', views.check_product_status, name='check_product_status'),
]