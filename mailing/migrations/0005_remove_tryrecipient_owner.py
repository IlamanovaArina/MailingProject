# Generated by Django 5.1.6 on 2025-03-04 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_tryrecipient_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tryrecipient',
            name='owner',
        ),
    ]
