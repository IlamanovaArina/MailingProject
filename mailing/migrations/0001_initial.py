# Generated by Django 5.1.6 on 2025-02-24 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=50, verbose_name='Тема письма')),
                ('body_mail', models.TextField(verbose_name='Тело письма')),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Рассылка будет отправлена на указанный email.', max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=50, verbose_name='Ф.И.О')),
                ('comment', models.TextField(blank=True, max_length=150, null=True, verbose_name='Комментарий')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки')),
                ('endDt', models.DateTimeField(auto_now=True, verbose_name='Дата и время окончания отправки')),
                ('my_field', models.CharField(choices=[('Завершена', 'Завершена'), ('Создана', 'Создана'), ('Запущена', 'Запущена')], default='Создана', verbose_name='Статус')),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mail', verbose_name='Сообщение')),
                ('recipient', models.ManyToManyField(to='mailing.recipient', verbose_name='Получатель')),
            ],
        ),
        migrations.CreateModel(
            name='TryRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_try', models.DateTimeField(verbose_name='Дата и время попытки')),
                ('status', models.CharField(choices=[('Успешно', 'Успешно'), ('Не успешно', 'Не успешно')], default='Успешно', verbose_name='Статус')),
                ('mail_response', models.TextField(verbose_name='Ответ почтового сервера')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.recipient', verbose_name='Рассылка')),
            ],
        ),
    ]
