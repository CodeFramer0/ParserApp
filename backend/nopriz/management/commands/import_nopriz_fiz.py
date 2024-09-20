import json

import requests
from django.core.management.base import BaseCommand
from nopriz.models import NoprizFiz


class Command(BaseCommand):
    help = "Load data from JSON into Worker model"

    def handle(self, *args, **options):
        json_file_path = "НОПРИЗ_физлица.json"
        NoprizFiz.objects.all().delete()
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for key, value in data.items():
                id_number = value.get("id_number", "")
                full_name = value.get("full_name", "")
                date_of_inclusion_protocol = value.get(
                    "date_of_inclusion_protocol", ""
                ).replace(" *", "")
                date_of_modification = value.get("date_of_modification", "")
                date_of_issue_certificate = value.get("date_of_issue_certificate", None)
                type_of_work = value.get("type_of_work", "")
                date_of_exclusion = value.get("date_of_exclusion", None)
                status_worker = (
                    "ACTIVE"
                    if value.get("status_worker") == "Действует"
                    else "EXCLUDED"
                )

                NoprizFiz.objects.create(
                    id_number=id_number,
                    id_number_img=value.get("id_number_img", ""),
                    full_name_img=value.get("full_name_img", ""),
                    date_of_inclusion_protocol_img=value.get(
                        "date_of_inclusion_protocol_img", ""
                    ),
                    date_of_modification_img=value.get("date_of_modification_img", ""),
                    full_name=full_name,
                    date_of_inclusion_protocol=date_of_inclusion_protocol,
                    date_of_modification=date_of_modification,
                    date_of_issue_certificate=date_of_issue_certificate,
                    type_of_work=type_of_work,
                    date_of_exclusion=date_of_exclusion,
                    status_worker=status_worker,
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported data"))
