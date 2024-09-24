import bz2
import os

from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
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


class DecompressFileView(View):
    def post(self, request):
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        compressed_file = request.FILES["file"]

        try:
            decompressed_data = bz2.decompress(compressed_file.read())
            original_filename = os.path.splitext(compressed_file.name)[0]
        except Exception as e:
            return JsonResponse(
                {"error": f"Error during decompression: {str(e)}"}, status=500
            )
        response = HttpResponse(decompressed_data, content_type="application/json")
        response["Content-Disposition"] = (
            f'attachment; filename="{original_filename}.json"'
        )
        return response
