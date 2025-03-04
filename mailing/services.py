import logging
from urllib import request

from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPSenderRefused, SMTPException
from django.http import HttpResponse, BadHeaderError

from config.settings import EMAIL_HOST_USER
from mailing.models import TryRecipient, Recipient

# Настройка логирования
logger = logging.getLogger(__name__)


def send_a_message(mailing):
    """  """
    recipients = mailing.recipient.all()

    try:
        subject = mailing.mail.theme
        message = mailing.mail.body_mail
        # Почта отправителя
        from_email = mailing.owner.email

        # Получаем список получателей для отправки
        recipient_list = mailing.recipient.values_list('email', flat=True)

        mailing.my_field = mailing.STATUS_STARTED  # Измени статус на отправленный
        mailing.endDt = timezone.now()  # Записываем время окончания
        mailing.save()

        # Отправляем письмо на почту
        response = send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
        create_try_recipient(recipients, response)

    except BadHeaderError:
        create_failure_recipient(recipients, "Неправильный заголовок в письме.")
        print("Неправильный заголовок в письме.")

    except SMTPException as e:
        # Логирование ошибки или действие в ответ на ошибку
        create_failure_recipient(recipients, f"Ошибка SMTP: {e}")
        print(f"Ошибка SMTP: {e}")
        # Дополнительные меры, например, повторная попытка или уведомление

    except SMTPSenderRefused as e:
        create_failure_recipient(recipients, f"Ошибка SMTP: {e}")
        logger.info(f"{HttpResponse("Ошибка при отправке письма.")} в {timezone.now()}")
        return HttpResponse("Ошибка при отправке письма.")  # обработка ошибок

    except Exception as e:
        create_failure_recipient(recipients, f"Ошибка SMTP: {e}")
        print(f"Возникла ошибка: {e}")



def create_try_recipient(recipients, response):
    """  """
    # response = response.text
    # print(response)
    for recipient in recipients:
        for recipient in recipients:
            try:
                # Убедитесь, что recipient - это экземпляр Recipient
                tryrecipient = TryRecipient.objects.create(
                    recipient=recipient,
                    time_try=timezone.now(),
                    status=TryRecipient.STATUS_OK,  # Вы можете изменить логику по статусу
                    mail_response=response  # Замените это на реальный ответ при отправке
                )
                tryrecipient.save()
            except Exception as e:
                # Логирование или обработка ошибок
                print(f"Error while processing recipient {recipient}: {e}")



def create_failure_recipient(recipients, response):
    # response = response.text
    # print(response)
    for recipient in recipients:
        try:
            tryrecipient = TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_ERROR,  # Вы можете изменить логику по статусу
                mail_response=response  # Замените это на реальный ответ при отправке
            )
            tryrecipient.save()
        except Exception as e:
            # Логирование или обработка ошибок
            print(f"Error while processing recipient {recipient}: {e}")
