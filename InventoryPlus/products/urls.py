from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path("add_product/", views.add_product_view, name="add_product_view"),
    path("update_product/<product_id>/", views.update_product_view, name="update_product_view"),
    path("delete_product/<product_id>/", views.delete_product_view, name="delete_product_view"),
    path("search/", views.search_products_view, name="search_products_view"),
    path("products/<type>/<product_param>/", views.all_products_view, name="all_products_view"),
    path('product_detail/<product_id>/', views.product_detail_view, name='product_detail_view'),
    path("export_products_csv/", views.export_products_csv_view, name="export_products_csv_view"),
    path("csv_products/", views.import_products_csv_view, name="import_products_csv_view"),

]


