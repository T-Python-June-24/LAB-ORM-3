from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('<int:supplier_id>/update/', views.supplier_update, name='supplier_update'),
    path('<int:supplier_id>/delete/', views.supplier_delete, name='supplier_delete'),
    path('add/', views.supplier_add, name='supplier_add'), 
]
