from django.urls import path
from . import views

app_name = "Supplier"

urlpatterns = [
    
    path("add/suppier" , views.Add_Supplier ,name="Add_Supplier"),
    path("update/supplier/<supplier_id>" , views.Update_Supplier, name="Update_Supplier"),
    path("delete/supplier/<supplier_id>" , views.delet_supplier , name="delet_supplier"),
]