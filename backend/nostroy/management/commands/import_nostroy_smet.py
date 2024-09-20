import json

from django.core.management.base import BaseCommand

from nostroy.models import NostroySmet


class Command(BaseCommand):
    help = "Load data from JSON into Worker model"

    def handle(self, *args, **options):
        json_file_path = "НОСТРОЙ_сметчики.json"

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for key, value in data.items():
                id_number = value.get("id_number", "")
                full_name = value.get("full_name", "")
                date_of_inclusion_protocol = value.get(
                    "date_of_inclusion_protocol", ""
                ).replace(" *", "")
                type_of_work = value.get("type_of_work", "")
                date_of_exclusion = value.get("date_of_exclusion", None)
                status_worker = (
                    "ACTIVE"
                    if value.get("status_worker") == "Действует"
                    else "EXCLUDED"
                )

                NostroySmet.objects.create(
                    id_number=id_number,
                    full_name=full_name,
                    date_of_inclusion_protocol=date_of_inclusion_protocol,
                    type_of_work=type_of_work,
                    date_of_exclusion=date_of_exclusion,
                    status_worker=status_worker,
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported data"))
