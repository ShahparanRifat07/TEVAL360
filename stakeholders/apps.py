from django.apps import AppConfig


class StakeholderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stakeholder'

    def ready(self):
        import stakeholder.signals
