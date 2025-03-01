from django.views.generic import DetailView
import secrets

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserRegisterForm) -> HttpResponse:
        user = form.save()  # Сохраняем пользователя
        user.is_active = False
        user.save()
        send_mail(
            subject='Спасибо за регистрацию!',
            message=f'Вы успешно зарегистрировались на нашем сайте.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


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
    success_url = reverse_lazy("users:login")


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    success_url = reverse_lazy("users:login")


# class UserDetailView(DetailView):
#     model = User
#     template_name = 'base.html'
#     context_object_name = 'profile'