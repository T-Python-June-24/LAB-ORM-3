from django.urls import path
from . import views
app_name = "suppliers"
urlpatterns = [
    path("all",views.all_suppliers,name="all_suppliers"),
    path("add",views.add_supplier,name="add_supplier"),
    path("delete/<supplier_id>",views.delete_supplier,name="delete_supplier"),
    path("update/<supplier_id>",views.update_supplier,name="update_supplier"),
    path("detailes/<supplier_id>",views.supplier_detailes,name="supplier_detailes"),
    path("export/",views.export_suppliers,name="export_suppliers"),
]