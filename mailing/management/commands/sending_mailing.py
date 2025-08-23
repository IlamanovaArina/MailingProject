from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from mailing.models import Mailing
from mailing.services import send_a_message


class SendingMailing(BaseCommand):
    help = "Тестовая отправка рассылки на тестовую почту."

    def add_arguments(self, parser):
        parser.add_argument('mailing_ids', nargs='+', type=int, help='ID рассылок для отправки')

    def handle(self, *args, **kwargs):
        mailing_ids = kwargs['mailing_ids']

        for mailing_id in mailing_ids:
            try:
                mailing = Mailing.objects.get(id=mailing_id)  # Получаем рассылку по ID
                send_a_message(mailing)  # Отправляем сообщение
                self.stdout.write(self.style.SUCCESS(f'Рассылка с ID {mailing_id} была успешно отправлена.'))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при отправке рассылки с ID {mailing_id}: {e}'))
