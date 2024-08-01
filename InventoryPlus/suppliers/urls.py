from django.urls import path
from . import views

app_name = 'suppliers'
urlpatterns = [
    path("add_supplier/", views.add_supplier_view, name="add_supplier_view"),
    path('supplier_detail/<supplier_id>/', views.supplier_detail_view, name='supplier_detail_view'),
    path("delete_supplier/<supplier_id>/", views.delete_supplier_view, name="delete_supplier_view"),
    path("update_supplier/<supplier_id>/", views.update_supplier_view, name="update_supplier_view"),
    path("all_suppliers/<supplier_id>/", views.all_suppliers_view, name="all_suppliers_view"),
]