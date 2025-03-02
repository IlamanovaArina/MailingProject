import logging
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth import login
from logging import exception
from config.settings import EMAIL_HOST_USER
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Count
from django.urls import reverse_lazy
from mailing.forms import MailForm, RecipientForm, MailingForm
from mailing.models import *
from mailing.services import send_a_message

# Настройка логирования
logger = logging.getLogger(__name__)


# Классы представления для Mailing по принципу CRUD
class MailingListView(ListView):
    model = Mailing
    template_name = "home.html"
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        mailing = Mailing.objects.filter(owner=user)

        context["ok"] = TryRecipient.objects
        context["error"] = TryRecipient.objects
        context["count_mailing"] = TryRecipient.objects
        context["try_recipient"] = TryRecipient.objects

         # Проверяем, что пользователь авторизован
        if self.request.user.is_authenticated:
            # Количество всех рассылок
            context['mailing_all'] = Mailing.objects.filter(owner=self.request.user).count()
            # Количество запущенных рассылок
            context['status_started'] = Mailing.objects.filter(owner=self.request.user,
                                                               my_field=Mailing.STATUS_STARTED).count()
            # Количество уникальных получателей
            context['recipient_all'] = Recipient.objects.filter(owner=self.request.user).count()
        else:
            context['mailing_all'] = 0
            context['status_started'] = 0
            context['recipient_all'] = 0
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()

    def post(self, request, *args, **kwargs):
        mailing_id = request.POST.get('mailing_id')
        mailing = get_object_or_404(Mailing, id=mailing_id, owner=request.user)

        # Здесь происходит отправка рассылки
        send_a_message(mailing)

        return redirect('mailing:home')  # Перенаправьте на нужный URL после отправки


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем всех получателей этой рассылки
        context['recipients'] = self.object.recipient.all()
    #     context['mails'] = Mail.objects.all()
    #     context['mailings'] = Mailing.objects.select_related('mail', 'recipient').all()
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()


class SendMessageDetailView(DetailView):
    model = Mailing
    template_name = 'send_handmade.html'

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()  # Получаем объект рассылки
        send_a_message(mailing)  # Отправляем сообщение
        return HttpResponse("Сообщение успешно отправлено!")  # Можно перенаправить на другую страницу


class CombinedTemplateView(TemplateView):
    model = Mailing
    template_name = 'mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context['mails'] = Mail.objects.all()
        context['recipients'] = Recipient.objects.all()
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mailing.objects.filter(owner=self.request.user)
        else:
            return Mailing.objects.none()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user

        # Создаем объект Mailing
        mailing_instance = form.save()

        # Создание объектов TryRecipient для каждого получателя
        for recipient in mailing_instance.recipient.all():
            TryRecipient.objects.create(
                recipient=recipient,
                time_try=timezone.now(),
                status=TryRecipient.STATUS_OK,  # Вы можете изменить логику по статусу
                mail_response='Ответ почтового сервера'  # Замените это на реальный ответ при отправке
            )

        # Если статус "Запущена", вызываем функцию отправки писем
        if form.instance.my_field == Mailing.STATUS_STARTED:
            send_a_message(mailing_instance)

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return MailingForm


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для TryRecipient по принципу CRUD
class TryRecipientCreateView(CreateView):
    model = TryRecipient
    # form_class =
    success_url = reverse_lazy('mailing:home')
    # template_name = 'create.html'


class TryRecipientDetailView(LoginRequiredMixin, DetailView):
    model = TryRecipient
    template_name = 'mailing_detail.html'

    def get_queryset(self):
        try:
            # Получаем только те посты, которые создал текущий пользователь
            return TryRecipient.objects.filter(owner=self.request.user)
        except Exception:
            logger.info(f"Произошла такая ошибка: \n {Exception}")


class TryRecipientListView(LoginRequiredMixin, ListView):
    model = TryRecipient
    template_name = 'mailing_detail.html'

    def get_queryset(self):
        # Получаем только те посты, которые создал текущий пользователь
        try:
            # Получаем только те посты, которые создал текущий пользователь
            return TryRecipient.objects.filter(owner=self.request.user)
        except Exception:
            logger.info(f"Произошла такая ошибка: \n {Exception}")


class TryRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = TryRecipient
    template_name = 'editing.html'

    # def get_form_class(self):
    #     return MailingForm


class TryRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = TryRecipient
    template_name = 'delete.html'


# Классы представления для Recipient по принципу CRUD
class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)

    def get_form_class(self):
        return RecipientForm


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'mailing.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipient.objects.filter(owner=self.request.user)
        else:
            return Recipient.objects.none()


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'mailing_detail.html'
    context_object_name = 'tryrecipients'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipient.objects.filter(owner=self.request.user)
        else:
            return Recipient.objects.none()


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return RecipientForm


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для Mail по принципу CRUD
class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)

    def get_form_class(self):
        return MailForm


class MailDetailView(LoginRequiredMixin, DetailView):
    model = Mail
    template_name = 'mailing_detail.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mail.objects.filter(owner=self.request.user)
        else:
            return Mail.objects.none()


class MailListView(LoginRequiredMixin, ListView):
    model = Mail
    # template_name =

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Mail.objects.filter(owner=self.request.user)
        else:
            return Mail.objects.none()


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Mail
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return MailForm


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')

