from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('<int:pk>/', views.stock_detail, name='stock_detail'),
    path('dashboard/', views.stock_dashboard, name='stock_dashboard'),

]
