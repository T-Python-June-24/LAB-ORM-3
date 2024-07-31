from django.urls import path
from . import views

app_name = "ReportsProduct"

urlpatterns = [
    path("upload/csv" , views.upload_csv , name="upload_csv"),
    path("download/sample" ,views.download_sample , name="download_sample"),
    path("Download/rebort"  , views.generate_report , name="generate_report"),
    path("download/suppliers/report" , views.download_suppliers_report ,  name="download_suppliers_report")
]