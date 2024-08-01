from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('',views.home_view, name= 'home_view'),
    path('products_report/',views.products_report_view, name= 'products_report_view'),
    path('suppliers_report/',views.suppliers_report_view, name= 'suppliers_report_view'),
    # path('contact/', views.contact_view, name="contact_view"),
    path("mode/<mode>/", views.mode_view, name="mode_view"),

]
