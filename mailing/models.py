from django.db import models
from config import settings
from users.models import User


class Recipient(models.Model):
    """Модель получателя"""
    email = models.EmailField(verbose_name='Email',
                              help_text='Рассылка будет отправлена на указанный email.')
    full_name = models.CharField(max_length=50, verbose_name='Ф.И.О')
    comment = models.TextField(max_length=150, verbose_name='Комментарий', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipients', verbose_name='Владелец')

    class Meta:
        """ UniqueConstraint гарантирует, что комбинация email и owner будет уникальной. """
        constraints = [
            models.UniqueConstraint(fields=['email', 'owner'], name='unique_recipient_per_owner')
        ]

    def __str__(self):
        return self.email




class Mail(models.Model):
    """Модель сообщения"""
    theme = models.CharField(verbose_name='Тема письма', max_length=50)
    body_mail = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails', verbose_name='Владелец')

    def __str__(self):
        return self.theme


class Mailing(models.Model):
    """Рассылка"""
    STATUS_END = 'Завершена'
    STATUS_NEW = 'Создана'
    STATUS_STARTED = 'Запущена'

    STATUS_CHOICES = [
        (STATUS_END, 'Завершена'),
        (STATUS_NEW, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
    ]

    startDt = models.DateTimeField(verbose_name='Дата и время первой отправки', auto_now_add=True)
    endDt = models.DateTimeField(verbose_name='Дата и время окончания отправки', auto_now=True)
    my_field = models.CharField(choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='Статус')
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipient = models.ManyToManyField(Recipient, verbose_name='Получатель')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailings', verbose_name='Владелец')

    def __str__(self):
        return self.my_field


class TryRecipient(models.Model):
    """Модель успеха отправлений"""
    STATUS_OK = 'Успешно'
    STATUS_ERROR = 'Не успешно'

    STATUS_CHOICES = [
        (STATUS_OK, 'Успешно'),
        (STATUS_ERROR, 'Не успешно'),
    ]

    time_try = models.DateTimeField(verbose_name='Дата и время попытки')
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_ERROR, verbose_name='Статус')
    mail_response = models.TextField(verbose_name='Ответ почтового сервера',)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name='Рассылка')

    # def __str__(self):
    #     return self.
