import logging
from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPSenderRefused
from django.http import HttpResponse


# Настройка логирования
logger = logging.getLogger(__name__)


def send_a_message(mailing):
    try:
        subject = mailing.mail.theme
        message = mailing.mail.body_mail
        from_email = mailing.owner.email

        # Получаем список получателей для отправки
        recipient_list = mailing.recipient.values_list('email', flat=True)

        send_mail(subject, message, from_email, recipient_list)
    except SMTPSenderRefused:
        logger.info(f"{HttpResponse("Ошибка при отправке письма.")} в {timezone.now()}")
        return HttpResponse("Ошибка при отправке письма.")  # обработка ошибок
