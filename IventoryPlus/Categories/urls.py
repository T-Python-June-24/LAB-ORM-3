# urls.py
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.list_categories, name='list_categories'),
    path('add/', views.add_category, name='add_category'),
    path('edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('import-csv/', views.import_categories_csv, name='import_categories_csv'),

]
