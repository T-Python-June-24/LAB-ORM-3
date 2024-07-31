from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.views_product, name="views_product"),
    path('update/product/<product_id>' , views.update_product , name='update_product'),
    path("product/new" , views.Add_product , name="Add_product"),
    
    path('download/', views.download_file, name='download_file'),
    path("product/ddelete/<product_id>" , views.delete , name="delete_product"),
]