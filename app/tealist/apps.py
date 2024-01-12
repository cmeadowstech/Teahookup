from django.apps import AppConfig


class TealistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tealist"

    def ready(self):
        import tealist.signals
