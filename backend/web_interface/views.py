import os

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View


def index(request):
    return render(request, "index.html")


class ExcelNoprizFizView(View):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, "НОПРИЗ Физ лица.xlsx")
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename="НОПРИЗ Физ лица.xlsx",
            )


class ExcelNoprizYrView(View):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, "НОПРИЗ Юр лица.xlsx")
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename="НОПРИЗ Юр лица.xlsx",
            )
