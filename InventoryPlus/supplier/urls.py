from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('add/', views.add_view, name='add_view'),
    path('edit/<int:supplier_id>/', views.edit_view, name='edit_view'),
    path('all/', views.all_view, name='all_view'),
    path('detail/<int:supplier_id>/', views.detail_view, name='detail_view'),
    path('delete/<int:supplier_id>/', views.delete_view, name='delete_view'),
    path('search/', views.search_view, name='search_view'),
]
