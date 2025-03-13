# Generated by Django 5.1.6 on 2025-03-02 17:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_tryrecipient_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='email',
            field=models.EmailField(help_text='Рассылка будет отправлена на указанный email.',
                                    max_length=254, verbose_name='Email'),
        ),
        migrations.AddConstraint(
            model_name='recipient',
            constraint=models.UniqueConstraint(fields=('email', 'owner'), name='unique_recipient_per_owner'),
        ),
    ]
