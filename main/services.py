import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from main.models import Post, PostLogs
import datetime as dt

class SendMailing:

    @staticmethod
    def send_mailing():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = zone.localize(dt.datetime.now()).replace(second=0, microsecond=0)
        mailings = Post.objects.filter(status='created').filter(start_at__lte=current_datetime)
        additional_mailings = Post.objects.filter(status='published').filter(next_send_date__lte=current_datetime)
        combined_mailings = mailings.union(additional_mailings)
        mailings = combined_mailings


        if mailings:
            for mailing in mailings:
                mailing.status = 'published'
                mailing.save()
                try:
                    server_response = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.text,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email for recipient in mailing.recipient.all()],
                        fail_silently=False
                    )

                    if server_response:
                        PostLogs.objects.create(post=mailing, try_date=current_datetime, result='success')
                        mailing.next_send_date = current_datetime
                        if mailing.period == 'daily':
                            mailing.next_send_date += dt.timedelta(days=1)
                        elif mailing.period == 'weekly':
                            mailing.next_send_date += dt.timedelta(days=7)
                        elif mailing.period == 'monthly':
                            mailing.next_send_date += dt.timedelta(days=30)

                        mailing.save()
                    else:
                        PostLogs.objects.create(post=mailing, try_date=current_datetime, result='failed')
                except smtplib.SMTPException as err:
                    PostLogs.objects.create(post=mailing, try_date=current_datetime, result='failed', error_message=err)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(SendMailing, 'interval', seconds=60)
    scheduler.start()


def get_posts_from_cache():
    if not CACHE_ENABLED:
        return Post.objects.all()
    key = 'post_list'
    posts = cache.get(key)
    if posts is not None:
        return posts
    posts = Post.objects.all()

    cache.set(key, posts)

    return posts
