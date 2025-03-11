import secrets
from audioop import reverse

from django.views.generic import DetailView, UpdateView
from smtplib import SMTPSenderRefused
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from config.settings import EMAIL_HOST_USER
from users.models import User

logger = logging.getLogger(__name__)


class UserCreateView(CreateView):
    """ Контроллер регистрации пользователя в сервисе. """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')
    template_name = 'register.html'

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """
        Обработка корректной формы регистрации пользователя.

        :param form: Заполненная форма регистрации
        :return: HttpResponse
        """
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/email-confirm/{token}/'
        send_mail(
            subject='Подтвердите email адрес',
            message=f'Для успешной регистрации на сайте подтвердите свой email адрес по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

def email_verification(request, token: str) -> HttpResponse:
    """
    Обработка подтверждения email адреса.

    :param request: HTTP запрос
    :param token: Токен подтверждения
    :return: HttpResponse
    """
    try:
        user = get_object_or_404(User, token=token)
        logger.info(f"{user.email} пытается зарегистрироваться")
        user.is_active = True
        user.save()
        return redirect(reverse('users:login'))
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {e}")
        return redirect(reverse('users:register'))


class CustomLoginView(LoginView):
    """ Контроллер аутентификации пользователя в сервисе. """
    template_name = 'login.html'
    redirect_authenticated_user = True  # Перенаправление, если пользователь уже авторизован
    success_url = reverse_lazy("users:home")

    def form_valid(self, form):
        # Вызываем логирование при успешном входе
        logger.info(f"{form.cleaned_data['username']} вошел в систему в {timezone.now()}")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """ Контроллер выхода пользователя в сервисе. """
    template_name = 'logout.html'
    success_url = reverse_lazy("users:home")

    def dispatch(self, request, *args, **kwargs):
        # Вызываем логирование при выходе
        logger.info(f"Выход из системы в {timezone.now()}")
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(DetailView):
    """ Контроллер просмотра профиля пользователя в сервисе. """
    model = User
    template_name = 'profile.html'


class UserUpdateView(UpdateView):
    """ Контроллер редактирования профиля пользователя в сервисе. """
    model = User


@login_required
def profile_view(request) -> HttpResponse:
    """
    Контроллер для отображения профиля пользователя.

    :param request: HTTP запрос
    :return: HttpResponse
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def upload_avatar(request) -> HttpResponse:
    """
    Обработка загрузки аватара пользователя.

    :param request: HTTP запрос
    :return: HttpResponse
    """
