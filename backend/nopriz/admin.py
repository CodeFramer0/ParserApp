from django.contrib import admin

from .models import *


@admin.register(NoprizFiz)
class NoprizFiz(admin.ModelAdmin):
    list_display = (
        "id_number",
        "full_name",
        "status_worker",
        "verified_id_number",
        "id_number_verification_attempts",
        "type_of_work",
        "is_parsed",
        "status_worker",
    )
    search_fields = [
        "full_name",
        "id_number",
    ]
    list_filter = (
        "verified_id_number",
        "status_worker",
        "type_of_work",
    )


@admin.register(NoprizYr)
class NoprizFiz(admin.ModelAdmin):
    list_display = (
        "id_number",
        "name_cpo",
        "status",
        "inn",
        "ogrn",
        "date_of_registration",
        "date_of_termination",
        "director",
    )
    search_fields = ["id_number", "inn", "ogrn"]
    list_filter = ("status",)
