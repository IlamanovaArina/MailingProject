import logging
from smtplib import SMTPException, SMTPSenderRefused

from django.core.mail import send_mail
from django.http import BadHeaderError
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import TryRecipient, Mailing

# Настройка логирования
logger = logging.getLogger(__name__)


def send_a_message(mailing: Mailing):
    """ Отправка рассылки на почту """
    recipients = mailing.recipient.all()

    try:
        subject = mailing.mail.theme
        message = mailing.mail.body_mail
        # from_email = mailing.owner.email
        recipient_list = mailing.recipient.values_list('email', flat=True)

        mailing.endDt = timezone.now()  # Записываем время окончания
        mailing.my_field = mailing.STATUS_STARTED  # Измени статус на отправленный
        mailing.save()

        response = send_mail(subject, message, EMAIL_HOST_USER, recipient_list)

        if response > 0:
            # При успешной отправке создаём модель попытки отправки
            create_try_recipient(recipients, "Сообщение успешно отправлено.", mailing.owner)
        elif response == 0:
            # При ошибке отправки создаём модель попытки отправки
            create_failure_recipient(recipients, "Сообщение не отправлено.", mailing.owner)

    except BadHeaderError as e:
        create_failure_recipient(recipients, "Неправильный заголовок в письме.", mailing.owner)
        logger.error(f"Ошибка: {e} в: {timezone.now()}")
    except SMTPException as e:
        create_failure_recipient(recipients, f"Ошибка SMTP: {e}", mailing.owner)
        logger.error(f"Ошибка: {e} в: {timezone.now()}")
    except SMTPSenderRefused as e:
        create_failure_recipient(recipients, f"Ошибка SMTP: {e}", mailing.owner)
        logger.error(f"Ошибка: {e} в: {timezone.now()}")
    except Exception as e:
        create_failure_recipient(recipients, f"Ошибка: {e}", mailing.owner)
        logger.error(f"Ошибка: {e} в: {timezone.now()}")


def create_try_recipient(recipients, response, owner):
    for recipient in recipients:
        try:
            TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_OK,
                mail_response=response,
                owner=owner
            )
        except Exception as e:
            logger.error(f"Error while processing recipient {recipient}: {e}")


def create_failure_recipient(recipients, response, owner):
    for recipient in recipients:
        try:
            TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_ERROR,
                mail_response=response,
                owner=owner
            )
        except Exception as e:
            logger.error(f"Error while processing recipient {recipient}: {e}")
