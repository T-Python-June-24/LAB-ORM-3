from django.urls import path
from . import views

app_name = "supplier"

urlpatterns = [
    path("allSuppliers/", views.all_suppliers_view, name="all_suppliers_view"),
    path("addSuppliers/", views.add_suppliers_view, name="add_suppliers_view"),
    path("deleteSuppliers/<supplier_id>", views.delete_suppliers_view, name="delete_suppliers_view"),
    path("updateSuppliers/<supplier_id>", views.update_suppliers_view, name="update_suppliers_view"),
]