import logging
import datetime
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mailing.forms import MailForm, RecipientForm, MailingForm, MailingUpdateForm
from mailing.models import *
from mailing.services import send_a_message
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Настройка логирования
logger = logging.getLogger(__name__)


# Классы представления для Mailing по принципу CRUD

@method_decorator(
    cache_page(60), name="dispatch"
)  # Кешировать представление на минуту
class MailingListView(ListView):
    """
        Представление для списка рассылок, с кэшированием данных на 5 минут.

        Модель: Mailing
        Шаблон: "home.html"
        Контекст: 'mailings' - список рассылок текущего пользователя.
    """
    model = Mailing
    template_name = "home.html"
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        """
            Получает данные контекста для шаблона.

            Если пользователь аутентифицирован, получает информацию о рассылках из кэша,
            в противном случае инициализирует значения для анонимного пользователя.

            :param kwargs: Дополнительные аргументы для передачи.
            :return: Словарь с данными контекста для шаблона.
        """
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # Идентификатор кеша можно формировать на основе пользователя
            cache_key = f"user_{self.request.user.id}_mailing_data"
            cached_data = cache.get(cache_key)

            if cached_data is None:
            # Если данные не закешированы, получаем их из базы данных
                # Проверяем, что пользователь принадлежит к группе модераторов
                if self.request.user.groups.filter(name='moderator').exists():
                    cached_data = {
                        # Количество всех рассылок
                        'mailing_all':Mailing.objects.all().count(),
                        # Количество запущенных рассылок
                        'status_started':Mailing.objects.filter(my_field=Mailing.STATUS_STARTED).count(),
                        # Количество уникальных получателей
                        'recipient_all':Recipient.objects.all().count(),
                        # Количество успешных попыток рассылок
                        'status_ok':TryRecipient.objects.filter(status='Успешно').count(),
                        # Количество неуспешных попыток рассылки
                        'status_error': TryRecipient.objects.filter( status='Не успешно').count(),
                        # Количество отправленных сообщений
                        'sum_recipient': TryRecipient.objects.all().count(),
                        'mailings': Mailing.objects.all(),
                    }
                    # Сохраняем данные в кеш на минуту
                    cache.set(cache_key, cached_data, 60)


                # Проверяем, что пользователь авторизован
                elif self.request.user.is_authenticated:
                    cached_data = {
                        # Количество всех рассылок
                        'mailing_all': Mailing.objects.filter(owner=self.request.user).count(),
                        # Количество запущенных рассылок
                        'status_started': Mailing.objects.filter(owner=self.request.user,
                                                                       my_field=Mailing.STATUS_STARTED).count(),
                        # Количество уникальных получателей
                        'recipient_all': Recipient.objects.filter(owner=self.request.user).count(),
                        # Количество успешных попыток рассылок
                        'status_ok': TryRecipient.objects.filter(owner=self.request.user, status='Успешно').count(),
                        'status_error': TryRecipient.objects.filter(owner=self.request.user, status='Не успешно').count(),
                        # Количество отправленных сообщений
                        'sum_recipient': TryRecipient.objects.filter(owner=self.request.user).count(),
                        'mailings': Mailing.objects.filter(owner=self.request.user),
                    }
                    # Сохраняем данные в кеш на минуту
                    cache.set(cache_key, cached_data, 60)
            # В контекст кладём сохранённый словарь
            context.update(cached_data)
        else:
            context['mailing_all'] = 0
            context['status_started'] = 0
            context['recipient_all'] = 0
            context['status_ok'] = 0
            context['status_error'] = 0
            context['sum_recipient'] = 0
        return context

    def get_queryset(self):
        """ Возвращает все объекты владельца """
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()

    def post(self, request, *args, **kwargs):
        """ При нажатии на кнопку отправить """
        mailing_id = request.POST.get('mailing_id')
        mailing = get_object_or_404(Mailing, id=mailing_id, owner=request.user)

        # Здесь происходит отправка рассылки
        send_a_message(mailing)

        return redirect('mailing:home')  # Перенаправьте на нужный URL после отправки


@method_decorator(
    cache_page(60), name="dispatch"
)  # Кешировать представление на минуту
class MailingDetailView(LoginRequiredMixin, DetailView):
    """
        Представление для детальной информации о рассылке.

        Модель: Mailing
        Шаблон: "mailing_detail.html"
    """
    model = Mailing
    template_name = 'mailing_detail.html'

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста для детального просмотра рассылки.
        """
        context = super().get_context_data(**kwargs)
        # Для проверки в шаблонах на модератора
        context['is_moderator'] = self.request.user.is_authenticated and self.request.user.groups.filter(name='moderator').exists()
        # Получаем всех получателей этой рассылки
        context['recipients'] = self.object.recipient.all()
        # Получаем все попытки рассылок для этой рассылки
        context['tryrecipients'] = TryRecipient.objects.filter(recipient__in=context['recipients'])
        return context

    def get_queryset(self):
         # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        elif self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()


class SendMessageDetailView(DetailView):
    """
        Представление для отправки сообщения о рассылке.

        Модель: Mailing
        Шаблон: "send_handmade.html"
    """
    model = Mailing
    template_name = 'send_handmade.html'

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()  # Получаем объект рассылки
        send_a_message(mailing)  # Отправляем сообщение
        return redirect('mailing:home')


@method_decorator(
    cache_page(60), name="dispatch"
)  # Кешировать представление на минуту
class CombinedTemplateView(TemplateView):
    """
        Отображает шаблон с данными о рассылках, письмах и получателях.

        Модель: Mailing
        Шаблон: "mailing.html"
    """
    model = Mailing
    template_name = 'mailing.html'

    def get_context_data(self, **kwargs):
        """
            Получает данные контекста для отображения шаблона.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='moderator').exists():
            context['mailings'] = Mailing.objects.all()
            context['mails'] = Mail.objects.all()
            context['recipients'] = Recipient.objects.all()
        elif self.request.user.is_authenticated:
            context['mailings'] = Mailing.objects.filter(owner=self.request.user)
            context['mails'] = Mail.objects.filter(owner=self.request.user)
            context['recipients'] = Recipient.objects.filter(owner=self.request.user)
        return context


    def get_queryset(self):
        # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()


