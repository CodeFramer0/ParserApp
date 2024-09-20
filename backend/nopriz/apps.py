from django.apps import AppConfig


class NoprizConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nopriz"
    verbose_name = "Nopriz"

    def ready(self):
        import nopriz.signals
