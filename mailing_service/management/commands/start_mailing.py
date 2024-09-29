import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing_service.models import Mailing, Attempt


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='started')

        for mailing in mailings:
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