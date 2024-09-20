from django.contrib import admin

from .models import *


@admin.register(NostroySmet)
class NostroySmet(admin.ModelAdmin):
    list_display = (
        "id_number",
        "full_name",
        "status_worker",
        "type_of_work",
        "status_worker",
    )
    search_fields = [
        "full_name",
        "id_number",
    ]
    list_filter = (
        "status_worker",
        "type_of_work",
    )
