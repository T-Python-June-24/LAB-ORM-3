from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    # CRUD Routes
    path('create/', views.supplier_create, name='supplier_create'),
    path('<int:pk>/update/', views.supplier_update, name='supplier_update'),
    path('<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    # CSV Related routes
    path('import/', views.import_suppliers_csv, name='import_suppliers_csv'),
    path('export/', views.export_suppliers_csv, name='export_suppliers_csv'),
    # Additional Routes
    path('supplier/<int:pk>/update-last-active/', views.update_last_active, name='update_last_active'),
]