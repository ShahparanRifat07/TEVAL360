from django.apps import AppConfig


class StakeholderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stakeholders'

    def ready(self):
        import stakeholders.signals
