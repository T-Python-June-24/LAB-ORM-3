from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("allInventories/", views.all_inventories_view, name="all_inventories_view"),
    path("addInventories/", views.add_inventories_view, name="add_inventories_view"),
    path("deleteInventories/<inventory_id>", views.delete_inventories_view, name="delete_inventories_view"),
    path("updateInventories/<inventory_id>", views.update_inventories_view, name="update_inventories_view"),
]