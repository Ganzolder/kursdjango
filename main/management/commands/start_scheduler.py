from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail # Импортируйте вашу задачу из соответствующего модуля

from main.services import SendMailing


class Command(BaseCommand):
    help = 'Starts the scheduler for sending emails'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        send_mailing_instance = SendMailing()
        scheduler.add_job(send_mailing_instance.send_mailing, 'interval', seconds=60)
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Scheduler started successfully'))

