import logging
from urllib import request

from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPSenderRefused, SMTPException
from django.http import HttpResponse, BadHeaderError

from config.settings import EMAIL_HOST_USER
from mailing.models import TryRecipient

# Настройка логирования
logger = logging.getLogger(__name__)


def send_a_message(mailing):
    try:
        subject = mailing.mail.theme
        message = mailing.mail.body_mail
        from_email = mailing.owner.email

        # Получаем список получателей для отправки
        recipient_list = mailing.recipient.values_list('email', flat=True)

        send_mail(subject, message, EMAIL_HOST_USER, recipient_list)

    except BadHeaderError:
        print("Неправильный заголовок в письме.")
    except SMTPException as e:
        # Логирование ошибки или действие в ответ на ошибку
        print(f"Ошибка SMTP: {e}")
        # Дополнительные меры, например, повторная попытка или уведомление
    except Exception as e:
        print(f"Возникла ошибка: {e}")
    except SMTPSenderRefused:
        logger.info(f"{HttpResponse("Ошибка при отправке письма.")} в {timezone.now()}")
        return HttpResponse("Ошибка при отправке письма.")  # обработка ошибок


def create_try_recipient(mailing, response):
    """  """
    # response = response.text
    # print(response)
    for recipient in mailing.recipient.all():
        if request:
            tryrecipient = TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_OK,  # Вы можете изменить логику по статусу
                mail_response=response  # Замените это на реальный ответ при отправке
            )
            tryrecipient.save()

        else:
            tryrecipient = TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_ERROR,  # Вы можете изменить логику по статусу
                mail_response=response  # Замените это на реальный ответ при отправке
            )
            tryrecipient.save()

