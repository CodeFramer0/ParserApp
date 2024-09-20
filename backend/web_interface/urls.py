from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("download/excel/nopriz/fiz/", views.generate_excel_nopriz_fiz, name="download_excel_nopriz_fiz"),
]
