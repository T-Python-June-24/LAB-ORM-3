from django.urls import path
from . import views
app_name = "reports"
urlpatterns = [
    path("reports/",views.reports_view,name="reports_view"),
]