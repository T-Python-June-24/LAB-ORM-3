from django.urls import path
from . import views
from .views import product_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.product_add, name='product_add'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/', product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'), #pic

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #pic