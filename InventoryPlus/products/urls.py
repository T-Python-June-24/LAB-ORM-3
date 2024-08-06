from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
  path("all/", views.products_view, name="products_view"),
  path("add/", views.add_product, name="add_product"),
  path("edit/<int:product_id>/", views.edit_product_view, name="edit_product_view"),
  path('delete/<int:product_id>/', views.delete_product_view, name="delete_product_view"),
  path('detail/<int:product_id>/', views.product_detail_view, name="product_detail_view"),
  path('search/', views.product_search_view, name="product_search_view"),
  path('categories/', views.categories_view, name="categories_view"),
  path('categories/add/', views.add_category_view, name="add_category_view"),
  path('categories/edit/<int:category_id>/', views.edit_category_view, name="edit_category_view"),
  path('categories/delete/<int:category_id>/', views.delete_category_view, name="delete_category_view"), 
]