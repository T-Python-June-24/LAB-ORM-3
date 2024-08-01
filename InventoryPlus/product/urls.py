from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path("allProducts/", views.all_products_view, name="all_products_view"),
    path("addProducts/", views.add_products_view, name="add_products_view"),
    path("deleteProducts/<product_id>", views.delete_products_view, name="delete_products_view"),
    path("updateProducts/<product_id>", views.update_products_view, name="update_products_view"),
]