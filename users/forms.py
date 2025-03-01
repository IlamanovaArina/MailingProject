from django.contrib.auth.forms import UserCreationForm
from users.models import User
from mailing.forms import StyleFormMixin
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "phone", "country", "password1", "password2")

    # def create_password_fields(self, *args, **kwargs):
    #     password1 = forms.CharField(verbose_name='Придумайте пароль')
    #     password2 = forms.CharField(verbose_name='Введите повторно пароль')
    #     super().create_password_fields(*args, **kwargs)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры.')
        return phone_number

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите электронную почту'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Добавьте изображение'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите номер телефона'
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите страну проживания'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тот же пароль'
        })
