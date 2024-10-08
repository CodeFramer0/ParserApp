from django.apps import AppConfig


class NostroyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nostroy"
    verbose_name = "НОСТРОЙ"

    def ready(self):
        import nostroy.signals
