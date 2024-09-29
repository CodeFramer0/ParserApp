from django.contrib import admin

from .models import *


@admin.register(NostroyFiz)
class NostroyFizAdmin(admin.ModelAdmin):
    list_display = (
        "id_number",
        "full_name",
        "status_worker",
        "date_of_inclusion_protocol",
        "date_of_modification",
        "type_of_work",
        "is_parsed",
    )
    search_fields = ("id_number", "full_name")
    list_filter = ("status_worker",)
    ordering = ("-date_of_inclusion_protocol",)


@admin.register(NostroySmet)
class NostroySmet(admin.ModelAdmin):
    list_display = (
        "id_number",
        "full_name",
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
