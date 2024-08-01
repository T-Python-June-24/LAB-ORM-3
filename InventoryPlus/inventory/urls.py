from django.urls import path
from . import views


app_name = "inventory"

urlpatterns = [
    path("", views.home, name="home_view"),
    path("inventory/", views.inventory, name="inventory_view"),

]