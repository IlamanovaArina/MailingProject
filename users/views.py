from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from config.settings import EMAIL_HOST_USER
from django.http import Http404
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
import secrets


class UserCreateView(CreateView):
    """ Контроллер регистрации пользователя в сервисе. """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'register.html'

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        """
        Обработка корректной формы регистрации пользователя.

        :param form: Заполненная форма регистрации
        :return: HttpResponse
        """
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(16)
        # user.token_created_at = timezone.now()  # если есть поле для времени
        user.save()

        # формируем абсолютную ссылку корректно
        path = reverse('users:email-confirm', args=[user.token])
        url = self.request.build_absolute_uri(path)

        subject = 'Подтвердите email адрес'
        message = f'Перейдите по ссылке для подтверждения: {url}'
        # можно использовать render_to_string для HTML-шаблона

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        except Exception:
            # логируем ошибку и, возможно, удаляем созданного пользователя или ставим флаг
            # logger.exception("Ошибка при отправке письма подтверждения")
            pass

        return super().form_valid(form)


def email_verification(request, token: str) -> HttpResponse:
    """
    Обработка подтверждения email адреса.

    :param request: HTTP запрос
    :param token: Токен подтверждения
    :return: HttpResponse
    """
    user = get_object_or_404(User, token=token)

    # при наличии времени создания токена проверяем срок годности
    # if hasattr(user, 'token_created_at'):
    #     max_age = timezone.timedelta(days=1)
    #     if timezone.now() - user.token_created_at > max_age:
    #         # токен просрочен
    #         # logger.info("Просроченный токен подтверждения")
    #         return redirect('users:register')

    if user.is_active:
        # уже активирован
        return redirect('users:login')

    user.is_active = True
    user.token = ''
    # если есть token_created_at, можно очистить
    user.save()
    return redirect('users:login')


class CustomLoginView(LoginView):
    """ Контроллер аутентификации пользователя в сервисе. """
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        # Вызываем логирование при успешном входе
        # logger.info(f"{form.cleaned_data['username']} вошел в систему в "
        #             f"{timezone.now()}")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """ Контроллер выхода пользователя в сервисе. """
    template_name = 'logout.html'
    next_page = reverse_lazy("mailing:home")


class UserDetailView(DetailView):
    """ Контроллер просмотра профиля пользователя в сервисе. """
    model = User
    template_name = 'profile.html'


class UserUpdateView(UpdateView):
    """ Контроллер редактирования профиля пользователя в сервисе. """
    model = User
    form_class = UserUpdateForm
    template_name = 'profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')  # или build url с username




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
