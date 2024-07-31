from django.urls import path
from . import views

app_name = 'Suppliers'

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('add/', views.add_supplier, name='add_supplier'),
    path('<int:pk>/update/', views.update_supplier, name='update_supplier'),
    path('<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),
    path('search/', views.supplier_search, name='search'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
]
