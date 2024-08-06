from django.urls import path
from . import views

app_name = "suppliers"

urlpatterns = [
  path('all/', views.suppliers_list_view, name='suppliers_list'),
  path('add/', views.add_supplier_view, name='add_supplier'),
  path('edit/<int:supplier_id>/', views.edit_supplier_view, name='edit_supplier'),
  path('delete/<int:supplier_id>/', views.delete_supplier_view, name='delete_supplier'),
  path('detail/<int:supplier_id>/', views.supplier_detail_view, name='supplier_detail'),
]