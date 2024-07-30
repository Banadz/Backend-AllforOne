from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fullBack'
    models = {'Agent': 'fullBack.Agent'}
    verbose_name = 'MK 47'
