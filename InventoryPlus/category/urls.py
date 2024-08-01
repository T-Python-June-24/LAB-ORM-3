from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('add/', views.add_view, name='add_view'),
    path('edit/<int:category_id>/', views.edit_view, name='edit_view'),
    path('all/', views.all_view, name='all_view'),
    path('detail/<int:category_id>/', views.detail_view, name='detail_view'),
    path('delete/<int:category_id>/', views.delete_view, name='delete_view'),


]
