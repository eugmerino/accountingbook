from django.apps import AppConfig


class StateofresultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stateOfResult'
    verbose_name = 'Estado de Resultado'

    def ready(self):
        import stateOfResult.signals  # Importa el archivo de señales
