from django.urls import path
from . import views

app_name = "Category"

urlpatterns = [
    path('', views.views_Category, name="views_Category"),
    path('Category/add' , views.add_category , name='add_category'),
    path('update/category/<category_id>' , views.update_category , name='update_category'),
    path('delete/category/<category_id>' , views.delete_category, name='delete_category'),
]