@method_decorator(
    cache_page(60), name="dispatch"
)  # Кешировать представление на минуту
class MailingCreateView(LoginRequiredMixin, CreateView):
    """
       Представление для создания новой рассылки.

       Модель: Mailing
       Форма для создания рассылки: MailingForm
       URL для перенаправления после успешного создания: 'mailing:mailing'
       Имя шаблона для отображения: create.html
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def get_form_kwargs(self):
        """
        Получает аргументы для формы.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        """
            Обрабатывает валидные данные формы.
        """
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user

        # Создаем объект Mailing
        mailing = form.save()

        if mailing.my_field == 'Запущена':
            # Если статус "Запущена", отправляем сообщение получателям
            send_a_message(mailing)

        return super().form_valid(form)


@method_decorator(
    cache_page(60), name="dispatch"
)  # Кешировать представление на минуту
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
       Представление для редактирования существующей рассылки.

        Модель: Mailing
        Шаблон: "editing.html"
        URL для перенаправления после успешного создания: 'mailing:mailing'
    """
    model = Mailing
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return MailingUpdateForm

    def form_valid(self, form):
        """ При указании статуса "Завершена", устанавливать endDt """
        mailing = form.save()
        if mailing.my_field == "Завершена":
            mailing.endDt = datetime.datetime.now()

        mailing.save()

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления рассылки."""
    model = Mailing
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для TryRecipient по принципу CRUD
class TryRecipientCreateView(CreateView):
    """ Представление для создания нового получателя рассылки."""
    model = TryRecipient
    success_url = reverse_lazy('mailing:home')
    # template_name = 'create.html'


class TryRecipientDetailView(LoginRequiredMixin, DetailView):
    """ Представление для отображения деталей получателя рассылки."""

    model = TryRecipient

    def get_queryset(self):
         # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return TryRecipient.objects.all()
        elif self.request.user.is_authenticated:
            return TryRecipient.objects.filter(owner=self.request.user)
        else:
            return TryRecipient.objects.none()


class TryRecipientListView(LoginRequiredMixin, ListView):
    """ Представление для отображения деталей информации о рассылке."""
    model = TryRecipient
    template_name = 'try_recipient.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='moderator').exists():
            context['try_recipients'] = TryRecipient.objects.filter()
        elif self.request.user.is_authenticated:
            # Получаем всех получателей этой рассылки
            context['try_recipients'] = TryRecipient.objects.filter(owner=self.request.user)
        return context

    def get_queryset(self):
         # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return TryRecipient.objects.all()
        elif self.request.user.is_authenticated:
            return TryRecipient.objects.filter(owner=self.request.user)
        else:
            return TryRecipient.objects.none()


class TryRecipientUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для обновления информации о рассылке."""
    model = TryRecipient
    template_name = 'editing.html'


class TryRecipientDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления информации о рассылке."""
    model = TryRecipient
    template_name = 'delete.html'


# Классы представления для Recipient по принципу CRUD
class RecipientCreateView(LoginRequiredMixin, CreateView):
    """ Представление для создания получателя."""
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        """Обрабатывает допустимую форму."""
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """ Представление для отображения деталей получателя."""
    model = Recipient
    template_name = 'mailing.html'

    def get_queryset(self):
        # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Recipient.objects.filter(owner=self.request.user)
        else:
            return Recipient.objects.none()


class RecipientListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка получателей."""
    model = Recipient
    template_name = 'mailing_detail.html'
    context_object_name = 'tryrecipients'

    def get_queryset(self):
        # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Recipient.objects.filter(owner=self.request.user)
        else:
            return Recipient.objects.none()


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для обновления получателя."""
    model = Recipient
    template_name = 'editing.html'
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:mailing')


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления получателя."""
    model = Recipient
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для Mail (сообщений) по принципу CRUD
class MailCreateView(LoginRequiredMixin, CreateView):
    """ Представление для создания письма."""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailDetailView(LoginRequiredMixin, DetailView):
    """ Представление для отображения деталей письма."""
    model = Mail
    template_name = 'mailing_detail.html'

    def get_queryset(self):
        # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Mail.objects.filter(owner=self.request.user)
        else:
            return Mail.objects.none()


class MailListView(LoginRequiredMixin, ListView):
    """ Представление для отображения списка писем."""
    model = Mail

    def get_queryset(self):
        # Проверяем, что пользователь принадлежит к группе модераторов
        if self.request.user.groups.filter(name='moderator').exists():
            return Mailing.objects.all()
        if self.request.user.is_authenticated:
            return Mail.objects.filter(owner=self.request.user)
        else:
            return Mail.objects.none()


class MailUpdateView(LoginRequiredMixin, UpdateView):
    """ Представление для редактирования письма."""
    model = Mail
    template_name = 'editing.html'
    form_class = MailForm
    success_url = reverse_lazy('mailing:mailing')


class MailDeleteView(LoginRequiredMixin, DeleteView):
    """ Представление для удаления письма."""
    model = Mail
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')
