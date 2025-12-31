from django.apps import AppConfig


class RespondersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "responders"
    
    def ready(self):
        # Import signals to register them
        import responders.signals
