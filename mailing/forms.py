from django.forms import BooleanField
from django import forms
from mailing.models import Mail, Recipient, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment',]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control ',
            'placeholder': 'Введите имя'
        })
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте комментарий'
        })


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['theme', 'body_mail',]

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields['theme'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему письма'
        })
        self.fields['body_mail'].widget.attrs.update({
            'class': 'form-control ',
            'placeholder': 'Ваше сообщение'
        })


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['my_field', 'mail', 'recipient']
        exclude = ['startDt', 'endDt',]

    def __init__(self, user, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['my_field'].choices = [
            (Mailing.STATUS_NEW, 'Создана'),
            (Mailing.STATUS_STARTED, 'Запущена'),
        ]
        self.fields['my_field'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите статус'
        })
        if user:
            # Фильтруем получателей по текущему пользователю
            self.fields['mail'].queryset = Mail.objects.filter(owner=user)
        self.fields['mail'].widget.attrs.update({
            'class': 'form-control ',
            'placeholder': 'Ваше сообщение:'
        })
        if user:
            # Фильтруем получателей по текущему пользователю
            self.fields['recipient'].queryset = Recipient.objects.filter(owner=user)
        self.fields['recipient'].widget.attrs.update({
            'class': 'form-control ',
            'placeholder': 'Выберите получателя'
        })
