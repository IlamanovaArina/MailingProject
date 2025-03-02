import secrets
from smtplib import SMTPSenderRefused
from django.contrib.auth import login
from django.utils import timezone
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from config.settings import EMAIL_HOST_USER
from users.models import User

logger = logging.getLogger(__name__)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('/users/login/')
    template_name = '../templates/register.html'

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """
        Обрабатывает валидную форму пользователя, сохраняет его и отправляет электронное письмо для подтверждения.

        Args:
            form (UserRegisterForm): Форма регистрации пользователя.

        Returns:
            HttpResponse: Редирект на страницу успешного завершения регистрации.
        """
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        # Вызываем логирование при успешной регистрации
        logger.info(f"{form.cleaned_data['email']} зарегистрировался в {timezone.now()}")
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        try:
            subject = 'Спасибо за регистрацию!'
            message = 'Вы успешно зарегистрировались на нашем сайте!'
            from_email = EMAIL_HOST_USER
            recipient_list = [user_email]
            send_mail(subject, message, from_email, recipient_list)
        except SMTPSenderRefused:
            return reverse_lazy('users:error')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
    success_url = reverse_lazy("users:home")

    def form_valid(self, form):
        # Вызываем логирование при успешном входе
        logger.info(f"{form.cleaned_data['username']} вошел в систему в {timezone.now()}")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    success_url = reverse_lazy("users:home")

    def dispatch(self, request, *args, **kwargs):
        # Вызываем логирование при выходе
        logger.info(f"{request.users.email} вышел из системы в {timezone.now()}")
        return super().dispatch(request, *args, **kwargs)