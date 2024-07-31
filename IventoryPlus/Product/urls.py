from . import views
from django.urls import path

app_name = 'Product'

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('thanks/', views.thanksPage , name='thanks'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/search/' ,views.product_search,name='search' ),
    path('stock_status/', views.stock_status, name='stock_status'),
    path('update_stock/<int:pk>/', views.update_stock, name='update_stock'),
    path('products/export/', views.export_products_csv, name='export_products_csv'),
    path('products/export/excel/', views.export_products_excel, name='export_products_excel'),
    path('import/', views.import_products_csv, name='import_products_csv'),
]
