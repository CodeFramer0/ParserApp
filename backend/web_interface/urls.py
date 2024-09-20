from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "excel/nopriz_fiz/", views.ExcelNoprizFizView.as_view(), name="excel_nopriz_fiz"
    ),
    path(
        "excel/nopriz/yr/", views.ExcelNoprizYrView.as_view(), name="excel_nopriz_yr"
    ),
    # path("download/nostroy/fiz/", views.excel_nostroy_fiz, name="excel_nostroy_fiz"),
    # path("download/nostroy/smet/", views.excel_nostroy_smet, name="excel_nostroy_smet"),
]
