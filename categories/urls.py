from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('create/', views.category_create, name='category_create'),
    path('<int:pk>/update/', views.category_update, name='category_update'),
    path('<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('import/', views.import_categories_csv, name='import_categories_csv'),
    path('export/', views.export_categories_csv, name='export_categories_csv'),
]