from django.views.generic import DetailView
import secrets
from django.contrib.auth import login
from smtplib import SMTPSenderRefused
import logging
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView


# Настройка логгирования
logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
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


# class CustomLoginView(LoginView):
#     template_name = 'users:login'
#     redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
#     success_url = reverse_lazy('catalog:product_list')  # URL для перенаправления после успешного входа
#
#     def form_valid(self, form) -> HttpResponse:
#         """
#         Обрабатывает валидную форму входа в систему.
#
#         Args:
#             form (AuthenticationForm): Форма входа.
#
#         Returns:
#             HttpResponse: Редирект на страницу после успешного входа.
#         """
#         return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
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
        logger.info(f"{request.user.username} вышел из системы в {timezone.now()}")
        return super().dispatch(request, *args, **kwargs)
