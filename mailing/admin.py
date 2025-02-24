from django.contrib import admin

from mailing.models import Recipient, Mail, Mailing, TryRecipient


@admin.register(Recipient)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment' )
    list_filter = ('email',)
    search_fields = ('email', 'id')


@admin.register(Mail)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'body_mail' )


@admin.register(Mailing)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'startDt', 'endDt', 'my_field', 'mail',)
    list_filter = ('my_field', )
    search_fields = ('id', )


@admin.register(TryRecipient)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_try', 'status', 'mail_response', 'recipient',)
    search_fields = ('mail_response', 'recipient', 'status',)
