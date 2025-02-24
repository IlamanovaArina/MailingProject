from django.db import models


class Recipient(models.Model):
    """Модель получателя"""
    email = models.EmailField(unique=True,
                              verbose_name='Email',
                              help_text='Рассылка будет отправлена на указанный email.')
    full_name = models.CharField(max_length=30,
                                 verbose_name='Ф.И.О')
    comment = models.TextField(max_length=150)


class Mail(models.Model):
    """Модель сообщения"""
    theme = models.CharField()
    body_mail = models.TextField()

    def __str__(self):
        return self.theme


class Mailing(models.Model):
    """Рассылка"""
    STATUS_NEW = 'NEW'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    startDt = models.DateField()
    endDt = models.DateField()
    my_field = (models.CharField
        (
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    ))
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient)


class TryRecipient(models.Model):
    """Модель успеха отправлений"""
    STATUS_OK = 'Успешно'
    STATUS_ERROR = 'Не успешно'

    STATUS_CHOICES = [
        (STATUS_OK, 'Успешно'),
        (STATUS_ERROR, 'Не успешно'),
    ]

    time_try = models.DateField()
    status = (models.CharField
        (
        choices=STATUS_CHOICES)
    )
    mail_response = models.TextField()
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
