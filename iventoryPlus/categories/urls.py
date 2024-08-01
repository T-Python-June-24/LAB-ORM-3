from django.urls import path
from . import views
app_name = "categories"
urlpatterns = [    
path('all/',views.all_categories,name="all_categories"),
path("add/",views.add_category,name="add_category"),
path("delete/<category_id>",views.delete_category,name="delete_category"),
path("update/<category_id>",views.update_category,name="update_category"),
path("related/products<category_id>",views.related_products,name="related_products"),
]