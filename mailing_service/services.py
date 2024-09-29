import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailing_service.models import Mailing, Attempt

def send_mailing():
    """
    Функция отправки рассылок
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status__in=['started', 'created'])

    for mailing in mailings:
        if mailing.start_date and current_datetime >= mailing.start_date:
            mailing.status = 'started'
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                Attempt.objects.create(status='success',
                                   response=server_response,
                                   mailing=mailing, )
            except smtplib.SMTPException as e:
                Attempt.objects.create(status='failed',
                                   response=str(e),
                                   mailing=mailing, )

            # Обновление времени следующей отправки
            if mailing.period == 'daily':
                mailing.start_date += timedelta(days=1)
            elif mailing.period == 'weekly':
                mailing.start_date += timedelta(weeks=1)
            elif mailing.period == 'monthly':
                mailing.start_date += timedelta(days=30)

            mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(send_mailing, 'interval', seconds=30)

    if not scheduler.running:
        scheduler.start()