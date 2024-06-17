from time import sleep


from django.apps import AppConfig


class SendMailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.services import start
        sleep(2)
        start()