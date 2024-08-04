from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.all_categories, name='all_categories'),
    path('add/', views.add_category, name='add_category'),
    path('update/<int:category_id>/', views.category_update, name='category_update'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),
]
