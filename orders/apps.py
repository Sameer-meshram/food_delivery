from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    # optional: if you ever add signals
    # def ready(self):
    #     from . import signals
