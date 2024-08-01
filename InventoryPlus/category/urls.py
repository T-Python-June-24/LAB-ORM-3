from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path("allCategories/", views.all_Categories_view, name="all_Categories_view"),
    path("addCategories/", views.add_Category_view, name="add_Category_view"),
    path('deleteCategories/<category_id>/', views.delete_Category_view, name='delete_Category_view'),
    path('updatedCategory/<category_id>/', views.update_Category_view, name='update_Category_view'),
]
