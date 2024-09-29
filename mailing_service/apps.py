import os
from django.apps import AppConfig


class MailingServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing_service"

    def ready(self):
        if os.environ.get('RUN_MAIN', False) == 'True':
            from mailing_service.services import start_scheduler
            start_scheduler()